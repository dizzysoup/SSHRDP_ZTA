# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: credentials.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x63redentials.proto\x12\x0b\x63redentials\"H\n\tPublicKey\x12\x0b\n\x03kty\x18\x01 \x01(\x05\x12\x0b\n\x03\x61lg\x18\x02 \x01(\x05\x12\x0b\n\x03\x63rv\x18\x03 \x01(\x05\x12\t\n\x01x\x18\x04 \x01(\t\x12\t\n\x01y\x18\x05 \x01(\t\"\x9f\x01\n\x11\x43redentialRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12*\n\npublic_key\x18\x02 \x01(\x0b\x32\x16.credentials.PublicKey\x12\x12\n\nsign_count\x18\x03 \x01(\x05\x12\x12\n\ntransports\x18\x04 \x01(\t\x12\x0e\n\x06\x61\x61guid\x18\x05 \x01(\t\x12\x15\n\rcredential_id\x18\x06 \x01(\t\"%\n\x12\x43redentialResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\xb3\x01\n\x11\x43redentialService\x12R\n\x0fStoreCredential\x12\x1e.credentials.CredentialRequest\x1a\x1f.credentials.CredentialResponse\x12J\n\x07\x41uthChk\x12\x1e.credentials.CredentialRequest\x1a\x1f.credentials.CredentialResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'credentials_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PUBLICKEY']._serialized_start=34
  _globals['_PUBLICKEY']._serialized_end=106
  _globals['_CREDENTIALREQUEST']._serialized_start=109
  _globals['_CREDENTIALREQUEST']._serialized_end=268
  _globals['_CREDENTIALRESPONSE']._serialized_start=270
  _globals['_CREDENTIALRESPONSE']._serialized_end=307
  _globals['_CREDENTIALSERVICE']._serialized_start=310
  _globals['_CREDENTIALSERVICE']._serialized_end=489
# @@protoc_insertion_point(module_scope)
