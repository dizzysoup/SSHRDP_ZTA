import grpc
from gRPC import credentials_pb2
from gRPC import credentials_pb2_grpc
import json
from fido2.cose import ES256 


class CredentialClient : 
    def __init__(self, server_address):
        self.server_address = server_address
    
    # 傳送給server
    def send_credentials_to_server(self,user_id, credentials):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.CredentialServiceStub(channel)
           
            
            public_key = credentials_pb2.PublicKey(
                kty= credentials["public_key"][1],
                alg= int(credentials["public_key"][3]),
                crv= int(credentials["public_key"][-1]),
                x=credentials["public_key"][-2],
                y=credentials["public_key"][-3]
            )
            
            request = credentials_pb2.CredentialRequest(
                user_id=str(user_id),
                public_key=public_key,
                sign_count=credentials["sign_count"],
                transports=credentials["transports"],
                aaguid=credentials["aaguid"],
                credential_id=credentials["credential_id"]
            )
            
            response = stub.StoreCredential(request)
            print(response.message)
            
    # credential authentication
    def send_credentials_to_auth(self,user_id, credentials):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.CredentialServiceStub(channel)      
            
            print(credentials)
                 
            public_key = credentials_pb2.PublicKey(
                kty= credentials["public_key"]['1'],
                alg= int(credentials["public_key"]['3']),
                crv= int(credentials["public_key"]['-1']),
                x=credentials["public_key"]['-2'],
                y=credentials["public_key"]['-3']
            )
            
            request = credentials_pb2.CredentialRequest(
                user_id=str(user_id),
                public_key=public_key,
                sign_count=credentials["sign_count"],
                transports=credentials["transports"],
                aaguid=credentials["aaguid"],
                credential_id=credentials["credential_id"]
            )
            
            response = stub.SendCredentialToAuth(request)
            print(response.message)
            return response.message
    # logout
    def send_logout_to_server(self):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.CredentialServiceStub(channel)
            request = credentials_pb2.LogoutMsg(message="0")
            response = stub.Logout(request)
            print(response.message)
            return response.message