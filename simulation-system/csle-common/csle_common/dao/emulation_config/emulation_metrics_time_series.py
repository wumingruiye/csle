from typing import List, Dict, Any
from csle_collector.ids_manager.alert_counters import AlertCounters
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.docker_stats_manager.docker_stats import DockerStats
from csle_collector.host_manager.host_metrics import HostMetrics
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig


class EmulationMetricsTimeSeries:
    """
    DTO containing time series data from the emulation
    """

    def __init__(self, client_metrics: List[ClientPopulationMetrics], aggregated_docker_stats: List[DockerStats],
                 docker_host_stats: Dict[str, List[DockerStats]], host_metrics: Dict[str, List[HostMetrics]],
                 aggregated_host_metrics: List[HostMetrics],
                 defender_actions: List[EmulationDefenderAction], attacker_actions: List[EmulationAttackerAction],
                 ids_metrics: List[AlertCounters], emulation_env_config: EmulationEnvConfig):
        """
        Initializes the DTO

        :param client_metrics: Time series data with information about the client population
        :param aggregated_docker_stats: Time series data with average docker statistics
        :param docker_host_stats: Time series data with docker statistics per host
        :param host_metrics: Time series data with general host metrics
        :param aggregated_host_metrics: Time series data with aggregated host metrics
        :param defender_actions: Time series data with defender actions
        :param attacker_actions: Time series data with attacker actions
        :param ids_metrics: Time series data with IDS metrics
        :param emulation_env_config: the emulation config
        """
        self.client_metrics = client_metrics
        self.aggregated_docker_stats = aggregated_docker_stats
        self.docker_host_stats = docker_host_stats
        self.host_metrics = host_metrics
        self.defender_actions = defender_actions
        self.attacker_actions = attacker_actions
        self.ids_metrics = ids_metrics
        self.aggregated_host_metrics = aggregated_host_metrics
        self.emulation_env_config = emulation_env_config


    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationMetricsTimeSeries":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        docker_host_stats = {}
        for k,v in d["docker_host_stats"].items():
            docker_host_stats[k] = list(map(lambda x: DockerStats.from_dict(x), v))
        host_metrics = {}
        for k,v in d["host_metrics"].items():
            host_metrics[k] = list(map(lambda x: HostMetrics.from_dict(x), v))
        obj = EmulationMetricsTimeSeries(
            client_metrics=list(map(lambda x: ClientPopulationMetrics.from_dict(x), d["client_metrics"])),
            aggregated_docker_stats=list(map(lambda x: DockerStats.from_dict(x), d["aggregated_docker_stats"])),
            docker_host_stats=docker_host_stats,
            host_metrics=host_metrics,
            defender_actions=list(map(lambda x: EmulationDefenderAction.from_dict(x), d["defender_actions"])),
            attacker_actions=list(map(lambda x: EmulationAttackerAction.from_dict(x), d["attacker_actions"])),
            ids_metrics=list(map(lambda x: AlertCounters.from_dict(x), d["ids_metrics"])),
            aggregated_host_metrics=list(map(lambda x: HostMetrics.from_dict(x), d["aggregated_host_metrics"])),
            emulation_env_config=EmulationEnvConfig.from_dict(d["emulation_env_config"])
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["client_metrics"] = list(map(lambda x: x.to_dict(), self.client_metrics))
        d["aggregated_docker_stats"] = list(map(lambda x: x.to_dict(), self.aggregated_docker_stats))
        d["docker_host_stats"] = {}
        for k,v in self.docker_host_stats.items():
            d["docker_host_stats"][k] = list(map(lambda x: x.to_dict(), v))
        d["host_metrics"] = {}
        for k,v in self.host_metrics.items():
            d["host_metrics"][k] = list(map(lambda x: x.to_dict(), v))
        d["defender_actions"] = list(map(lambda x: x.to_dict(), self.defender_actions))
        d["attacker_actions"] = list(map(lambda x: x.to_dict(), self.attacker_actions))
        d["ids_metrics"] = list(map(lambda x: x.to_dict(), self.ids_metrics))
        d["aggregated_host_metrics"] = list(map(lambda x: x.to_dict(), self.aggregated_host_metrics))
        d["emulation_env_config"] = self.emulation_env_config.to_dict()
        return d

    def __str__(self):
        """
        :return: a string representation
        """
        return f"client_metrics: {list(map(lambda x: str(x), self.client_metrics))}," \
               f"aggregated_docker_stats: {list(map(lambda x: str(x), self.aggregated_docker_stats))}," \
               f"docker_host_stats: {list(map(lambda x: str(x), self.docker_host_stats))}," \
               f"host_metrics: {list(map(lambda x: str(x), self.host_metrics))}," \
               f"defender_actions: {list(map(lambda x: str(x), self.defender_actions))}," \
               f"attacker_actions: {list(map(lambda x: str(x), self.attacker_actions))}," \
               f"ids_metrics: {list(map(lambda x: str(x), self.ids_metrics))}," \
               f"aggregated_host_metrics: {list(map(lambda x: str(x), self.aggregated_host_metrics))}," \
               f"config: {self.emulation_env_config}"