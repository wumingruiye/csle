from typing import Dict, Any, List
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.controllers.container_controller import ContainerController
import csle_cluster.cluster_manager.cluster_manager_pb2
import csle_collector.client_manager.client_manager_pb2
import csle_collector.traffic_manager.traffic_manager_pb2
import csle_collector.docker_stats_manager.docker_stats_manager_pb2


class ClusterManagerUtil:
    """
    Class with utility functions related to the cluster manager
    """

    @staticmethod
    def convert_traffic_dto_to_traffic_manager_info_dto(
            traffic_dto: csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO) -> \
            csle_cluster.cluster_manager.cluster_manager_pb2.TrafficManagerInfoDTO:
        """
        Converts a TrafficDTO to a TrafficManagerInfoDTO

        :param traffic_dto: the DTO to convert
        :return: the converted DTO
        """
        return csle_cluster.cluster_manager.cluster_manager_pb2.TrafficManagerInfoDTO(
            running=traffic_dto.running, script=traffic_dto.script)

    @staticmethod
    def get_empty_traffic_managers_info_dto() -> \
            csle_cluster.cluster_manager.cluster_manager_pb2.TrafficManagersInfoDTO:
        """
        :return: an empty TrafficManagersInfoDTO
        """
        return csle_cluster.cluster_manager.cluster_manager_pb2.TrafficManagersInfoDTO(
            ips=[], ports=[], emulationName="", executionId=-1, trafficManagersRunning=[],
            trafficManagersStatuses=[])

    @staticmethod
    def get_empty_client_managers_info_dto() -> csle_cluster.cluster_manager.cluster_manager_pb2.ClientManagersInfoDTO:
        """
        :return: an empty ClientManagersInfoDTO
        """
        return csle_cluster.cluster_manager.cluster_manager_pb2.ClientManagersInfoDTO(
            ips=[], ports=[], emulationName="", executionId=-1, clientManagersRunning=[],
            clientManagersStatuses=[])

    @staticmethod
    def get_empty_get_num_clients_dto() -> csle_cluster.cluster_manager.cluster_manager_pb2.GetNumActiveClientsMsg:
        """
        :return: an empty GetNumClientsDTO
        """
        return csle_cluster.cluster_manager.cluster_manager_pb2.GetNumClientsDTO(
            num_clients=0, client_process_active=False, producer_active=False, clients_time_step_len_seconds=0,
            producer_time_step_len_seconds=0)

    @staticmethod
    def convert_client_dto_to_get_num_clients_dto(
            clients_dto: csle_collector.client_manager.client_manager_pb2.ClientsDTO) -> \
            csle_cluster.cluster_manager.cluster_manager_pb2.GetNumActiveClientsMsg:
        """
        Converts a clients DTO to a GetNumClientsDTO

        :param clients_dto: the clients DTO to convert
        :return: the converted DTO
        """
        return csle_cluster.cluster_manager.cluster_manager_pb2.GetNumClientsDTO(
            num_clients=clients_dto.num_clients,
            client_process_active=clients_dto.client_process_active,
            producer_active=clients_dto.producer_active,
            clients_time_step_len_seconds=clients_dto.clients_time_step_len_seconds,
            producer_time_step_len_seconds=clients_dto.producer_time_step_len_seconds
        )

    @staticmethod
    def node_status_dto_to_dict(node_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.NodeStatusDTO) \
            -> Dict[str, Any]:
        """
        Converts a NodeStatusDTO to a dict

        :param node_status_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["ip"] = node_status_dto.ip
        d["leader"] = node_status_dto.leader
        d["cAdvisorRunning"] = node_status_dto.cAdvisorRunning
        d["prometheusRunning"] = node_status_dto.prometheusRunning
        d["grafanaRunning"] = node_status_dto.grafanaRunning
        d["pgAdminRunning"] = node_status_dto.pgAdminRunning
        d["nginxRunning"] = node_status_dto.nginxRunning
        d["flaskRunning"] = node_status_dto.flaskRunning
        d["dockerStatsManagerRunning"] = node_status_dto.dockerStatsManagerRunning
        d["nodeExporterRunning"] = node_status_dto.nodeExporterRunning
        d["postgreSQLRunning"] = node_status_dto.postgreSQLRunning
        d["dockerEngineRunning"] = node_status_dto.dockerEngineRunning
        return d

    @staticmethod
    def service_status_dto_to_dict(node_status_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ServiceStatusDTO) \
            -> Dict[str, Any]:
        """
        Converts a ServiceStatusDTO to a dict

        :param node_status_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["running"] = node_status_dto.running
        return d

    @staticmethod
    def logs_dto_to_dict(logs_dto: csle_cluster.cluster_manager.cluster_manager_pb2.LogsDTO) \
            -> Dict[str, Any]:
        """
        Converts a LogsDTO to a dict

        :param logs_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["logs"] = list(logs_dto.logs)
        return d

    @staticmethod
    def get_num_clients_dto_to_dict(
            get_num_clients_dto: csle_cluster.cluster_manager.cluster_manager_pb2.GetNumClientsDTO) -> Dict[str, Any]:
        """
        Converts a GetNumClientsDTO to a dict

        :param get_num_clients_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["num_clients"] = get_num_clients_dto.num_clients
        d["client_process_active"] = get_num_clients_dto.client_process_active
        d["producer_active"] = get_num_clients_dto.producer_active
        d["clients_time_step_len_seconds"] = get_num_clients_dto.clients_time_step_len_seconds
        d["producer_time_step_len_seconds"] = get_num_clients_dto.producer_time_step_len_seconds
        return d

    @staticmethod
    def get_active_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        Gets the locally active ips for a given emulation

        :param emulation_env_config: the emulation configuration
        :return: the list of Ips
        """
        running_containers, stopped_containers = ContainerController.list_all_running_containers_in_emulation(
            emulation_env_config=emulation_env_config)
        active_ips = []
        for container in running_containers:
            active_ips = active_ips + container.get_ips()
        active_ips.append(constants.COMMON.LOCALHOST)
        active_ips.append(constants.COMMON.LOCALHOST_127_0_0_1)
        active_ips.append(constants.COMMON.LOCALHOST_127_0_1_1)
        return active_ips

    @staticmethod
    def client_managers_info_dto_to_dict(
            clients_managers_info_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ClientManagersInfoDTO) \
            -> Dict[str, Any]:
        """
        Converts a ClientManagersInfoDTO to a dict

        :param clients_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["ips"] = list(clients_managers_info_dto.ips)
        d["ports"] = list(clients_managers_info_dto.ports)
        d["emulationName"] = clients_managers_info_dto.emulationName
        d["executionId"] = clients_managers_info_dto.executionId
        d["clientManagersRunning"] = list(clients_managers_info_dto.clientManagersRunning)
        d["clientManagersRunning"] = list(map(lambda x: ClusterManagerUtil.get_num_clients_dto_to_dict(x),
                                              list(clients_managers_info_dto.clientManagersRunning)))
        return d

    @staticmethod
    def traffic_manager_info_dto_to_dict(
            traffic_manager_info_dto: csle_cluster.cluster_manager.cluster_manager_pb2.TrafficManagerInfoDTO) \
            -> Dict[str, Any]:
        """
        Converts a TrafficManagerInfoDTO to a dict

        :param traffic_manager_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["running"] = traffic_manager_info_dto.running
        d["script"] = traffic_manager_info_dto.script
        return d

    @staticmethod
    def traffic_managers_info_dto_to_dict(
            traffic_managers_info_dto: csle_cluster.cluster_manager.cluster_manager_pb2.TrafficManagersInfoDTO) \
            -> Dict[str, Any]:
        """
        Converts a TrafficManagersInfoDTO to a dict

        :param traffic_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["ips"] = list(traffic_managers_info_dto.ips)
        d["ports"] = list(traffic_managers_info_dto.ports)
        d["trafficManagersRunning"] = list(traffic_managers_info_dto.trafficManagersRunning)
        d["trafficManagersStatuses"] = list(map(lambda x: ClusterManagerUtil.traffic_manager_info_dto_to_dict(x),
                                                list(traffic_managers_info_dto.trafficManagersStatuses)))
        d["emulationName"] = list(traffic_managers_info_dto.emulationName)
        d["executionId"] = list(traffic_managers_info_dto.executionId)
        return d

    @staticmethod
    def docker_stats_monitor_status_dto_to_dict(
            docker_stats_managers_info_dto: csle_cluster.cluster_manager.
                cluster_manager_pb2.DockerStatsMonitorStatusDTO) -> Dict[str, Any]:
        """
        Converts a DockerStatsMonitorStatusDTO to a dict

        :param docker_stats_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["num_monitors"] = list(docker_stats_managers_info_dto.num_monitors)
        d["emulations"] = list(docker_stats_managers_info_dto.emulations)
        d["emulation_executions"] = list(docker_stats_managers_info_dto.emulation_executions)
        return d

    @staticmethod
    def docker_stats_managers_info_dto_to_dict(
            docker_stats_managers_info_dto: csle_cluster.cluster_manager.cluster_manager_pb2.
                DockerStatsManagersInfoDTO) -> Dict[str, Any]:
        """
        Converts a DockerStatsManagersInfoDTO to a dict

        :param docker_stats_managers_info_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["ips"] = list(docker_stats_managers_info_dto.ips)
        d["ports"] = list(docker_stats_managers_info_dto.ports)
        d["dockerStatsManagersRunning"] = list(docker_stats_managers_info_dto.dockerStatsManagersRunning)
        d["dockerStatsManagersStatuses"] = list(map(lambda x: ClusterManagerUtil.traffic_manager_info_dto_to_dict(x),
                                                    list(docker_stats_managers_info_dto.dockerStatsManagersStatuses)))
        d["emulationName"] = list(docker_stats_managers_info_dto.emulationName)
        d["executionId"] = list(docker_stats_managers_info_dto.executionId)
        return d

    @staticmethod
    def stopped_containers_dto_to_dict(
            stopped_containers_dto_to_dict: csle_cluster.cluster_manager.cluster_manager_pb2.StoppedContainersDTO) \
            -> Dict[str, Any]:
        """
        Converts a StoppedContainersDTO to a dict

        :param stopped_containers_dto_to_dict: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["stoppedContainers"] = list(map(lambda x: ClusterManagerUtil.docker_container_dto_to_dict(x),
                                          list(stopped_containers_dto_to_dict.stoppedContainers)))
        return d

    @staticmethod
    def docker_container_dto_to_dict(
            docker_container_dto_to_dict: csle_cluster.cluster_manager.cluster_manager_pb2.DockerContainerDTO) \
            -> Dict[str, Any]:
        """
        Converts a DockerContainerDTO to a dict

        :param docker_container_dto_to_dict: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["name"] = docker_container_dto_to_dict.name
        d["image"] = docker_container_dto_to_dict.image
        d["ip"] = docker_container_dto_to_dict.ip
        return d

    @staticmethod
    def running_emulations_dto_to_dict(
            running_emulations_dto: csle_cluster.cluster_manager.cluster_manager_pb2.RunningEmulationsDTO) \
            -> Dict[str, Any]:
        """
        Converts a RunningEmulationsDTO to a dict

        :param running_emulations_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["runningEmulations"] = list(running_emulations_dto.runningEmulations)
        return d

    @staticmethod
    def running_containers_dto_to_dict(
            running_containers_dto_to_dict: csle_cluster.cluster_manager.cluster_manager_pb2.RunningContainersDTO) \
            -> Dict[str, Any]:
        """
        Converts a RunningContainersDTO to a dict

        :param running_containers_dto_to_dict: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["runningContainers"] = list(map(lambda x: ClusterManagerUtil.docker_container_dto_to_dict(x),
                                          list(running_containers_dto_to_dict.stoppedContainers)))
        return d

    @staticmethod
    def docker_networks_dto_to_dict(
            docker_networks_dto: csle_cluster.cluster_manager.cluster_manager_pb2.DockerNetworksDTO) \
            -> Dict[str, Any]:
        """
        Converts a DockerNetworksDTO to a dict

        :param docker_networks_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["networks"] = list(docker_networks_dto.networks)
        d["network_ids"] = list(docker_networks_dto.network_ids)
        return d

    @staticmethod
    def container_image_dto_to_dict(
            container_image_dto: csle_cluster.cluster_manager.cluster_manager_pb2.ContainerImageDTO) \
            -> Dict[str, Any]:
        """
        Converts a ContainerImageDTO to a dict

        :param container_image_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["repoTags"] = list(container_image_dto.repoTags)
        d["created"] = list(container_image_dto.created)
        d["os"] = list(container_image_dto.os)
        d["architecture"] = list(container_image_dto.architecture)
        d["size"] = list(container_image_dto.size)
        return d

    @staticmethod
    def container_images_dtos_to_dict(
            container_images_dtos: csle_cluster.cluster_manager.cluster_manager_pb2.ContainerImagesDTO) \
            -> Dict[str, Any]:
        """
        Converts a ContainerImagesDTO to a dict

        :param container_images_dtos: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["images"] = list(map(lambda x: ClusterManagerUtil.container_image_dto_to_dict(x),
                               list(container_images_dtos.images)))
        return d

    @staticmethod
    def convert_docker_stats_monitor_dto(
            monitor_dto: csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO) -> \
            csle_cluster.cluster_manager.cluster_manager_pb2.DockerStatsMonitorStatusDTO:
        """
        Converts a DockerStatsMonitorDTO to a DockerStatsMonitorStatusDTO

        :param monitor_dto: the DTO to convert
        :return: the converted DTO
        """
        return csle_cluster.cluster_manager.cluster_manager_pb2.DockerStatsMonitorStatusDTO(
            num_monitors=monitor_dto.num_monitors, emulations=monitor_dto.emulations,
            emulation_executions=monitor_dto.emulation_executions
        )
