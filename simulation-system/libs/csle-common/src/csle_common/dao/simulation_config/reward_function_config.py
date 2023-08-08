from typing import Dict, Any, List

import numpy as np

from csle_base.json_serializable import JSONSerializable


class RewardFunctionConfig(JSONSerializable):
    """
    DTO containing the reward tensor of a simulation
    """

    def __init__(self, reward_tensor: List):
        """
        Initalizes the DTO

        :param reward_tensor: the reward tensor of the simulation
        """
        self.reward_tensor = reward_tensor

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RewardFunctionConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = RewardFunctionConfig(reward_tensor=d["reward_tensor"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation  of the object
        """
        d = {}
        if isinstance(self.reward_tensor, np.ndarray):
            tensor = self.reward_tensor.tolist()
        else:
            tensor = self.reward_tensor
        for i in range(len(tensor)):
            if isinstance(tensor[i], np.ndarray):
                tensor[i] = tensor[i].tolist()
        d["reward_tensor"] = list(tensor)
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"reward_tensor:{self.reward_tensor}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "RewardFunctionConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return RewardFunctionConfig.from_dict(json.loads(json_str))
