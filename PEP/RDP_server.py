import socket
import threading


# 定义代理服务器的地址和端口
PROXY_HOST = '192.168.166.18'
PROXY_PORT = 3389

# 定义RDP服务器的地址和端口
RDP_SERVER_HOST = '192.168.166.17'
RDP_SERVER_PORT = 3389
    

def forward_data(source, destination):
    while True:
        data = source.recv(4096)
        if not data:
            break
        destination.sendall(data)
    source.close()
    destination.close()
    

def handle_client(client_socket):
    
    rdp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rdp_server_socket.connect((RDP_SERVER_HOST, RDP_SERVER_PORT))
    
    auth_data = client_socket.recv(1024).decode("latin1")
    auth_part = auth_data.split("mstshash=")[1]
    print(f"Received authentication data: {auth_part}")
    
    rdp_server_socket.sendall(auth_data.encode("latin1"))
    client_to_server_thread = threading.Thread(target=forward_data, args=(client_socket, rdp_server_socket))
    server_to_client_thread = threading.Thread(target=forward_data, args=(rdp_server_socket, client_socket))

    client_to_server_thread.start()
    server_to_client_thread.start()
   
    #username = client_socket.recv(1024).decode("latin1")
    # print(f"Received username: {username}")
    print("??")    

def main():
    # 创建代理服务器的套接字
    proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server_socket.bind((PROXY_HOST, PROXY_PORT))
    proxy_server_socket.listen(5)

    print(f"Proxy server listening on {PROXY_HOST}:{PROXY_PORT}")
    try:
        while True:
            client_socket, client_address = proxy_server_socket.accept()
            print(f"Connection from {client_address}")            
            handle_client(client_socket)
    except KeyboardInterrupt:
        print("Proxy server shutting down...")
        proxy_server_socket.close()

if __name__ == "__main__":
    main()
