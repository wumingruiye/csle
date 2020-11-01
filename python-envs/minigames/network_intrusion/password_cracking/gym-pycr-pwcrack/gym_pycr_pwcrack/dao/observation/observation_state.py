from typing import List
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_id import ActionId

class ObservationState:

    def __init__(self, num_machines : int, num_ports : int, num_vuln : int, num_sh : int,
                 num_flags : int, catched_flags : int):
        self.num_machines = num_machines
        self.num_ports = num_ports
        self.num_vuln = num_vuln
        self.machines : List[MachineObservationState] = []
        self.detected = False
        self.all_flags = False
        self.num_sh = num_sh
        self.num_flags = num_flags
        self.catched_flags = catched_flags
        self.actions_tried = set()
        self.agent_reachable = set()


    def sort_machines(self):
        self.machines = sorted(self.machines, key=lambda x: int(x.ip.rsplit(".", 1)[-1]), reverse=False)


    def cleanup(self):
        for m in self.machines:
            m.cleanup()


    def get_action_ip(self, a : Action):
        if a.index < len(self.machines) and a.index < self.num_machines:
            self.sort_machines()
            return self.machines[a.index].ip
        return a.ip

    def brute_tried(self, a: Action, m: MachineObservationState):
        if m is not None:
            if (a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET
                or a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST):
                return m.ssh_brute_tried

            if (a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET
                or a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST):
                return m.telnet_brute_tried

            if (a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET
                or a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST):
                return m.ftp_brute_tried

            if (a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET
                or a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST):
                return m.cassandra_brute_tried

            if (a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET
                or a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST):
                return m.irc_brute_tried

            if (a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET
                or a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST):
                return m.mongo_brute_tried

            if (a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET
                or a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST):
                return m.mysql_brute_tried

            if (a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET
                or a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST):
                return m.smtp_brute_tried

            if (a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET
                or a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST):
                return m.postgres_brute_tried
            return False
        else:
            brute_tried = True
            for m2 in self.machines:
                res = self.brute_tried(a=a, m=m2)
                if not res:
                    brute_tried = res
                    break
            return brute_tried
