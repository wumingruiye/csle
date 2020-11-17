import pandas as pd
import numpy as np
from gym_pycr_pwcrack.util.experiments_util import plotting_util

def plot_rewards_steps_v1_v2_v3_v4():
    ppo_v1_df_0 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v1/cluster/ppo_baseline/results/data/0/1605647813.0375652_train.csv")
    ppo_v1_df_299 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v1/cluster/ppo_baseline/results/data/299/1605648113.4477253_train.csv")
    ppo_v1_df_399 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v1/cluster/ppo_baseline/results/data/399/1605648257.510173_train.csv")
    ppo_v1_df_499 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v1/cluster/ppo_baseline/results/data/499/1605648396.8842435_train.csv")
    ppo_v1_df_999 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v1/cluster/ppo_baseline/results/data/999/1605647962.3639574_train.csv")
    ppo_dfs_v1 = [ppo_v1_df_0, ppo_v1_df_299, ppo_v1_df_399, ppo_v1_df_499, ppo_v1_df_999]

    ppo_v2_df_0 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v2/cluster/ppo_baseline/results/data/0/1605644277.9484346_train.csv")
    ppo_v2_df_299 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v2/cluster/ppo_baseline/results/data/299/1605644643.7108836_train.csv")
    ppo_v2_df_399 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v2/cluster/ppo_baseline/results/data/399/1605644824.44998_train.csv")
    ppo_v2_df_499 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v2/cluster/ppo_baseline/results/data/499/1605644994.556923_train.csv")
    ppo_v2_df_999 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v2/cluster/ppo_baseline/results/data/999/1605644463.7742753_train.csv")
    ppo_dfs_v2 = [ppo_v2_df_0, ppo_v2_df_299, ppo_v2_df_399, ppo_v2_df_499, ppo_v2_df_999]

    ppo_v3_df_0 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v3/cluster/ppo_baseline/results/data/0/1605645849.4342642_train.csv")
    ppo_v3_df_299 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v3/cluster/ppo_baseline/results/data/299/1605646269.5544713_train.csv")
    ppo_v3_df_399 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v3/cluster/ppo_baseline/results/data/399/1605646489.2817347_train.csv")
    ppo_v3_df_499 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v3/cluster/ppo_baseline/results/data/499/1605646692.2049596_train.csv")
    ppo_v3_df_999 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_1/training/v3/cluster/ppo_baseline/results/data/999/1605646061.7188168_train.csv")
    ppo_dfs_v3 = [ppo_v3_df_0, ppo_v3_df_299, ppo_v3_df_399, ppo_v3_df_499, ppo_v3_df_999]

    # ppo_v4_df_0 = pd.read_csv(
    #     "./v4/cluster/ppo_baseline/results/data/0/1603190715.7338402_train.csv")
    # ppo_v4_df_299 = pd.read_csv(
    #     "./v4/cluster/ppo_baseline/results/data/299/1603192933.9591403_train.csv")
    # ppo_v4_df_399 = pd.read_csv(
    #     "./v4/cluster/ppo_baseline/results/data/399/1603194281.0459163_train.csv")
    # ppo_v4_df_499 = pd.read_csv(
    #     "./v4/cluster/ppo_baseline/results/data/499/1603195265.9069285_train.csv")
    # ppo_v4_df_999 = pd.read_csv(
    #     "./v4/cluster/ppo_baseline/results/data/999/1603191648.747736_train.csv")
    #ppo_dfs_v4 = [ppo_v4_df_0, ppo_v4_df_299, ppo_v4_df_399, ppo_v4_df_499, ppo_v4_df_999]

    rewards_data_v1 = list(map(lambda df: df["eval_avg_episode_rewards"].values, ppo_dfs_v1))
    rewards_means_v1 = np.mean(tuple(rewards_data_v1), axis=0)
    rewards_stds_v1 = np.std(tuple(rewards_data_v1), axis=0, ddof=1)

    flags_data_v1 = list(map(lambda df: df["eval_avg_episode_flags_percentage"].values, ppo_dfs_v1))
    flags_means_v1 = np.mean(tuple(flags_data_v1), axis=0)
    flags_stds_v1 = np.std(tuple(flags_data_v1), axis=0, ddof=1)

    steps_data_v1 = list(map(lambda df: df["eval_avg_episode_steps"].values, ppo_dfs_v1))
    steps_means_v1 = np.mean(tuple(steps_data_v1), axis=0)
    steps_stds_v1 = np.std(tuple(steps_data_v1), axis=0, ddof=1)

    rewards_data_v2 = list(map(lambda df: df["eval_avg_episode_rewards"].values, ppo_dfs_v2))
    rewards_means_v2 = np.mean(tuple(rewards_data_v2), axis=0)
    rewards_stds_v2 = np.std(tuple(rewards_data_v2), axis=0, ddof=1)

    flags_data_v2 = list(map(lambda df: df["eval_avg_episode_flags_percentage"].values, ppo_dfs_v2))
    flags_means_v2 = np.mean(tuple(flags_data_v2), axis=0)
    flags_stds_v2 = np.std(tuple(flags_data_v2), axis=0, ddof=1)

    steps_data_v2 = list(map(lambda df: df["eval_avg_episode_steps"].values, ppo_dfs_v2))
    steps_means_v2 = np.mean(tuple(steps_data_v2), axis=0)
    steps_stds_v2 = np.std(tuple(steps_data_v2), axis=0, ddof=1)

    rewards_data_v3 = list(map(lambda df: df["eval_avg_episode_rewards"].values, ppo_dfs_v3))
    rewards_means_v3 = np.mean(tuple(rewards_data_v3), axis=0)
    rewards_stds_v3 = np.std(tuple(rewards_data_v3), axis=0, ddof=1)

    flags_data_v3 = list(map(lambda df: df["eval_avg_episode_flags_percentage"].values, ppo_dfs_v3))
    flags_means_v3 = np.mean(tuple(flags_data_v3), axis=0)
    flags_stds_v3 = np.std(tuple(flags_data_v3), axis=0, ddof=1)

    steps_data_v3 = list(map(lambda df: df["eval_avg_episode_steps"].values, ppo_dfs_v3))
    steps_means_v3 = np.mean(tuple(steps_data_v3), axis=0)
    steps_stds_v3 = np.std(tuple(steps_data_v3), axis=0, ddof=1)

    # rewards_data_v4 = list(map(lambda df: df["eval_avg_episode_rewards"].values, ppo_dfs_v4))
    # rewards_means_v4 = np.mean(tuple(rewards_data_v4), axis=0)
    # rewards_stds_v4 = np.std(tuple(rewards_data_v4), axis=0, ddof=1)
    #
    # flags_data_v4 = list(map(lambda df: df["eval_avg_episode_flags_percentage"].values, ppo_dfs_v4))
    # flags_means_v4 = np.mean(tuple(flags_data_v4), axis=0)
    # flags_stds_v4 = np.std(tuple(flags_data_v4), axis=0, ddof=1)
    #
    # steps_data_v4 = list(map(lambda df: df["eval_avg_episode_steps"].values, ppo_dfs_v4))
    # steps_means_v4 = np.mean(tuple(steps_data_v4), axis=0)
    # steps_stds_v4 = np.std(tuple(steps_data_v4), axis=0, ddof=1)

    # ylim_rew = (min([min(rewards_means_v1 - rewards_stds_v1),
    #                  min(rewards_means_v2 - rewards_stds_v2),
    #                  min(rewards_means_v3 - rewards_stds_v3),
    #                  min(rewards_means_v4 - rewards_stds_v4)]),
    #             max([max(rewards_means_v1 + rewards_stds_v1),
    #                  max(rewards_means_v2 + rewards_stds_v2),
    #                  max(rewards_means_v3 + rewards_stds_v3),
    #                  max(rewards_means_v4 + rewards_stds_v4)]))
    # ylim_step = (min([min(steps_means_v1 - steps_stds_v1),
    #                   min(steps_means_v2 - steps_stds_v2),
    #                   min(steps_means_v3 - steps_stds_v3),
    #                   min(steps_means_v4 - steps_stds_v4)]),
    #              max([max(steps_means_v1 + steps_stds_v1),
    #                   max(steps_means_v2 + steps_stds_v2),
    #                   max(steps_means_v3 + steps_stds_v3),
    #                   max(steps_means_v4 + steps_stds_v4)]))

    ylim_rew = (min([min(rewards_means_v1 - rewards_stds_v1),
                     min(rewards_means_v2 - rewards_stds_v2),
                     min(rewards_means_v3 - rewards_stds_v3)]),
                max([max(rewards_means_v1 + rewards_stds_v1),
                     max(rewards_means_v2 + rewards_stds_v2),
                     max(rewards_means_v3 + rewards_stds_v3)]))
    ylim_step = (min([min(steps_means_v1 - steps_stds_v1),
                      min(steps_means_v2 - steps_stds_v2),
                      min(steps_means_v3 - steps_stds_v3)]),
                 max([max(steps_means_v1 + steps_stds_v1),
                      max(steps_means_v2 + steps_stds_v2),
                      max(steps_means_v3 + steps_stds_v3)]))

    plotting_util.plot_rewards_steps_4(rewards_data_v1[0:200], rewards_means_v1[0:200], rewards_stds_v1[0:200],
                         flags_data_v1[0:200], flags_means_v1[0:200], flags_stds_v1[0:200],
                         steps_data_v1[0:200], steps_means_v1[0:200], steps_stds_v1[0:200],
                         rewards_data_v2[0:200], rewards_means_v2[0:200], rewards_stds_v2[0:200],
                         flags_data_v2[0:200], flags_means_v2[0:200], flags_stds_v2[0:200],
                         steps_data_v2[0:200], steps_means_v2[0:200], steps_stds_v2[0:200],
                         rewards_data_v3[0:200], rewards_means_v3[0:200], rewards_stds_v3[0:200],
                         flags_data_v3[0:200], flags_means_v3[0:200], flags_stds_v3[0:200],
                         steps_data_v3[0:200], steps_means_v3[0:200], steps_stds_v3[0:200],

                        None, None, None, None, None, None, None, None, None,
                         # rewards_data_v4[0:200], rewards_means_v4[0:200], rewards_stds_v4[0:200],
                         # flags_data_v4[0:200], flags_means_v4[0:200], flags_stds_v4[0:200],
                         # steps_data_v4[0:200], steps_means_v4[0:200], steps_stds_v4[0:200],

                         "23 actions", "54 actions", "90 actions", "155 actions", ylim_rew, ylim_step,
                         "./steps_rewards_eval_v1_v2_v3_v4", markevery=10, optimal_steps=5, optimal_reward=16)

    ylim_rew = (0, 150)
    ylim_step = (7, 30)

    plotting_util.plot_rewards_steps_4(rewards_data_v1[0:200], rewards_means_v1[0:200], rewards_stds_v1[0:200],
                         flags_data_v1[0:200], flags_means_v1[0:200], flags_stds_v1[0:200],
                         steps_data_v1[0:200], steps_means_v1[0:200], steps_stds_v1[0:200],
                         rewards_data_v2[0:200], rewards_means_v2[0:200], rewards_stds_v2[0:200],
                         flags_data_v2[0:200], flags_means_v2[0:200], flags_stds_v2[0:200],
                         steps_data_v2[0:200], steps_means_v2[0:200], steps_stds_v2[0:200],
                         rewards_data_v3[0:200], rewards_means_v3[0:200], rewards_stds_v3[0:200],
                         flags_data_v3[0:200], flags_means_v3[0:200], flags_stds_v3[0:200],
                         steps_data_v3[0:200], steps_means_v3[0:200], steps_stds_v3[0:200],

                        None, None, None, None, None, None, None, None, None,
                         # rewards_data_v4[0:200], rewards_means_v4[0:200], rewards_stds_v4[0:200],
                         # flags_data_v4[0:200], flags_means_v4[0:200], flags_stds_v4[0:200],
                         # steps_data_v4[0:200], steps_means_v4[0:200], steps_stds_v4[0:200],

                         "23 actions", "54 actions", "90 actions", "155 actions", ylim_rew, ylim_step,
                         "./steps_rewards_eval_v1_v2_v3_v4_zoomedin", markevery=10, optimal_steps=5, optimal_reward=16)

    rewards_data_v1 = list(map(lambda df: df["avg_episode_rewards"].values, ppo_dfs_v1))
    rewards_means_v1 = np.mean(tuple(rewards_data_v1), axis=0)
    rewards_stds_v1 = np.std(tuple(rewards_data_v1), axis=0, ddof=1)

    flags_data_v1 = list(map(lambda df: df["avg_episode_flags_percentage"].values, ppo_dfs_v1))
    flags_means_v1 = np.mean(tuple(flags_data_v1), axis=0)
    flags_stds_v1 = np.std(tuple(flags_data_v1), axis=0, ddof=1)

    steps_data_v1 = list(map(lambda df: df["avg_episode_steps"].values, ppo_dfs_v1))
    steps_means_v1 = np.mean(tuple(steps_data_v1), axis=0)
    steps_stds_v1 = np.std(tuple(steps_data_v1), axis=0, ddof=1)

    rewards_data_v2 = list(map(lambda df: df["avg_episode_rewards"].values, ppo_dfs_v2))
    rewards_means_v2 = np.mean(tuple(rewards_data_v2), axis=0)
    rewards_stds_v2 = np.std(tuple(rewards_data_v2), axis=0, ddof=1)

    flags_data_v2 = list(map(lambda df: df["avg_episode_flags_percentage"].values, ppo_dfs_v2))
    flags_means_v2 = np.mean(tuple(flags_data_v2), axis=0)
    flags_stds_v2 = np.std(tuple(flags_data_v2), axis=0, ddof=1)

    steps_data_v2 = list(map(lambda df: df["avg_episode_steps"].values, ppo_dfs_v2))
    steps_means_v2 = np.mean(tuple(steps_data_v2), axis=0)
    steps_stds_v2 = np.std(tuple(steps_data_v2), axis=0, ddof=1)

    rewards_data_v3 = list(map(lambda df: df["avg_episode_rewards"].values, ppo_dfs_v3))
    rewards_means_v3 = np.mean(tuple(rewards_data_v3), axis=0)
    rewards_stds_v3 = np.std(tuple(rewards_data_v3), axis=0, ddof=1)

    flags_data_v3 = list(map(lambda df: df["avg_episode_flags_percentage"].values, ppo_dfs_v3))
    flags_means_v3 = np.mean(tuple(flags_data_v3), axis=0)
    flags_stds_v3 = np.std(tuple(flags_data_v3), axis=0, ddof=1)

    steps_data_v3 = list(map(lambda df: df["avg_episode_steps"].values, ppo_dfs_v3))
    steps_means_v3 = np.mean(tuple(steps_data_v3), axis=0)
    steps_stds_v3 = np.std(tuple(steps_data_v3), axis=0, ddof=1)

    # rewards_data_v4 = list(map(lambda df: df["avg_episode_rewards"].values, ppo_dfs_v4))
    # rewards_means_v4 = np.mean(tuple(rewards_data_v4), axis=0)
    # rewards_stds_v4 = np.std(tuple(rewards_data_v4), axis=0, ddof=1)
    #
    # flags_data_v4 = list(map(lambda df: df["avg_episode_flags_percentage"].values, ppo_dfs_v4))
    # flags_means_v4 = np.mean(tuple(flags_data_v4), axis=0)
    # flags_stds_v4 = np.std(tuple(flags_data_v4), axis=0, ddof=1)
    #
    # steps_data_v4 = list(map(lambda df: df["avg_episode_steps"].values, ppo_dfs_v4))
    # steps_means_v4 = np.mean(tuple(steps_data_v4), axis=0)
    # steps_stds_v4 = np.std(tuple(steps_data_v4), axis=0, ddof=1)

    # ylim_rew = (min([min(rewards_means_v1 - rewards_stds_v1),
    #                  min(rewards_means_v2 - rewards_stds_v2),
    #                  min(rewards_means_v3 - rewards_stds_v3),
    #                  min(rewards_means_v4 - rewards_stds_v4)]),
    #             max([max(rewards_means_v1 + rewards_stds_v1),
    #                  max(rewards_means_v2 + rewards_stds_v2),
    #                  max(rewards_means_v3 + rewards_stds_v3),
    #                  max(rewards_means_v4 + rewards_stds_v4)]))
    # ylim_step = (min([min(steps_means_v1 - steps_stds_v1),
    #                   min(steps_means_v2 - steps_stds_v2),
    #                   min(steps_means_v3 - steps_stds_v3),
    #                   min(steps_means_v4 - steps_stds_v4)]),
    #              max([max(steps_means_v1 + steps_stds_v1),
    #                   max(steps_means_v2 + steps_stds_v2),
    #                   max(steps_means_v3 + steps_stds_v3),
    #                   max(steps_means_v4 + steps_stds_v4)]))

    ylim_rew = (min([min(rewards_means_v1 - rewards_stds_v1),
                     min(rewards_means_v2 - rewards_stds_v2),
                     min(rewards_means_v3 - rewards_stds_v3)]),
                max([max(rewards_means_v1 + rewards_stds_v1),
                     max(rewards_means_v2 + rewards_stds_v2),
                     max(rewards_means_v3 + rewards_stds_v3)]))
    ylim_step = (min([min(steps_means_v1 - steps_stds_v1),
                      min(steps_means_v2 - steps_stds_v2),
                      min(steps_means_v3 - steps_stds_v3)]),
                 max([max(steps_means_v1 + steps_stds_v1),
                      max(steps_means_v2 + steps_stds_v2),
                      max(steps_means_v3 + steps_stds_v3)]))

    plotting_util.plot_rewards_steps_4(rewards_data_v1[0:200], rewards_means_v1[0:200], rewards_stds_v1[0:200],
                         flags_data_v1[0:200], flags_means_v1[0:200], flags_stds_v1[0:200],
                         steps_data_v1[0:200], steps_means_v1[0:200], steps_stds_v1[0:200],

                         rewards_data_v2[0:200], rewards_means_v2[0:200], rewards_stds_v2[0:200],
                         flags_data_v2[0:200], flags_means_v2[0:200], flags_stds_v2[0:200],
                         steps_data_v2[0:200], steps_means_v2[0:200], steps_stds_v2[0:200],

                         rewards_data_v3[0:200], rewards_means_v3[0:200], rewards_stds_v3[0:200],
                         flags_data_v3[0:200], flags_means_v3[0:200], flags_stds_v3[0:200],
                         steps_data_v3[0:200], steps_means_v3[0:200], steps_stds_v3[0:200],
                        None, None, None, None, None, None, None, None, None,
                         # rewards_data_v4[0:200], rewards_means_v4[0:200], rewards_stds_v4[0:200],
                         # flags_data_v4[0:200], flags_means_v4[0:200], flags_stds_v4[0:200],
                         # steps_data_v4[0:200], steps_means_v4[0:200], steps_stds_v4[0:200],

                         "23 actions", "54 actions", "90 actions", "155 actions", ylim_rew, ylim_step,
                         "./steps_rewards_v1_v2_v3_v4", markevery=10, optimal_steps=5, optimal_reward=16)


if __name__ == '__main__':
    plot_rewards_steps_v1_v2_v3_v4()

