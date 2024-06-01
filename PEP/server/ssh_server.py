from concurrent import futures
import grpc
import credentials_pb2
import credentials_pb2_grpc
import os 
import json

# 憑證儲存
def store_credential_files(user_id, credential):
    # 提取 credential 的各個屬性並轉換為可序列化的格式
    credential_id = credential["credential_id"].hex()
    public_key = {
        k: v.hex() if isinstance(v, bytes) else v
        for k, v in credential["public_key"].items()
    }
    sign_count = 0  # 假設初始簽名計數為 0
    transports = "usb"  # 假設默認傳輸方式為 USB
    aaguid = credential["aaguid"].hex()
   
    # 將屬性轉換為字典格式
    credential_data = {
        "user_id": user_id.decode("utf-8"),
        "public_key": public_key,
        "sign_count": sign_count,
        "transports": transports,
        "aaguid": aaguid,
        "credential_id": credential_id,
    }
    
    # 將字典格式轉換為 JSON 並儲存到文件中
    filename = f'credentials/credential.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(credential_data, f, indent=4)

class CredentialServiceServicer(credentials_pb2_grpc.CredentialServiceServicer):
   
    def StoreCredential(self, request, context):
        user_id = request.user_id
        credentials = {
            "aaguid": request.aaguid,
            "credential_id": request.credential_id,
            "public_key": request.public_key,
        }
        print(f"Received credentials for user_id {user_id}: {credentials}")
        # 在這裡儲存憑證
        store_credential_files(user_id, credentials)
        return credentials_pb2.CredentialResponse(message="Credentials stored successfully")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    credentials_pb2_grpc.add_CredentialServiceServicer_to_server(CredentialServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Server started on port 50051.')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
