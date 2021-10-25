import pycr_common.constants.constants as constants
from pycr_common.dao.observation.common.port_observation_state import PortObservationState
from pycr_common.dao.action_results.nmap_port_status import NmapPortStatus
from pycr_common.dao.network.transport_protocol import TransportProtocol
from pycr_common.dao.action_results.nmap_http_enum import NmapHttpEnum
from pycr_common.dao.action_results.nmap_http_grep import NmapHttpGrep
from pycr_common.dao.action_results.nmap_vulscan import NmapVulscan


class NmapPort:
    """
    DTO Representing a Port found with a NMAP scan
    """

    def __init__(self, port_id: int, protocol : TransportProtocol, status: NmapPortStatus = NmapPortStatus.DOWN,
                 service_name : str = "none", http_enum: NmapHttpEnum = None,
                 http_grep: NmapHttpGrep = None, vulscan: NmapVulscan = None, service_version : str = "",
                 service_fp : str = ""):
        """
        Initializes the DTO

        :param port_id: the id of the port found
        :param protocol: the protocol of the port
        :param status: the status of the port
        :param service_name: the service running on the port
        :param http_enum: the http enum output
        :param http_grep: the http grep output
        :param vulscan: the vulscan output
        :param service_version: the service version
        :param service_fp: the service fp
        """
        self.port_id = port_id
        self.protocol = protocol
        self.status = status
        self.service_name = service_name
        self.http_enum = http_enum
        self.http_grep = http_grep
        self.vulscan = vulscan
        self.service_version = service_version
        self.service_fp = service_fp

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "port_id:{}, protocol:{}, status:{}, service_name:{}, http_enum:{}, http_grep:{}, vulscan:{}, " \
               "service_version:{}, service_fp:{}".format(
            self.port_id, self.protocol, self.status, self.service_name, self.http_enum, self.http_grep, self.vulscan,
        self.service_version, self.service_fp)

    def __hash__(self) -> int:
        """
        :return: a hash of the object
        """
        return hash(self.port_id)

    def __eq__(self, other) -> bool:
        """
        Compares equality of the object with another object

        :param other: the object to compare with
        :return: True if equal otherwise False
        """
        return (self.port_id == other.port_id)

    def to_obs(self) -> PortObservationState:
        """
        Converts the object into a PortObservationState

        :return: the created PortObservationState
        """
        open = self.status == NmapPortStatus.UP
        if self.service_name not in constants.SERVICES.service_lookup:
            self.service_name = "unknown"
        hp_enum = ""
        if self.http_enum is not None:
            hp_enum = self.http_enum.output
        hp_grep = ""
        if self.http_grep is not None:
            hp_grep = self.http_grep.output
        vulscan = ""
        if self.vulscan is not None:
            vulscan = self.vulscan.output
        port_obs = PortObservationState(port = self.port_id, open=open, service=self.service_name,
                                        protocol=self.protocol, http_enum=hp_enum,
                                        http_grep=hp_grep, vulscan=vulscan, version=self.service_version,
                                        fingerprint=self.service_fp)
        return port_obs