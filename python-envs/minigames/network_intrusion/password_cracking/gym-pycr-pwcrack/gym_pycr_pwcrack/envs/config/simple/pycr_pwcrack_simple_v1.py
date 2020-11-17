from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.network.network_config import NetworkConfig
from gym_pycr_pwcrack.dao.render.render_config import RenderConfig
from gym_pycr_pwcrack.dao.network.env_mode import EnvMode
from gym_pycr_pwcrack.dao.action.action_config import ActionConfig
from gym_pycr_pwcrack.dao.action.nmap_actions import NMAPActions
from gym_pycr_pwcrack.dao.action.network_service_actions import NetworkServiceActions
from gym_pycr_pwcrack.dao.action.shell_actions import ShellActions
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.envs.state_representation.state_type import StateType
from gym_pycr_pwcrack.envs.config.simple.pycr_pwcrack_simple_base import PyCrPwCrackSimpleBase

class PyCrPwCrackSimpleV1:
    """
    V1 configuration of level 1 of the PyCrPwCrack environment.
    """

    @staticmethod
    def actions_conf(num_nodes : int, subnet_mask: str, hacker_ip: str = None) -> ActionConfig:
        """
        :param num_nodes: max number of nodes to consider (whole subnetwork in most general case)
        :param subnet_mask: subnet mask of the network
        :param hacker_ip: ip of the agent
        :return: the action config
        """
        actions = []

        # Host actions
        for idx in range(num_nodes):
            actions.append(NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))

        # Subnet actions
        actions.append(NMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes+1, ip=subnet_mask,
                                                        subnet=True))
        actions.append(NMAPActions.NMAP_VULNERS(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(ShellActions.FIND_FLAG(index=num_nodes+1))
        actions.append(NetworkServiceActions.SERVICE_LOGIN(index=num_nodes+1))
        actions.append(
            NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(num_nodes+1, ip=subnet_mask,
                                                         subnet=True))
        actions.append(NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(num_nodes+1, ip=subnet_mask,
                                                                 subnet=True))
        actions.append(NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(num_nodes+1, ip=subnet_mask,
                                                                 subnet=True))

        actions = sorted(actions, key=lambda x: (x.id.value, x.index))
        nmap_action_ids = [
            ActionId.TCP_SYN_STEALTH_SCAN_SUBNET,
            ActionId.NMAP_VULNERS_SUBNET,
            ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST, ActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST, ActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST, ActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET
        ]
        network_service_action_ids = [ActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [ActionId.FIND_FLAG]
        nikto_action_ids = []
        masscan_action_ids = []
        action_config = ActionConfig(num_indices=num_nodes+1, actions=actions, nmap_action_ids=nmap_action_ids,
                                     network_service_action_ids=network_service_action_ids,
                                     shell_action_ids=shell_action_ids, nikto_action_ids=nikto_action_ids,
                                     masscan_action_ids=masscan_action_ids)
        return action_config

    @staticmethod
    def env_config(network_conf : NetworkConfig, action_conf: ActionConfig, cluster_conf: ClusterConfig,
                   render_conf: RenderConfig) -> EnvConfig:
        """
        :param network_conf: the network config
        :param action_conf: the action config
        :param cluster_conf: the cluster config
        :param render_conf: the render config
        :return: The complete environment config
        """
        env_config = EnvConfig(network_conf=network_conf, action_conf=action_conf, num_ports=10, num_vuln=10,
                               num_sh=3, num_nodes = PyCrPwCrackSimpleBase.num_nodes(),
                               render_config=render_conf, env_mode=EnvMode.SIMULATION,
                               cluster_config=cluster_conf,
                               simulate_detection=True, detection_reward=10, base_detection_p=0.05,
                               hacker_ip=PyCrPwCrackSimpleBase.hacker_ip(), state_type=StateType.COMPACT,
                               router_ip=PyCrPwCrackSimpleBase.router_ip())
        env_config.ping_scan_miss_p = 0.00
        env_config.udp_port_scan_miss_p = 0.00
        env_config.syn_stealth_scan_miss_p = 0.00
        env_config.os_scan_miss_p = 0.00
        env_config.vulners_miss_p = 0.00
        env_config.num_flags = 3
        env_config.blacklist_ips = ["172.18.1.1"]

        env_config.flag_found_reward_mult = 1
        env_config.shell_access_found_reward_mult = 1
        env_config.new_tools_installed_reward_mult = 1
        env_config.new_backdoors_installed_reward_mult = 1
        env_config.all_flags_reward = 20
        env_config.base_step_reward = -10
        env_config.final_steps_reward_coefficient = 1
        env_config.illegal_reward_action = -10
        env_config.new_login_reward_mult = 1
        env_config.machine_found_reward_mult = 1
        env_config.new_backdoors_installed_reward_mult = 1
        env_config.new_tools_installed_reward_mult = 1

        env_config.port_found_reward_mult = 0
        env_config.os_found_reward_mult = 0
        env_config.cve_vuln_found_reward_mult = 0
        env_config.osvdb_vuln_found_reward_mult = 0
        env_config.root_found_reward_mult = 0
        env_config.cost_coefficient = 0
        env_config.detection_reward = 0

        return env_config
