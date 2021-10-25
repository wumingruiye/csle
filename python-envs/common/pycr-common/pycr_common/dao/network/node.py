"""
Class representing a node in the network, used for simulations
"""

from typing import List
from pycr_common.dao.network.node_type import NodeType
from pycr_common.dao.network.flag import Flag
from pycr_common.dao.network.vulnerability import Vulnerability
from pycr_common.dao.network.network_service import NetworkService
from pycr_common.dao.network.credential import Credential


class Node:
    """
    DTO class that represents a node in the network
    """

    def __init__(self, ip: str, ip_id: int, id : int, type: NodeType, flags: List[Flag], level : int,
                 vulnerabilities : List[Vulnerability], services : List[NetworkService], os : str,
                 credentials : List[Credential], root_usernames : List[str], visible : bool = True,
                 reachable_nodes: List = None, firewall: bool =  False):
        """
        Initializes the DTO

        :param ip: the ip of the node
        :param ip_id: the id of the node's ip
        :param id: the id of the node
        :param type: the type of the node
        :param flags: the set of flags in the node
        :param level: the level of the node
        :param vulnerabilities: the set of vulnerabilities of the node
        :param services: the set of services of the node
        :param os: the operating system of the node
        :param credentials: the list of credentials of the node
        :param root_usernames: the list of root usernames at the node
        :param visible: whether the node is visible or not
        :param reachable_nodes: the set of nodes reachable from this node
        :param firewall: whether this node has a firewall or not
        """
        self.ip = ip
        self.ip_id = ip_id
        self.id = id
        self.type = type
        self.flags = flags
        self.level = level
        self.vulnerabilities = vulnerabilities
        self.services = services
        self.os = os
        self.credentials = credentials
        self.root_usernames = root_usernames
        self.visible = visible
        self.reachable_nodes = reachable_nodes
        self.firewall = firewall

    def merge(self, other_node: "Node") -> None:
        """
        Merges this node with another node

        :param other_node: the node to merge with
        :return: None
        """
        for fl2 in other_node.flags:
            new_flag = True
            for fl1 in self.flags:
                if fl2.name == fl1.name:
                    new_flag = False
            if new_flag:
                self.flags.append(fl2)

        for vuln2 in other_node.vulnerabilities:
            new_vuln = True
            for vuln1 in self.vulnerabilities:
                if vuln2.name == vuln1.name:
                    new_vuln = False
                    vuln1.credentials = vuln1.credentials + vuln2.credentials
            if new_vuln:
                self.vulnerabilities.append(vuln2)

        for s2 in other_node.services:
            new_service = True
            for s1 in self.services:
                if s2.name == s1.name:
                    new_service = False
                    s1.credentials = s1.credentials + s2.credentials
            if new_service:
                self.services.append(s2)

        for root_user in other_node.root_usernames:
            new_root_user = True
            for root_user2 in self.root_usernames:
                if root_user == root_user2:
                    new_root_user = False
            if new_root_user:
                self.root_usernames.append(root_user)


        for cr2 in other_node.credentials:
            new_credential = True
            for cr1 in self.credentials:
                if cr2.username == cr1.username:
                    new_credential = False
            if new_credential:
                self.credentials.append(cr2)

        self.reachable_nodes = self.reachable_nodes.union(other_node.reachable_nodes)

    def __str__(self) -> str:
        """
        :return: a string representation of the node
        """
        return "ip:{}, ip_id:{}, id:{}, type:{}, flags:{}, level:{}, vulnerabilities:{}, services:{}, os:{}," \
               " credentials:{}, root_usernames:{}, visible:{}, reachable_nodes:{}, firewall:{}".format(
            self.ip, self.ip_id, self.id, self.type, list(map(lambda x: str(x), self.flags)), self.level,
            list(map(lambda x: str(x), self.vulnerabilities)), list(map(lambda x: str(x), self.services)),
            self.os, list(map(lambda x: str(x), self.credentials)), self.root_usernames, self.visible,
            self.reachable_nodes, self.firewall
        )

