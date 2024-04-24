import paramiko
import threading
import socket
import sys
import subprocess
import termios
import select 
import requests

# 伺服器的 RSA 金鑰
host_key = paramiko.RSAKey.generate(2048)

# 定義一個用戶名和密碼的驗證函數
def check_auth(username, password):
    # 在這裡你可以添加你的身份驗證邏輯，例如從資料庫中檢查用戶名和密碼
    # 這個例子中，只是簡單地固定了一組用戶名和密碼
    
    r = requests.post("http://192.168.166.16:3000/", data = {'username' : 'pep' , 'password' : 'pep'})
    print(r.text)
    print("身分驗證成功")
    return username == 'pep' and password == 'pep'

# 定義一個 SSH 伺服器類別
class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    # 通道request
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    # 帳號密碼確認
    def check_auth_password(self, username, password):
        if check_auth(username, password):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    # shell request
    def check_channel_shell_request(self, channel):
        return True

# 建立一個 SSH 伺服器
try:
    # 初始化 SSH 伺服器
    ssh_server = SSHServer()
    
    # 建立一個 socket 並綁定到指定的port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 2223))
    server_socket.listen(100)
    print("等待連接......")
    
    # 等待並處理客戶端的連接
    client_socket, client_addr = server_socket.accept()
    print(f"與 {client_addr} 建立連接")

    # 初始化傳輸層
    transport = paramiko.Transport(client_socket)
    transport.add_server_key(host_key)
    transport.start_server(server=ssh_server)

    # 等待連接建立
    chan = transport.accept(20)
    if chan is None:
        print('*** No channel.')
        sys.exit(1)

    print('[+] 連接成功！')

    # 開啟 shell
    chan.send('\r\nWelcome to My SSH Server!\r\n')

    # Jump Box 

    # 建立一个socket
    trans = paramiko.Transport(('192.168.166.11', 22))
    # 啟動客戶端
    trans.start_client()
    # 帳號密碼登入
    trans.auth_password(username='resource', password='resource')
    # 打開通道
    channel = trans.open_session()
    # 取得終端
    channel.get_pty()
    # xshell 終端
    channel.invoke_shell()


    oldtty = termios.tcgetattr(sys.stdin)
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
                print(result)
                chan.send(result)

           #  output = subprocess.check_output(command.decode(), shell=True)
            
        except Exception as e:
            chan.send(str(e))       

    # 關閉連接
   # chan.close()
   # transport.close()
   # server_socket.close()

except Exception as e:
    print("無法建立伺服器:", e)
    raise
