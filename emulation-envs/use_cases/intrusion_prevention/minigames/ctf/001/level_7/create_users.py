import os
from pycr_common.dao.container_config.users_config import UsersConfig
from pycr_common.dao.container_config.node_users_config import NodeUsersConfig
from pycr_common.util.experiments_util import util
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.config.generator.users_generator import UsersGenerator
import pycr_common.constants.constants as constants


def default_users() -> UsersConfig:
    """
    :return: the UsersConfig of the emulation
    """
    users = [
        NodeUsersConfig(ip="172.18.7.191", users=[
            ("agent", "agent", True)
        ]),
        NodeUsersConfig(ip="172.18.7.21", users=[
            ("admin", "admin31151x", True),
            ("test", "qwerty", True),
            ("oracle", "abc123", False)
        ]),
        NodeUsersConfig(ip="172.18.7.10", users=[
            ("admin", "admin1235912", True),
            ("jessica", "water", False)
        ]),
        NodeUsersConfig(ip="172.18.7.2", users=[
            ("admin", "test32121", True),
            ("user1", "123123", True)
        ]),
        NodeUsersConfig(ip="172.18.7.3", users=[
            ("john", "doe", True),
            ("vagrant", "test_pw1", False)
        ]),
        NodeUsersConfig(ip="172.18.7.19", users=[
            ("karl", "gustaf", True),
            ("steven", "carragher", False)
        ]),
        NodeUsersConfig(ip="172.18.7.31", users=[
            ("stefan", "zweig", True)
        ]),
        NodeUsersConfig(ip="172.18.7.42", users=[
            ("roy", "neruda", True)
        ]),
        NodeUsersConfig(ip="172.18.7.37", users=[
            ("john", "conway", True)
        ]),
        NodeUsersConfig(ip="172.18.7.82", users=[
            ("john", "nash", True)
        ]),
        NodeUsersConfig(ip="172.18.7.75", users=[
            ("larry", "samuelson", True)
        ]),
        NodeUsersConfig(ip="172.18.7.71", users=[
            ("robbins", "monro", True)
        ]),
        NodeUsersConfig(ip="172.18.7.11", users=[
            ("rich", "sutton", True)
        ])
    ]
    users_conf = UsersConfig(users=users)
    return users_conf

# Generates the users.json configuration file
if __name__ == '__main__':
    if not os.path.exists(util.default_users_path()):
        UsersGenerator.write_users_config(default_users())
    users_config = util.read_users_config(util.default_users_path())
    emulation_config = EmulationConfig(agent_ip="172.18.7.191", agent_username=constants.PYCR_ADMIN.USER,
                                     agent_pw=constants.PYCR_ADMIN.PW, server_connection=False)
    UsersGenerator.create_users(users_config=users_config, emulation_config=emulation_config)