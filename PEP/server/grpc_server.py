from concurrent import futures
import grpc
import credentials_pb2
import credentials_pb2_grpc

class CredentialServiceServicer(credentials_pb2_grpc.CredentialServiceServicer):
    def StoreCredential(self, request, context):
        user_id = request.user_id
        credentials = {
            "user_id": user_id,
            "public_key": {
                "kty": request.public_key.kty,
                "alg": request.public_key.alg,
                "crv": request.public_key.crv,
                "x": request.public_key.x,
                "y": request.public_key.y,
            },
            "sign_count": request.sign_count,
            "transports": request.transports,
            "aaguid": request.aaguid,
            "credential_id": request.credential_id
        }
        print(f"Received credentials for user_id {user_id}: {credentials}")
        # 在這裡儲存憑證
        self.store_credential_files(user_id, credentials)
        return credentials_pb2.CredentialResponse(message="Credentials stored successfully")
    
    def store_credential_files(self, user_id, credentials):
        # 這裡是儲存憑證的邏輯
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    credentials_pb2_grpc.add_CredentialServiceServicer_to_server(CredentialServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Server started on port 50051.')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
