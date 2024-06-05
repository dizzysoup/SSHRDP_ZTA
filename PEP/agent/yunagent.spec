# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['yunagent.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('credentials/credential.json', 'credentials'),
        ('credentials/data.json', 'credentials'),
        ('fido2/*', 'fido2'),
        ('gRPC/credentials_pb2.py', 'gRPC'),
        ('gRPC/credentials_pb2_grpc.py', 'gRPC'),
        ('gRPC/gRPC.py', 'gRPC')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='yunagent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='your_executable_name'
)
