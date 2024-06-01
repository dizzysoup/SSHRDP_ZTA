import paramiko
import threading
import sys
import termios
import tty
import socket


'''
# 定義一個用戶名和密碼的驗證函數
def check_auth(username, password):
    r = requests.post("http://192.168.166.16:3000/", data = {'username' : username, 'password' : password})
    print(r.text)
    print("身分驗證成功")
    return username == 'pep' and password == 'pep'

'''

# 定義一個 SSH 伺服器類別
class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        
    def check_auth_password(self, username, password):
        #if check_auth(username, password):
        #    return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_SUCCESSFUL
    
    def check_channel_shell_request(self, channel):
        return True
            

def ssh_connect_and_interact(host, port, username, password , chan):
    #創建 Transport 對象
    trans = paramiko.Transport((host, port))
    try:
        # 啟動client
        trans.start_client()       
        # 認證頻證
        trans.auth_password(username=username, password=password)
        # 打開session channel (for RP )
        channel = trans.open_session()
        channel.get_pty()
        channel.invoke_shell()
        command = ""
        def read_from_channel(channel):
            buffer = ""
            chk = False
            while True:
                if channel.recv_ready():
                    buffer = channel.recv(1024).decode('utf-8')
                    
                    # 傳送給agent ，處理整行        
                    if '\n' in buffer and chk == True:
                        line, buffer = buffer.split('\n', 1)
                        chan.send(line)
                        chan.send(buffer)
                    else :
                        chan.send(buffer)
                        chk = True                    
                        
                    
        # 開始一個thread 來讀取RP端發送的輸出
        threading.Thread(target=read_from_channel, args=(channel,), daemon=True).start()

        
        while True:
            command = chan.recv(1024)
            if command == '\x03':  # Ctrl+C
                break
            channel.send(command)


    finally:
        # 關閉通道及傳輸
        channel.close()
        trans.close()

if __name__ == "__main__":
    host = '192.168.71.4'
    port = 22
    username = 'linuxrp'
    password = 'linuxrp'
    # 伺服器的 RSA 金鑰
    host_key = paramiko.RSAKey.from_private_key_file('/etc/ssh/ssh_host_rsa_key')
    
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
       
    ssh_connect_and_interact(host, port, username, password, chan)
