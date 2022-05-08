from typing import List, Dict, Tuple, Union, Optional
import random
import numpy as np
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.simulation_config.state import State
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy


class MixedMultiThresholdStoppingPolicy(Policy):
    """
    A mixed multi-threshold stopping policy
    """

    def __init__(self, Theta: Union[List[List[List[float]]], List[List[List[List[float]]]]],
                 simulation_name: str, L: int, states : List[State], player_type: PlayerType,
                 actions: List[Action], experiment_config: Optional[ExperimentConfig], avg_R: float,
                 agent_type: AgentType, opponent_strategy: Optional["MixedMultiThresholdStoppingPolicy"] = None):
        """
        Initializes the policy

        :param Theta: the buffer with threshold vectors
        :param simulation_name: the simulation name
        :param attacker: whether it is an attacker or not
        :param L: the number of stop actions
        :param states: list of states (required for computing stage policies)
        :param actions: list of actions
        :param experiment_config: the experiment configuration used for training the policy
        :param avg_R: the average reward of the policy when evaluated in the simulation
        :param agent_type: the agent type
        :param opponent_strategy: the opponent's strategy
        """
        super(MixedMultiThresholdStoppingPolicy, self).__init__(agent_type=agent_type, player_type=player_type)
        self.Theta = Theta
        self.id = -1
        self.simulation_name = simulation_name
        self.L = L
        self.states = states
        self.actions = actions
        self.experiment_config = experiment_config
        self.avg_R = avg_R
        self.opponent_strategy = opponent_strategy

    def action(self, o: List[float]) -> int:
        """
        Multi-threshold stopping policy

        :param o: the current observation
        :return: the selected action
        """
        if not self.player_type == PlayerType.ATTACKER:
            a, _ = self._defender_action(o=o)
            return a
        else:
            a1, defender_stop_probability = self.opponent_strategy._defender_action(o=o)
            if a1 == 0:
                defender_stop_probability = 1-defender_stop_probability
            a, _ = self._attacker_action(o=o, defender_stop_probability=defender_stop_probability)
            return a

    def _attacker_action(self, o, defender_stop_probability) -> Tuple[int, float]:
        """
        Multi-threshold stopping policy of the attacker

        :param o: the input observation
        :param defender_stop_probability: the defender's stopping probability
        :return: the selected action (int)
        """
        s = o[2]
        b1 = o[1]
        l = int(o[0])
        thresholds = self.Theta[s][l-1][0]
        counts = self.Theta[s][l-1][1]

        # sum_thresholds = 0
        # for i in range(len(thresholds)):
        #     sum_thresholds = sum_thresholds + thresholds[i]*counts[i]
        # avg_threshold = sum_thresholds/sum(counts)
        # prob = MultiThresholdStoppingPolicy.stopping_probability(b1=b1, threshold=avg_threshold, k=-20)
        # prob = MultiThresholdStoppingPolicy.stopping_probability(b1=defender_stop_probability,
        #                                                          threshold=avg_threshold, k=-20)

        mixture_weights = np.array(counts) / sum(self.Theta[s][l-1][1])
        prob = 0
        for i in range(len(thresholds)):
            if defender_stop_probability >= thresholds[i]:
                prob += mixture_weights[i]*MultiThresholdStoppingPolicy.stopping_probability(
                    b1=defender_stop_probability, threshold=thresholds[i],k=-20)
                # prob += mixture_weights[i]*MultiThresholdStoppingPolicy.stopping_probability(
                #     b1=b1, threshold=thresholds[i],k=-20)


        if s == 1:
            a = 0
            if random.uniform(0,1) < prob:
                a = 1
            else:
                prob = 1-prob
        else:
            a = 1
            if random.uniform(0,1) < prob:
                a = 0
            else:
                prob = 1-prob
        prob = round(prob, 3)
        return a, prob

    def _defender_action(self, o) -> Tuple[int, float]:
        """
        Multi-threshold stopping policy of the defender

        :param o: the input observation
        :return: the selected action (int)
        """
        b1 = o[1]
        l = int(o[0])
        thresholds = self.Theta[l-1][0]
        counts = self.Theta[l-1][1]

        sum_thresholds = 0
        for i in range(len(thresholds)):
            sum_thresholds = sum_thresholds + thresholds[i]*counts[i]
        avg_threshold = sum_thresholds/sum(counts)
        stop_probability = MultiThresholdStoppingPolicy.stopping_probability(b1=b1, threshold=avg_threshold, k=-20)

        # mixture_weights = np.array(counts) / sum(self.Theta[l-1][1])
        # stop_probability = 0
        # for i, thresh in enumerate(thresholds):
        #     if b1 >= thresh:
        #         stop_probability += mixture_weights[i]*MultiThresholdStoppingPolicy.stopping_probability(
        #             b1=b1, threshold=thresh, k=-20)
        # stop_probability = round(stop_probability, 3)

        if random.uniform(0,1) >= stop_probability:
            return 0, stop_probability
        else:
            return 1, stop_probability

    def to_dict(self) -> Dict[str, List[float]]:
        """
        :return: a dict representation of the policy
        """
        d = {}
        d["Theta"] = self.Theta
        d["id"] = self.id
        d["simulation_name"] = self.simulation_name
        d["states"] = list(map(lambda x: x.to_dict(), self.states))
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["player_type"] = self.player_type
        d["agent_type"] = self.agent_type
        d["L"] = self.L
        if self.experiment_config is not None:
            d["experiment_config"] = self.experiment_config.to_dict()
        else:
            d["experiment_config"] = None
        d["avg_R"] = self.avg_R
        return d

    @staticmethod
    def from_dict(d: Dict) -> "MultiThresholdStoppingPolicy":
        """
        Converst a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = MixedMultiThresholdStoppingPolicy(
            Theta=d["Theta"], simulation_name=d["simulation_name"], L=d["L"],
            states=list(map(lambda x: State.from_dict(x), d["states"])), player_type=d["player_type"],
            actions=list(map(lambda x: Action.from_dict(x), d["actions"])),
            experiment_config=ExperimentConfig.from_dict(d["experiment_config"]), avg_R=d["avg_R"],
            agent_type=d["agent_type"])
        obj.id = d["id"]
        return obj

    def update_Theta(self, new_thresholds: List[List[List[float]]]) -> None:
        """
        Updates the threshold buffer

        :param new_thresholds: the new thresholds to add
        :return: None
        """
        if not self.player_type == PlayerType.ATTACKER:
            self._update_Theta_defender(new_thresholds=new_thresholds)
        else:
            self._update_Theta_attacker(new_thresholds=new_thresholds)

    def _update_Theta_attacker(self, new_thresholds: List[List[float]]) -> None:
        """
        Updates the Theta buffer with new attacker thresholds

        :param new_thresholds: the new thresholds to add to the buffer
        :return: None
        """
        for a_thresholds in new_thresholds:
            for s in range(2):
                for l in range(self.L):
                    if self.Theta[s][l] == 0:
                        self.Theta[s][l] = [[a_thresholds[s][l]], [1]]
                    else:
                        if a_thresholds[s][l] in self.Theta[s][l][0]:
                            i = self.Theta[s][l][0].index(a_thresholds[s][l])
                            self.Theta[s][l][1][i] = self.Theta[s][l][1][i] + 1
                        else:
                            self.Theta[s][l][0].append(a_thresholds[s][l])
                            self.Theta[s][l][1].append(1)

    def _update_Theta_defender(self, new_thresholds: List[List[float]]) -> None:
        """
        Updates the theta buffer with new defender thresholds

        :param new_thresholds: the new thresholds to add to the buffer
        :return: None
        """
        for defender_theta in new_thresholds:
            for l in range(self.L):
                if self.Theta[l] == 0:
                    self.Theta[l] = [[defender_theta[l]], [1]]
                else:
                    if defender_theta[l] in self.Theta[l][0]:
                        i = self.Theta[l][0].index(defender_theta[l])
                        self.Theta[l][1][i] = self.Theta[l][1][i] + 1
                    else:
                        self.Theta[l][0].append(defender_theta[l])
                        self.Theta[l][1].append(1)
        # for l in range(self.L):
        #     self.Theta[l] = [[new_thresholds[0][l]], [1]]

    def stage_policy(self, o: Union[List[Union[int, float]], int, float]) \
            -> List[List[float]]:
        b1 = o[1]
        l = int(o[0])
        if not self.player_type == PlayerType.ATTACKER:
            stage_policy = []
            for _ in self.states:
                a1, stopping_probability = self._defender_action(o=o)
                if a1 == 0:
                    stopping_probability = 1 - stopping_probability
                stage_policy.append([1-stopping_probability, stopping_probability])
            return stage_policy
        else:
            stage_policy = []
            a1, defender_stop_probability = self.opponent_strategy._defender_action(o=o)
            if a1 == 0:
                defender_stop_probability = 1-defender_stop_probability
            # print(f"def stop prob:{defender_stop_probability}, o:{o}")
            for s in self.states:
                if s.state_type != StateType.TERMINAL:
                    o = [l,b1,s.id]
                    a, action_prob = self._attacker_action(o=o, defender_stop_probability=defender_stop_probability)
                    if action_prob == 1:
                        action_prob = 0.99
                    if action_prob == 0:
                        action_prob = 0.01
                    if a == 1:
                        stage_policy.append([1-action_prob, action_prob])
                    elif a == 0:
                        stage_policy.append([action_prob, 1-action_prob])
                    else:
                        raise ValueError(f"Invalid state: {s.id}, valid states are: 0 and 1")
                else:
                    stage_policy.append([0.5, 0.5])
            return stage_policy

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"Theta: {self.Theta}, id: {self.id}, simulation_name: {self.simulation_name}, " \
               f"player_type: {self.player_type}, " \
               f"L:{self.L}, states: {self.states}, agent_type: {self.agent_type}, actions: {self.actions}," \
               f"experiment_config: {self.experiment_config}, avg_R: {self.avg_R}"
