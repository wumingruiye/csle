import gym
import numpy as np


class StoppingGameConfig:
    """
    DTO class containing the configuration of the stopping game
    """

    def __init__(self, T: np.ndarray, O: np.ndarray, Z: np.ndarray, R: np.ndarray, S: np.ndarray, A1: np.ndarray,
                 A2: np.ndarray, L: int, R_INT: int, R_COST: int, R_SLA: int, R_ST: int, b1: np.ndarray,
                 save_dir: str) -> None:
        """
        Initializes the DTO

        :param T: the transition tensor
        :param O: the observation space
        :param Z: the observation tensor
        :param R: the reward function
        :param S: the state space
        :param A1: the action space of the defender
        :param A2: the action space of the attacker
        :param L: the maximum number of stops of the defender
        :param R_INT: the R_INT constant for the reward function
        :param R_COST: the R_COST constant for the reward function
        :param R_SLA: the R_SLA constant for the reward function
        :param R_ST: the R_ST constant for the reward function
        :param b1: the initial belief
        :param save_dir: the directory to save artefacts produced by the environment
        """
        self.T = T
        self.O = O
        self.Z = Z
        self.R = R
        self.S = S
        self.L = L
        self.R_INT = R_INT
        self.R_COST = R_COST
        self.R_SLA = R_SLA
        self.R_ST = R_ST
        self.A1 = A1
        self.A2 = A2
        self.b1 = b1
        self.save_dir = save_dir


    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"T:{self.T}, O:{self.O}, Z:{self.Z}, R:{self.R}, S:{self.S}, A1:{self.A1}, A2:{self.A2}, L:{self.L}, " \
               f"R_INT:{self.R_INT}, R_COST:{self.R_COST}, R_SLA:{self.R_SLA}, R_ST:{self.R_ST}, b1:{self.b1}, " \
               f"save_dir: {self.save_dir}"

    def attacker_observation_space(self) -> gym.spaces.Box:
        """
        :return: the attacker's observation space
        """
        return gym.spaces.Box(low=np.array([0,0,0]), high=np.array([self.L,1,2]), dtype=np.float32,
                       shape=(3,))

    def defender_observation_space(self) -> gym.spaces.Box:
        """
        :return: the defender's observation space
        """
        return gym.spaces.Box(low=np.array([0,0]), high=np.array([self.L,1]), dtype=np.float32,
                              shape=(2,))

    def attacker_action_space(self) -> gym.spaces.Discrete:
        """
        :return: the attacker's action space
        """
        return gym.spaces.Discrete(len(self.A2))

    def defender_action_space(self) -> gym.spaces.Discrete:
        """
        :return: the defender's action space
        """
        return gym.spaces.Discrete(len(self.A1))