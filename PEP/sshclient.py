import grpc
import sshgrpc_pb2
import sshgrpc_pb2_grpc

def run():
    with grpc.insecure_channel('192.168.71.3:50051') as channel:
        stub = sshgrpc_pb2_grpc.ExampleServiceStub(channel)
        response = stub.SayHello(sshgrpc_pb2.HelloRequest(name='World'))
        print(f'Client received: {response.message}')

if __name__ == '__main__':
    run()
