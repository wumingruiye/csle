# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cluster_manager.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x63luster_manager.proto\"\x12\n\x10GetNodeStatusMsg\"\xb3\x02\n\rNodeStatusDTO\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0e\n\x06leader\x18\x02 \x01(\x08\x12\x17\n\x0f\x63\x41\x64visorRunning\x18\x03 \x01(\x08\x12\x19\n\x11prometheusRunning\x18\x04 \x01(\x08\x12\x16\n\x0egrafanaRunning\x18\x05 \x01(\x08\x12\x16\n\x0epgAdminRunning\x18\x06 \x01(\x08\x12\x14\n\x0cnginxRunning\x18\x07 \x01(\x08\x12\x14\n\x0c\x66laskRunning\x18\x08 \x01(\x08\x12!\n\x19\x64ockerStatsManagerRunning\x18\t \x01(\x08\x12\x1b\n\x13nodeExporterRunning\x18\n \x01(\x08\x12\x19\n\x11postgreSQLRunning\x18\x0b \x01(\x08\x12\x1b\n\x13\x64ockerEngineRunning\x18\x0c \x01(\x08\"#\n\x10ServiceStatusDTO\x12\x0f\n\x07running\x18\x01 \x01(\x08\"\x14\n\x12StartPostgreSQLMsg\"\x12\n\x10StartCAdvisorMsg\"\x16\n\x14StartNodeExporterMsg\"\x11\n\x0fStartGrafanaMsg\"\x14\n\x12StartPrometheusMsg\"\x11\n\x0fStartPgAdminMsg\"\x0f\n\rStartNginxMsg\"\x0f\n\rStartFlaskMsg\"\x1c\n\x1aStartDockerStatsManagerMsg\"\x16\n\x14StartDockerEngineMsg\"\x13\n\x11StopPostgreSQLMsg\"\x11\n\x0fStopCAdvisorMsg\"\x15\n\x13StopNodeExporterMsg\"\x10\n\x0eStopGrafanaMsg\"\x13\n\x11StopPrometheusMsg\"\x10\n\x0eStopPgAdminMsg\"\x0e\n\x0cStopNginxMsg\"\x0e\n\x0cStopFlaskMsg\"\x1b\n\x19StopDockerStatsManagerMsg\"\x15\n\x13StopDockerEngineMsg2\xde\t\n\x0e\x43lusterManager\x12\x34\n\rgetNodeStatus\x12\x11.GetNodeStatusMsg\x1a\x0e.NodeStatusDTO\"\x00\x12;\n\x0fstartPostgreSQL\x12\x13.StartPostgreSQLMsg\x1a\x11.ServiceStatusDTO\"\x00\x12\x37\n\rstartCAdvisor\x12\x11.StartCAdvisorMsg\x1a\x11.ServiceStatusDTO\"\x00\x12?\n\x11startNodeExporter\x12\x15.StartNodeExporterMsg\x1a\x11.ServiceStatusDTO\"\x00\x12\x35\n\x0cstartGrafana\x12\x10.StartGrafanaMsg\x1a\x11.ServiceStatusDTO\"\x00\x12;\n\x0fstartPrometheus\x12\x13.StartPrometheusMsg\x1a\x11.ServiceStatusDTO\"\x00\x12\x35\n\x0cstartPgAdmin\x12\x10.StartPgAdminMsg\x1a\x11.ServiceStatusDTO\"\x00\x12\x31\n\nstartNginx\x12\x0e.StartNginxMsg\x1a\x11.ServiceStatusDTO\"\x00\x12\x31\n\nstartFlask\x12\x0e.StartFlaskMsg\x1a\x11.ServiceStatusDTO\"\x00\x12K\n\x17startDockerStatsManager\x12\x1b.StartDockerStatsManagerMsg\x1a\x11.ServiceStatusDTO\"\x00\x12?\n\x11startDockerEngine\x12\x15.StartDockerEngineMsg\x1a\x11.ServiceStatusDTO\"\x00\x12\x39\n\x0estopPostgreSQL\x12\x12.StopPostgreSQLMsg\x1a\x11.ServiceStatusDTO\"\x00\x12\x35\n\x0cstopCAdvisor\x12\x10.StopCAdvisorMsg\x1a\x11.ServiceStatusDTO\"\x00\x12=\n\x10stopNodeExporter\x12\x14.StopNodeExporterMsg\x1a\x11.ServiceStatusDTO\"\x00\x12\x33\n\x0bstopGrafana\x12\x0f.StopGrafanaMsg\x1a\x11.ServiceStatusDTO\"\x00\x12\x39\n\x0estopPrometheus\x12\x12.StopPrometheusMsg\x1a\x11.ServiceStatusDTO\"\x00\x12\x33\n\x0bstopPgAdmin\x12\x0f.StopPgAdminMsg\x1a\x11.ServiceStatusDTO\"\x00\x12/\n\tstopNginx\x12\r.StopNginxMsg\x1a\x11.ServiceStatusDTO\"\x00\x12/\n\tstopFlask\x12\r.StopFlaskMsg\x1a\x11.ServiceStatusDTO\"\x00\x12I\n\x16stopDockerStatsManager\x12\x1a.StopDockerStatsManagerMsg\x1a\x11.ServiceStatusDTO\"\x00\x12=\n\x10stopDockerEngine\x12\x14.StopDockerEngineMsg\x1a\x11.ServiceStatusDTO\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cluster_manager_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETNODESTATUSMSG._serialized_start=25
  _GETNODESTATUSMSG._serialized_end=43
  _NODESTATUSDTO._serialized_start=46
  _NODESTATUSDTO._serialized_end=353
  _SERVICESTATUSDTO._serialized_start=355
  _SERVICESTATUSDTO._serialized_end=390
  _STARTPOSTGRESQLMSG._serialized_start=392
  _STARTPOSTGRESQLMSG._serialized_end=412
  _STARTCADVISORMSG._serialized_start=414
  _STARTCADVISORMSG._serialized_end=432
  _STARTNODEEXPORTERMSG._serialized_start=434
  _STARTNODEEXPORTERMSG._serialized_end=456
  _STARTGRAFANAMSG._serialized_start=458
  _STARTGRAFANAMSG._serialized_end=475
  _STARTPROMETHEUSMSG._serialized_start=477
  _STARTPROMETHEUSMSG._serialized_end=497
  _STARTPGADMINMSG._serialized_start=499
  _STARTPGADMINMSG._serialized_end=516
  _STARTNGINXMSG._serialized_start=518
  _STARTNGINXMSG._serialized_end=533
  _STARTFLASKMSG._serialized_start=535
  _STARTFLASKMSG._serialized_end=550
  _STARTDOCKERSTATSMANAGERMSG._serialized_start=552
  _STARTDOCKERSTATSMANAGERMSG._serialized_end=580
  _STARTDOCKERENGINEMSG._serialized_start=582
  _STARTDOCKERENGINEMSG._serialized_end=604
  _STOPPOSTGRESQLMSG._serialized_start=606
  _STOPPOSTGRESQLMSG._serialized_end=625
  _STOPCADVISORMSG._serialized_start=627
  _STOPCADVISORMSG._serialized_end=644
  _STOPNODEEXPORTERMSG._serialized_start=646
  _STOPNODEEXPORTERMSG._serialized_end=667
  _STOPGRAFANAMSG._serialized_start=669
  _STOPGRAFANAMSG._serialized_end=685
  _STOPPROMETHEUSMSG._serialized_start=687
  _STOPPROMETHEUSMSG._serialized_end=706
  _STOPPGADMINMSG._serialized_start=708
  _STOPPGADMINMSG._serialized_end=724
  _STOPNGINXMSG._serialized_start=726
  _STOPNGINXMSG._serialized_end=740
  _STOPFLASKMSG._serialized_start=742
  _STOPFLASKMSG._serialized_end=756
  _STOPDOCKERSTATSMANAGERMSG._serialized_start=758
  _STOPDOCKERSTATSMANAGERMSG._serialized_end=785
  _STOPDOCKERENGINEMSG._serialized_start=787
  _STOPDOCKERENGINEMSG._serialized_end=808
  _CLUSTERMANAGER._serialized_start=811
  _CLUSTERMANAGER._serialized_end=2057
# @@protoc_insertion_point(module_scope)