import subprocess
import argparse
import paramiko
import time 
import socket
import select 
import sys 

parser = argparse.ArgumentParser(description='Example script with a positional argument.')
parser.add_argument('command', help='Input value')
parser.add_argument('ip', help='IP address to connect')

args = parser.parse_args()
print(args)
if args.command == "ssh":
    print('進行身分認證')
    try :
        command = ["ssh", args.ip, "-p", "2223"]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        command = ["ssh", args.ip]
        result = subprocess.run(command, check=True)
        print(result.stdout)