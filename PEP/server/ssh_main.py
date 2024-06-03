from ssh_server import start_ssh_server
from grpc_server import start_gGPC_server
import threading


# port 2223
ssh_thread = threading.Thread(target=start_ssh_server,daemon=True)
# port 50051
grpc_thread = threading.Thread(target=start_gGPC_server, daemon=True)

ssh_thread.start()
grpc_thread.start()

ssh_thread.join()
grpc_thread.join()


