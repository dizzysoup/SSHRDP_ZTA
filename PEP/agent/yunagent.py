from fido2.hid import CtapHidDevice
from fido2.client import Fido2Client, WindowsClient, UserInteraction
from fido2.server import Fido2Server
from fido2.cose import CoseKey , ES256 , ES256K
from getpass import getpass
import sys
import ctypes
import subprocess
import argparse
import paramiko
import time 
import socket
import select 
import sys 
import json 
import os

try:
    from fido2.pcsc import CtapPcscDevice
except ImportError:
    CtapPcscDevice = None


uv = "discouraged"

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

# 憑證提取
def load_credential_files():
    # 從文件中加載 JSON 數據
    with open('credentials/credential.json', 'r') as f:
        credential_data = json.load(f)   
    # 組裝為原始格式的字典
    credential = AttestedCredentialData.from_dict(credential_data)
    return credential


def enumerate_devices():
    for dev in CtapHidDevice.list_devices():
        yield dev
    if CtapPcscDevice:
        for dev in CtapPcscDevice.list_devices():
            yield dev


index = 0 

# Handle user interaction
class CliInteraction(UserInteraction):
    def prompt_up(self):
        print("\nTouch your authenticator device now...\n")

    def request_pin(self, permissions, rd_id):
        return getpass("Enter PIN: ")

    def request_uv(self, permissions, rd_id):
        print("User Verification required.")
        return True

class AttestedCredentialData:
    def __init__(self, aaguid, credential_id, public_key):
        print(public_key)
        self.aaguid = aaguid
        self.credential_id =credential_id
        self.public_key =  ES256(public_key)
        
    @staticmethod
    def from_dict(data):
        aaguid = bytes.fromhex(data['aaguid'])
        credential_id = bytes.fromhex(data['credential_id'])
        public_key = {
            int(k): bytes.fromhex(v) if isinstance(v, str) and all(c in '0123456789abcdef' for c in v) else v
            for k, v in data['public_key'].items()
        }
        return AttestedCredentialData(aaguid, credential_id, public_key)

if WindowsClient.is_available() and not ctypes.windll.shell32.IsUserAnAdmin():
    # Use the Windows WebAuthn API if available, and we're not running as admin
    client = WindowsClient("https://example.com")
else:
    # Locate a device
    for dev in enumerate_devices():
        client = Fido2Client(
            dev, "https://example.com", user_interaction=CliInteraction()
        )
        if client.info.options.get("rk"):
            break
    else:
        print("No Authenticator with support for resident key found!")
        sys.exit(1)

    # Prefer UV if supported
    if client.info.options.get("uv"):
        uv = "preferred"
        print("Authenticator supports User Verification")

parser = argparse.ArgumentParser(description='Example script with a positional argument.')
subparsers = parser.add_subparsers(dest='command', help='sub-command help')

# register sub-command
register_parser = subparsers.add_parser('register', help='register help')
register_parser.add_argument('--pep' , type=str , help='The PEP address')
register_parser.add_argument('--user', type=str, help='The username')

#login sub-command
login_parser = subparsers.add_parser('login', help='login help')
login_parser.add_argument('--pep' , type=str , help='The PEP address')
login_parser.add_argument('--user', type=str, help='The username')


# ssh sub-command
ssh_parser = subparsers.add_parser('ssh', help='ssh command')
ssh_parser.add_argument("argtext", type=str, help="SSH command")


# parser.add_argument('argtext', help='IP address to connect')

args = parser.parse_args()
print(args)
server = Fido2Server({"id": "example.com", "name": "Example RP"}, attestation="direct")
credentials_data = "" 
match args.command:
    case "register" :
        pep_address = args.pep
        username = args.user
        user = {"id": str(index).encode("utf-8") , "name": username}
        # Prepare parameters for makeCredential
        create_options, state = server.register_begin(
            user,
            resident_key_requirement="required",
            user_verification=uv,
            authenticator_attachment="cross-platform",
        )       
        # Create a credential
        result = client.make_credential(create_options["publicKey"])
        # Complete registration
        auth_data = server.register_complete(
            state, result.client_data, result.attestation_object
        )
        
        credentials_data = [auth_data.credential_data]
        credentials = {
            "aaguid": auth_data.credential_data.aaguid,
            "credential_id": auth_data.credential_data.credential_id,
            "public_key": auth_data.credential_data.public_key
        }
        print(auth_data.credential_data)
        print("New credential created!")
        # 儲存憑證
        store_credential_files(user["id"], credentials)   
        
    case "login" : 
        pep_address = args.pep
        username = args.user
        
        # 讀取憑證
        credential = load_credential_files()
        # Prepare parameters for getAssertion
        request_options, state = server.authenticate_begin(user_verification=uv)
        
        # Authenticate the credential
        selection = client.get_assertion(request_options["publicKey"])
        result = selection.get_response(0)  # There may be multiple responses, get the first.
        
        print("USER ID:", result.user_handle)

        # server 端驗證
        server.authenticate_complete(
            state,
            [credential],
            result.credential_id,
            result.client_data,
            result.authenticator_data,
            result.signature,
        )
        print("Credential authenticated!")
        
    case "ssh":        
       

        
       
        
        ip = args.argtext.split('@')[1]
        user = {"id": str(index).encode("utf-8") , "name": args.argtext.split('@')[0]}     
        command = ["ssh" ,  args.argtext ]   
        subprocess.run(command, check=True)
        
        