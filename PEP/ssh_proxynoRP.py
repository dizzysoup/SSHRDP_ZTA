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
import base64 

# 生成RSA金鑰對
def generate_rsa_keypair():
    (public_key , privkey) = rsa.newkeys(1024)
        
    private_key_path = os.path.expanduser("/root/.ssh/id_rsa")
    public_key_path = os.path.expanduser("/root/.ssh/id_rsa.pub")
    
    # 保存私鑰到文件
    pub = public_key.save_pkcs1()
    pubfile = open(private_key_path , 'wb')
    pubfile.write(pub)
    pubfile.close()
    
    # 保存公鑰到文件
    pri = privkey.save_pkcs1()
    prifile = open(public_key_path , 'wb')
    prifile.write(pri)
    prifile.close()

    print("RSA key pair generated successfully.")

    return private_key_path, public_key_path





# 定義一個用戶名和密碼的驗證函數
def check_auth(username, password):
    r = requests.post("http://192.168.166.16:3000/", data = {'username' : 'pep' , 'password' : 'pep'})
    print(r.text)
    print("身分驗證成功")
    return username == 'root' and password == 'pep'


# 定義一個 SSH 伺服器類別

class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    
    # password check     
    def check_auth_password(self, username, password):
        if check_auth(username, password):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED   
    def check_channel_shell_request(self, channel):
        return True

# 伺服器的 RSA 金鑰
host_key = paramiko.ECDSAKey(filename="/etc/ssh/ssh_host_ecdsa_key")


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
    chan.send("\r\nWelcome to My SSH Server!\r\n")
    
    
except Exception as e:
    print("無法建立伺服器:", e)
    raise



  