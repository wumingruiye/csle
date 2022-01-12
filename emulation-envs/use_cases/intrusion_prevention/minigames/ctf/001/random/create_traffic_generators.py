from pycr_common.util.experiments_util import util
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.config.generator.traffic_generator import TrafficGenerator
import pycr_common.constants.constants as constants


def apply_config() -> None:
    """
    Applies the users config
    """
    containers_config = util.read_containers_config(util.default_containers_path())
    traffic_config = util.read_traffic_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip=containers_config.agent_ip, agent_username=constants.PYCR_ADMIN.USER,
                                       agent_pw=constants.PYCR_ADMIN.PW, server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, emulation_config=emulation_config,
                                            sleep_time=1)

#Applies the users config
if __name__ == '__main__':
    apply_config()