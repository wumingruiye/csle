from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from csle_common.dao.container_config.resources_config import ResourcesConfig
from csle_common.envs_model.config.generator.generator_util import GeneratorUtil
from csle_common.util.experiments_util import util
import subprocess


class ResourceConstraintsGenerator:
    """
    A Utility Class for generating resource-constraints configuration files
    """

    @staticmethod
    def apply_resource_constraints(resources_config: ResourcesConfig, emulation_config: EmulationConfig):
        """
        Creates users in an emulation environment according to a specified users-configuration

        :param users_config: the users configuration
        :param emulation_config: the emulation configuration
        :return: None
        """
        if emulation_config.server_connection:
            emulation_config.connect_server()
        for node_resource_config in resources_config.node_resources_configurations:
            ips = node_resource_config.get_ips()
            ip = ips[0]
            print(f"appliying resource constraints on node:{ip}")
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=ip)

            for ip_and_net_config in node_resource_config.ips_and_network_configs:
                _, net_config = ip_and_net_config
                # update cpus and memory
                cmd = f"docker update --memory={node_resource_config.available_memory_gb}G " \
                      f"--cpus={node_resource_config.num_cpus} {node_resource_config.container_name}"
                if emulation_config.server_connection:
                    o,e,_ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.server_conn)
                else:
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

                # delete existing netem rules
                cmd = f"sudo tc qdisc del dev {net_config.interface} root netem"
                o,e,_ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

                # add new netem rule that implements the traffic shaping configuration
                cmd = f"sudo tc qdisc add dev {net_config.interface} root netem " \
                      f"delay {net_config.packet_delay_ms:.6f}ms " \
                      f"{net_config.packet_delay_jitter_ms:.6f}ms " \
                      f"distribution {str(net_config.packet_delay_distribution)} " \
                      f"loss gemodel {net_config.loss_gemodel_p:.6f} " \
                      f"{net_config.loss_gemodel_r:.6f} " \
                      f"{(1 - net_config.loss_gemodel_h):.6f} " \
                      f"{(1 - net_config.loss_gemodel_k):.6f} " \
                      f"duplicate {net_config.packet_duplicate_percentage:.6f}% " \
                      f"{net_config.packet_duplicate_correlation_percentage:.6f}% corrupt " \
                      f"{net_config.packet_corrupt_percentage:.6f}% " \
                      f"reorder {net_config.packet_reorder_percentage:.6f}% " \
                      f"{net_config.packet_reorder_correlation_percentage:.6f}% " \
                      f"gap {net_config.packet_reorder_gap} " \
                      f"rate {net_config.rate_limit_mbit:.6f}mbit " \
                      f"limit {net_config.limit_packets_queue:.6f}"
                o,e,_ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            GeneratorUtil.disconnect_admin(emulation_config=emulation_config)


    @staticmethod
    def write_resources_config(resources_config: ResourcesConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param path: the path to write the configuration to
        :return: None
        """
        path = util.default_resources_path(out_dir=path)
        util.write_resources_config_file(resources_config, path)

