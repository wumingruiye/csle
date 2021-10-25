from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.dao.network.env_mode import EnvMode
from pycr_common.dao.container_config.containers_config import ContainersConfig
from pycr_common.dao.container_config.flags_config import FlagsConfig
from pycr_common.envs_model.logic.exploration.random_exploration_policy import RandomExplorationPolicy
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs_model.config.random.pycr_ctf_random_base import PyCrCTFRandomBase
from gym_pycr_ctf.envs_model.config.random.pycr_ctf_random_v1 import PyCrCTFRandomV1
from gym_pycr_ctf.envs_model.config.random.pycr_ctf_random_v2 import PyCrCTFRandomV2
from gym_pycr_ctf.envs_model.config.random.pycr_ctf_random_v3 import PyCrCTFRandomV3
from gym_pycr_ctf.envs_model.config.random.pycr_ctf_random_v4 import PyCrCTFRandomV4


# -------- Version 1 Generated Sim ------------
class PyCRCTFRandomGeneratedSim1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV1.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV1.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV1.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_max_exploration_steps = 500
            env_config.attacker_max_exploration_trajectories = 10
            env_config.max_episode_length = 100
            env_config.attacker_alerts_coefficient = 0
            env_config.attacker_cost_coefficient = 0
            env_config.attacker_base_step_reward = -1
            env_config.use_upper_bound_pi_star_attacker = False
            env_config.detection_alerts_threshold = -1
            env_config.emulate_detection = True
            env_config.detection_prob_factor = 0.05
            env_config.randomize_attacker_starting_state = False
        super(PyCRCTFRandomGeneratedSim1Env, self).__init__(env_config=env_config)


# -------- Version 1 Generated Sim With Costs ------------
class PyCRCTFRandomGeneratedSimWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV1.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV1.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV1.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 100
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_exploration_filter_illegal = True
        super(PyCRCTFRandomGeneratedSimWithCosts1Env, self).__init__(env_config=env_config)


# -------- Version 2 Generated Sim ------------
class PyCRCTFRandomGeneratedSim2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV2.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV2.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV2.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_exploration_filter_illegal = True
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
        super(PyCRCTFRandomGeneratedSim2Env, self).__init__(env_config=env_config)


# -------- Version 2 Generated Sim With Costs ------------
class PyCRCTFRandomGeneratedSimWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV2.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV2.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV2.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_filter_illegal = True
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
        super(PyCRCTFRandomGeneratedSimWithCosts2Env, self).__init__(env_config=env_config)


# -------- Version 3, Generated Simulation ------------
class PyCRCTFRandomGeneratedSim3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV3.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV3.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV3.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_filter_illegal = True
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
        super(PyCRCTFRandomGeneratedSim3Env, self).__init__(env_config=env_config)


# -------- Version 3, Generated Simulation With Costs ------------
class PyCRCTFRandomGeneratedSimWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV3.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV3.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV3.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes-1)
            env_config.attacker_cost_coefficient = 1
            env_config.attacker_alerts_coefficient = 1
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_filter_illegal = True
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
        super(PyCRCTFRandomGeneratedSimWithCosts3Env, self).__init__(env_config=env_config)


# -------- Version 4, Generated Simulation ------------
class PyCRCTFRandomGeneratedSim4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """

    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir: str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes: int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV4.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV4.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV4.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes - 1)
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.attacker_exploration_filter_illegal = True
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
        super(PyCRCTFRandomGeneratedSim4Env, self).__init__(env_config=env_config)


# -------- Version 4, Generated Simulation, With Costs------------
class PyCRCTFRandomGeneratedSimWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """

    def __init__(self, env_config: EnvConfig, emulation_config: EmulationConfig, checkpoint_dir: str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes: int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrCTFRandomBase.render_conf(containers_config=containers_config)
            if emulation_config is None:
                raise ValueError("emulation config cannot be None")
            emulation_config.ids_router = containers_config.ids_enabled
            emulation_config.ids_router_ip = containers_config.router_ip
            attacker_action_conf = PyCrCTFRandomV4.attacker_actions_conf(num_nodes=num_nodes - 1,
                                                                subnet_mask=containers_config.subnet_mask,
                                                                hacker_ip=containers_config.agent_ip)
            defender_action_conf = PyCrCTFRandomV4.defender_actions_conf(
                num_nodes=num_nodes - 1, subnet_mask=containers_config.subnet_mask)
            env_config = PyCrCTFRandomV4.env_config(containers_config=containers_config,
                                                    flags_config=flags_config,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config,
                                                    num_nodes=num_nodes - 1)
            env_config.attacker_cost_coefficient = 1
            env_config.attacker_alerts_coefficient = 1
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions)
            env_config.attacker_exploration_filter_illegal = True
            env_config.attacker_exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 50
            env_config.compute_pi_star_attacker = False
            env_config.use_upper_bound_pi_star_attacker = True
        super(PyCRCTFRandomGeneratedSimWithCosts4Env, self).__init__(env_config=env_config)