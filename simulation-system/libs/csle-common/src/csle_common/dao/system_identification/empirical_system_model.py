from typing import List, Dict, Any
import math
from scipy.special import rel_entr
from csle_common.dao.system_identification.empirical_conditional import EmpiricalConditional
from csle_common.dao.system_identification.system_model import SystemModel
from csle_common.dao.system_identification.system_model_type import SystemModelType


class EmpiricalSystemModel(SystemModel):
    """
    A system model (list of conditional distributions) made up of empirical distributions
    """

    def __init__(self, emulation_env_name: str, emulation_statistic_id: int,
                 conditional_metric_distributions: List[List[EmpiricalConditional]], descr: str):
        """
        Initializes the object

        :param emulation: the emulation that this system model is for
        :param emulation_statistic_id: the emulation statistic that this model was built from
        :param conditional_metric_distributions: the list of conditional distributions
        :param descr: description of the model
        """
        super(EmpiricalSystemModel, self).__init__(descr=descr, model_type=SystemModelType.EMPIRICAL_DISTRIBUTION)
        self.conditional_metric_distributions = conditional_metric_distributions
        self.emulation_env_name = emulation_env_name
        self.emulation_statistic_id = emulation_statistic_id
        self.id = -1
        self.conditionals_kl_divergences = {}
        self.compute_kl_divergences()

    def compute_kl_divergences(self) -> None:
        """
        Computes the KL-divergences betwen different conditional distributions

        :return: None
        """
        for metric_distributions_condition_1 in self.conditional_metric_distributions:
            self.conditionals_kl_divergences[metric_distributions_condition_1[0].conditional_name] = {}
            for metric_distributions_condition_2 in self.conditional_metric_distributions:
                self.conditionals_kl_divergences[metric_distributions_condition_1[0].conditional_name][
                    metric_distributions_condition_2[0].conditional_name] = {}
                for i, metric_dist in enumerate(metric_distributions_condition_1):
                    self.conditionals_kl_divergences[metric_distributions_condition_1[0].conditional_name][
                        metric_distributions_condition_2[0].conditional_name][metric_dist.metric_name] = float(
                        round(sum(rel_entr(
                            metric_dist.probabilities, metric_distributions_condition_2[i].probabilities)), 3))
                    if math.isinf(
                            self.conditionals_kl_divergences[metric_distributions_condition_1[0].conditional_name][
                                metric_distributions_condition_2[0].conditional_name][metric_dist.metric_name]):
                        self.conditionals_kl_divergences[metric_distributions_condition_1[0].conditional_name][
                            metric_distributions_condition_2[0].conditional_name][
                            metric_dist.metric_name] = "inf"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmpiricalSystemModel":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        dto = EmpiricalSystemModel(
            conditional_metric_distributions=list(map(
                lambda x: list(map(lambda y: EmpiricalConditional.from_dict(y), x)),
                d["conditional_metric_distributions"])),
            emulation_env_name=d["emulation_env_name"], emulation_statistic_id=d["emulation_statistic_id"],
            descr=d["descr"]
        )
        if "id" in d:
            dto.id = d["id"]
        return dto

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d = {}
        d["conditional_metric_distributions"] = list(map(lambda x: list(map(lambda y: y.to_dict(), x)),
                                                         self.conditional_metric_distributions))
        d["emulation_env_name"] = self.emulation_env_name
        d["emulation_statistic_id"] = self.emulation_statistic_id
        d["descr"] = self.descr
        d["id"] = self.id
        d["conditionals_kl_divergences"] = self.conditionals_kl_divergences
        d["model_type"] = self.model_type
        return d

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"conditional_distributions: {self.conditional_metric_distributions}, " \
               f"emulation_env_name: {self.emulation_env_name}, " \
               f"emulation_statistic_id: {self.emulation_statistic_id}," \
               f"descr: {self.descr}, conditionals_kl_divergences: {self.conditionals_kl_divergences}, " \
               f"model_type: {self.model_type}"

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    def copy(self) -> "EmpiricalSystemModel":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmpiricalSystemModel":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmpiricalSystemModel.from_dict(json.loads(json_str))
