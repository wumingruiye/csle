from typing import List
import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.dynasec_test.dynasec_test_agent import DynaSecTestAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_stopping_actions \
    import EmulationAttackerStoppingActions
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_common.dao.emulation_action.attacker.emulation_attacker_nmap_actions import EmulationAttackerNMAPActions
import csle_system_identification.constants.constants as system_identification_constants

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation_by_name("csle-level9-001")
    simulation_env_config = MetastoreFacade.get_simulation_by_name("csle-stopping-pomdp-defender-002")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}dynasectest_test", title="DynaSecTest test",
        random_seeds=[399],
        agent_type=AgentType.DYNA_SEC_TEST,
        log_every=1,
        hparams={
            agents_constants.COMMON.NUM_NEURONS_PER_HIDDEN_LAYER: HParam(
                value=32, name=agents_constants.COMMON.NUM_NEURONS_PER_HIDDEN_LAYER,
                descr="neurons per hidden layer of the policy network"),
            agents_constants.COMMON.NUM_HIDDEN_LAYERS: HParam(
                value=2, name=agents_constants.COMMON.NUM_HIDDEN_LAYERS,
                descr="number of layers of the policy network"),
            agents_constants.PPO.STEPS_BETWEEN_UPDATES: HParam(
                value=512, name=agents_constants.PPO.STEPS_BETWEEN_UPDATES,
                descr="number of steps in the environment for doing rollouts between policy updates"),
            agents_constants.COMMON.BATCH_SIZE: HParam(value=64, name=agents_constants.COMMON.BATCH_SIZE,
                                                       descr="batch size for updates"),
            agents_constants.COMMON.LEARNING_RATE: HParam(value=0.0005,
                                                          name=agents_constants.COMMON.LEARNING_RATE,
                                                          descr="learning rate for updating the policy"),
            agents_constants.COMMON.DEVICE: HParam(value="cpu",
                                                   name=agents_constants.COMMON.DEVICE,
                                                   descr="the device to train on (cpu or cuda:x)"),
            agents_constants.COMMON.NUM_PARALLEL_ENVS: HParam(value=50,
                                                              name=agents_constants.COMMON.NUM_PARALLEL_ENVS,
                                                              descr="the nunmber of parallel environments for training"),
            agents_constants.COMMON.GAMMA: HParam(
                value=1, name=agents_constants.COMMON.GAMMA, descr="the discount factor"),
            agents_constants.PPO.GAE_LAMBDA: HParam(
                value=0.95, name=agents_constants.PPO.GAE_LAMBDA, descr="the GAE weighting term"),
            agents_constants.PPO.CLIP_RANGE: HParam(
                value=0.2, name=agents_constants.PPO.CLIP_RANGE, descr="the clip range for PPO"),
            agents_constants.PPO.CLIP_RANGE_VF: HParam(
                value=None, name=agents_constants.PPO.CLIP_RANGE_VF,
                descr="the clip range for PPO-update of the value network"),
            agents_constants.PPO.ENT_COEF: HParam(
                value=0.0, name=agents_constants.PPO.ENT_COEF,
                descr="the entropy coefficient for exploration"),
            agents_constants.PPO.VF_COEF: HParam(value=0.5, name=agents_constants.PPO.VF_COEF,
                                                 descr="the coefficient of the value network for the loss"),
            agents_constants.PPO.MAX_GRAD_NORM: HParam(
                value=0.5, name=agents_constants.PPO.MAX_GRAD_NORM, descr="the maximum allows gradient norm"),
            agents_constants.PPO.TARGET_KL: HParam(value=None,
                                                   name=agents_constants.PPO.TARGET_KL,
                                                   descr="the target kl"),
            agents_constants.COMMON.NUM_TRAINING_TIMESTEPS: HParam(
                value=int(150000), name=agents_constants.COMMON.NUM_TRAINING_TIMESTEPS,
                descr="number of timesteps to train"),
            agents_constants.COMMON.EVAL_EVERY: HParam(value=1, name=agents_constants.COMMON.EVAL_EVERY,
                                                       descr="training iterations between evaluations"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=10, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="the batch size for evaluation"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=10000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=10, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.L: HParam(value=3, name=agents_constants.COMMON.L,
                                              descr="the number of stop actions"),
            agents_constants.DYNASEC.INTRUSION_START_P: HParam(
                value=0.4, name=agents_constants.DYNASEC.INTRUSION_START_P,
                descr="the p parameter for the geometric distribution of the intrusion start time"),
            agents_constants.DYNASEC.EMULATION_TRACES_TO_SAVE_W_DATA_COLLECTION_JOB: HParam(
                value=1, name=agents_constants.DYNASEC.EMULATION_TRACES_TO_SAVE_W_DATA_COLLECTION_JOB,
                descr="number of traces to cache with each data collection job"),
            agents_constants.DYNASEC.SLEEP_TIME: HParam(
                value=30, name=agents_constants.DYNASEC.SLEEP_TIME,
                descr="sleep time for data collection processes"),
            agents_constants.DYNASEC.TRAINING_EPOCHS: HParam(
                value=10000, name=agents_constants.DYNASEC.TRAINING_EPOCHS,
                descr="the number of training epochs of dynasec"),
            agents_constants.DYNASEC.WARMUP_EPISODES: HParam(
                value=2, name=agents_constants.DYNASEC.WARMUP_EPISODES,
                descr="the number of warmup episodes in dynasec"),
            agents_constants.DYNASEC.EMULATION_MONITOR_SLEEP_TIME: HParam(
                value=1, name=agents_constants.DYNASEC.EMULATION_MONITOR_SLEEP_TIME,
                descr="the sleep time of the emulation monitor (minutes)"),
            agents_constants.DYNASEC.REPLAY_WINDOW_SIZE: HParam(
                value=20, name=agents_constants.DYNASEC.REPLAY_WINDOW_SIZE,
                descr="the replay window size for DynaSec (unit: episodes)")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    simulation_env_config.simulation_env_input_config.attacker_strategy = TabularPolicy(
        player_type=PlayerType.ATTACKER,
        actions=simulation_env_config.joint_action_space_config.action_spaces[1].actions,
        simulation_name=simulation_env_config.name, value_function=None, q_table=None,
        lookup_table=[
            [0.8, 0.2],
            [1, 0],
            [1, 0]
        ],
        agent_type=AgentType.RANDOM, avg_R=-1)
    simulation_env_config.simulation_env_input_config.stopping_game_config.R = list(StoppingGameUtil.reward_tensor(
        R_INT=-10, R_COST=-10, R_SLA=0, R_ST=20, L=3))
    simulation_env_config.simulation_env_input_config.stopping_game_config.O = np.array(list(range(0, 6000)))
    agent = DynaSecTestAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                             experiment_config=experiment_config)
    experiment_execution = agent.train()
    # MetastoreFacade.save_experiment_execution(experiment_execution)
    # for policy in experiment_execution.result.policies.values():
    #     MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
