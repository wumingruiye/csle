from typing import List
import copy
import datetime
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.dao.observation.common.port_observation_state import PortObservationState
from pycr_common.dao.observation.common.connection_observation_state import ConnectionObservationState
from pycr_common.dao.network.node import Node


class DefenderMachineObservationState:
    """
    Represent's the defender's belief state of a component in the infrastructure
    """

    def __init__(self, ip : str):
        """
        Initializes the DTO

        :param ip: the ip of the machine
        """
        self.ip = ip
        self.os="unknown"
        self.ports : List[PortObservationState] = []
        self.ssh_connections :List[ConnectionObservationState] = []
        self.emulation_config : EmulationConfig = None
        self.num_open_connections = 0
        self.num_failed_login_attempts = 0
        self.num_users = 0
        self.num_logged_in_users = 0
        self.num_login_events = 0
        self.num_processes = 0

        self.num_open_connections_recent = 0
        self.num_failed_login_attempts_recent = 0
        self.num_users_recent = 0
        self.num_logged_in_users_recent = 0
        self.num_login_events_recent = 0
        self.num_processes_recent = 0


        self.failed_auth_last_ts = datetime.datetime.now().timestamp()
        self.login_last_ts = datetime.datetime.now().timestamp()

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{},os:{},num_ports:{},num_ssh_connections:{}," \
               "num_open_connections:{},num_failed_login_attempts:{},num_users:{}," \
               "num_logged_in_users:{},num_login_events:{},num_processes:{}," \
               "failed_auth_last_ts:{},login_last_ts:{},num_open_connections_recent:{}," \
               "num_failed_login_attempts_recent:{},num_users_recent:{},num_logged_in_users_recent:{}," \
               "num_login_events_recent:{},num_processes_recent:{}" \
               "".format(self.ip, self.os, len(self.ports), len(self.ssh_connections),
                         self.num_open_connections, self.num_failed_login_attempts,
                         self.num_failed_login_attempts, self.num_users, self.num_logged_in_users,
                         self.num_login_events, self.num_processes, self.failed_auth_last_ts,
                         self.login_last_ts, self.num_open_connections_recent, self.num_failed_login_attempts_recent,
                         self.num_users_recent, self.num_logged_in_users_recent, self.num_login_events_recent,
                         self.num_processes_recent)

    def sort_ports(self) -> None:
        """
        Sorts the list of ports

        :return: None
        """
        for p in self.ports:
            p.port = int(p.port)
        self.ports = sorted(self.ports, key=lambda x: x.port, reverse=False)

    def cleanup(self) -> None:
        """
        Cleans up environment state. This method is particularly useful in emulation mode where there are
        SSH/Telnet/FTP... connections that should be cleaned up, as well as background threads.

        :return: None
        """
        for c in self.ssh_connections:
            c.cleanup()

    def copy(self) -> "DefenderMachineObservationState":
        """
        :return: a copy of the object
        """
        m_copy = DefenderMachineObservationState(ip=self.ip)
        m_copy.os = self.os
        m_copy.ports = copy.deepcopy(self.ports)
        m_copy.ssh_connections = self.ssh_connections
        m_copy.num_open_connections = self.num_open_connections
        m_copy.num_failed_login_attempts = self.num_failed_login_attempts
        m_copy.num_users = self.num_users
        m_copy.num_logged_in_users = self.num_logged_in_users
        m_copy.num_login_events = self.num_login_events
        m_copy.num_processes = self.num_processes
        m_copy.failed_auth_last_ts = self.failed_auth_last_ts
        m_copy.login_last_ts = self.login_last_ts
        m_copy.num_open_connections_recent = self.num_open_connections_recent
        m_copy.num_failed_login_attempts_recent = self.num_failed_login_attempts_recent
        m_copy.num_users_recent = self.num_users_recent
        m_copy.num_logged_in_users_recent = self.num_login_events_recent
        m_copy.num_login_events_recent = self.num_login_events_recent
        m_copy.num_processes_recent = self.num_processes_recent
        return m_copy


    @staticmethod
    def from_node(node: Node, service_lookup: dict) -> "DefenderMachineObservationState":
        """
        Converts a node to a defender machine observation

        :param service_lookup: a service lookup table
        :return: the defender machine observation
        """
        d_obs = DefenderMachineObservationState(node.ip)
        d_obs.os = node.os
        d_obs.num_flags = len(node.flags)
        d_obs.ports = list(map(lambda x: PortObservationState.from_network_service(x, service_lookup), node.services))
        return d_obs



