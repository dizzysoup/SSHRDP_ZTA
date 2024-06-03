# PEP 說明

## agent 核心程式
yunagent.py
Fido 驅動程式 >> Fido 資料夾
credentials >> 憑證資料夾(local stored)
### gRPC 核心
sshgrpc_pb2

## register 
```python
    yunagent register --pep 192.168.71.3:50051 --user admin
```

## Server 


進入python虛擬環境
```python
    source myvenv/bin/activate
```

生成python code 
```python
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. credentials.proto
```
