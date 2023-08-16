"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class StopDockerStatsMonitorMsg(google.protobuf.message.Message):
    """Message that the client sends to stop the docker stats monitor"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EMULATION_FIELD_NUMBER: builtins.int
    EXECUTION_FIRST_IP_OCTET_FIELD_NUMBER: builtins.int
    emulation: builtins.str
    execution_first_ip_octet: builtins.int
    def __init__(
        self,
        *,
        emulation: builtins.str = ...,
        execution_first_ip_octet: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["emulation", b"emulation", "execution_first_ip_octet", b"execution_first_ip_octet"]) -> None: ...

global___StopDockerStatsMonitorMsg = StopDockerStatsMonitorMsg

@typing_extensions.final
class ContainerIp(google.protobuf.message.Message):
    """DTO representing a pair of ip and container name"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    IP_FIELD_NUMBER: builtins.int
    CONTAINER_FIELD_NUMBER: builtins.int
    ip: builtins.str
    container: builtins.str
    def __init__(
        self,
        *,
        ip: builtins.str = ...,
        container: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["container", b"container", "ip", b"ip"]) -> None: ...

global___ContainerIp = ContainerIp

@typing_extensions.final
class StartDockerStatsMonitorMsg(google.protobuf.message.Message):
    """Message that the client sends to start the docker stats monitor"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EMULATION_FIELD_NUMBER: builtins.int
    EXECUTION_FIRST_IP_OCTET_FIELD_NUMBER: builtins.int
    KAFKA_IP_FIELD_NUMBER: builtins.int
    STATS_QUEUE_MAXSIZE_FIELD_NUMBER: builtins.int
    TIME_STEP_LEN_SECONDS_FIELD_NUMBER: builtins.int
    KAFKA_PORT_FIELD_NUMBER: builtins.int
    CONTAINERS_FIELD_NUMBER: builtins.int
    emulation: builtins.str
    execution_first_ip_octet: builtins.int
    kafka_ip: builtins.str
    stats_queue_maxsize: builtins.int
    time_step_len_seconds: builtins.int
    kafka_port: builtins.int
    @property
    def containers(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ContainerIp]: ...
    def __init__(
        self,
        *,
        emulation: builtins.str = ...,
        execution_first_ip_octet: builtins.int = ...,
        kafka_ip: builtins.str = ...,
        stats_queue_maxsize: builtins.int = ...,
        time_step_len_seconds: builtins.int = ...,
        kafka_port: builtins.int = ...,
        containers: collections.abc.Iterable[global___ContainerIp] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["containers", b"containers", "emulation", b"emulation", "execution_first_ip_octet", b"execution_first_ip_octet", "kafka_ip", b"kafka_ip", "kafka_port", b"kafka_port", "stats_queue_maxsize", b"stats_queue_maxsize", "time_step_len_seconds", b"time_step_len_seconds"]) -> None: ...

global___StartDockerStatsMonitorMsg = StartDockerStatsMonitorMsg

@typing_extensions.final
class GetDockerStatsMonitorStatusMsg(google.protobuf.message.Message):
    """Message that the client sends to extract the status of the docker stats monitor"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___GetDockerStatsMonitorStatusMsg = GetDockerStatsMonitorStatusMsg

@typing_extensions.final
class DockerStatsMonitorDTO(google.protobuf.message.Message):
    """Message that the server returns when requested by the client, contains info about the docker stats monitor"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NUM_MONITORS_FIELD_NUMBER: builtins.int
    EMULATIONS_FIELD_NUMBER: builtins.int
    EMULATION_EXECUTIONS_FIELD_NUMBER: builtins.int
    num_monitors: builtins.int
    @property
    def emulations(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def emulation_executions(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        num_monitors: builtins.int = ...,
        emulations: collections.abc.Iterable[builtins.str] | None = ...,
        emulation_executions: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["emulation_executions", b"emulation_executions", "emulations", b"emulations", "num_monitors", b"num_monitors"]) -> None: ...

global___DockerStatsMonitorDTO = DockerStatsMonitorDTO