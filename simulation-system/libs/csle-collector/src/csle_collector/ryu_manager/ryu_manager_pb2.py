# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ryu_manager.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11ryu_manager.proto\"\x0c\n\nStopRyuMsg\"A\n\x0bStartRyuMsg\x12\x0c\n\x04port\x18\x01 \x01(\x05\x12\x10\n\x08web_port\x18\x02 \x01(\x05\x12\x12\n\ncontroller\x18\x03 \x01(\t\"\x13\n\x11StopRyuMonitorMsg\"Q\n\x12StartRyuMonitorMsg\x12\x10\n\x08kafka_ip\x18\x01 \x01(\t\x12\x12\n\nkafka_port\x18\x02 \x01(\x05\x12\x15\n\rtime_step_len\x18\x03 \x01(\x05\"\x11\n\x0fGetRyuStatusMsg\"\xa7\x01\n\x06RyuDTO\x12\x13\n\x0bryu_running\x18\x01 \x01(\x08\x12\x17\n\x0fmonitor_running\x18\x02 \x01(\x08\x12\x0c\n\x04port\x18\x03 \x01(\x05\x12\x10\n\x08web_port\x18\x04 \x01(\x05\x12\x12\n\ncontroller\x18\x05 \x01(\t\x12\x10\n\x08kafka_ip\x18\x06 \x01(\t\x12\x12\n\nkafka_port\x18\x07 \x01(\x05\x12\x15\n\rtime_step_len\x18\x08 \x01(\x05\x32\xe5\x01\n\nRyuManager\x12+\n\x0cgetRyuStatus\x12\x10.GetRyuStatusMsg\x1a\x07.RyuDTO\"\x00\x12!\n\x07stopRyu\x12\x0b.StopRyuMsg\x1a\x07.RyuDTO\"\x00\x12#\n\x08startRyu\x12\x0c.StartRyuMsg\x1a\x07.RyuDTO\"\x00\x12/\n\x0estopRyuMonitor\x12\x12.StopRyuMonitorMsg\x1a\x07.RyuDTO\"\x00\x12\x31\n\x0fstartRyuMonitor\x12\x13.StartRyuMonitorMsg\x1a\x07.RyuDTO\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ryu_manager_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STOPRYUMSG._serialized_start=21
  _STOPRYUMSG._serialized_end=33
  _STARTRYUMSG._serialized_start=35
  _STARTRYUMSG._serialized_end=100
  _STOPRYUMONITORMSG._serialized_start=102
  _STOPRYUMONITORMSG._serialized_end=121
  _STARTRYUMONITORMSG._serialized_start=123
  _STARTRYUMONITORMSG._serialized_end=204
  _GETRYUSTATUSMSG._serialized_start=206
  _GETRYUSTATUSMSG._serialized_end=223
  _RYUDTO._serialized_start=226
  _RYUDTO._serialized_end=393
  _RYUMANAGER._serialized_start=396
  _RYUMANAGER._serialized_end=625
# @@protoc_insertion_point(module_scope)
