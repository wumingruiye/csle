import os
from csle_common.dao.container_config.users_config import UsersConfig
from csle_common.dao.container_config.node_users_config import NodeUsersConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.users_generator import UsersGenerator
import csle_common.constants.constants as constants


def default_users(network_id: int = 3) -> UsersConfig:
    """
    :param network_id: the network id
    :return: the UsersConfig of the emulation
    """
    users = [
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191", users=[
            ("agent", "agent", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21", users=[
            ("admin", "admin31151x", True),
            ("test", "qwerty", True),
            ("oracle", "abc123", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10", users=[
            ("admin", "admin1235912", True),
            ("jessica", "water", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2", users=[
            ("admin", "test32121", False),
            ("user1", "123123", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3", users=[
            ("john", "doe", True),
            ("vagrant", "test_pw1", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54", users=[
            ("trent", "xe125@41!341", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101", users=[
            ("zidane", "1b12ha9", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7", users=[
            ("zlatan", "pi12195e", True),
            ("kennedy", "eul1145x", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4", users=[
            ("user1", "1235121", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5", users=[
            ("user2", "1235121", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6", users=[
            ("user3", "1bsae235121", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8", users=[
            ("user4", "1bsae235121", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9", users=[
            ("user5", "1gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178", users=[
            ("user6", "1gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11", users=[
            ("user7", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12", users=[
            ("user8", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13", users=[
            ("user9", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14", users=[
            ("user10", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15", users=[
            ("user11", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16", users=[
            ("user12", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17", users=[
            ("user13", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18", users=[
            ("user14", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19", users=[
            ("user15", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20", users=[
            ("user16", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28", users=[
            ("user17", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22", users=[
            ("user18", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23", users=[
            ("user19", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24", users=[
            ("user20", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25", users=[
            ("user20", "081gxq2", True)
        ])
    ]
    users_conf = UsersConfig(users=users)
    return users_conf


# Generates the users.json configuration file
if __name__ == '__main__':
    network_id = 3
    if not os.path.exists(util.default_users_path()):
        UsersGenerator.write_users_config(default_users(network_id=network_id))
    users_config = util.read_users_config(util.default_users_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                       agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    UsersGenerator.create_users(users_config=users_config, emulation_config=emulation_config)
