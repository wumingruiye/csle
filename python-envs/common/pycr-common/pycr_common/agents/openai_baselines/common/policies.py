"""Policies: abstract base class and concrete implementations."""

import collections
from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import gym
import numpy as np
import torch as th
from torch import nn as nn
import copy

from stable_baselines3.common.preprocessing import get_action_dim, preprocess_obs
from stable_baselines3.common.utils import get_device
import pycr_common.constants.constants as constants
from pycr_common.dao.envs.base_pycr_env import BasePyCREnv
from pycr_common.dao.network.base_env_state import BaseEnvState
from pycr_common.dao.network.base_env_config import BaseEnvConfig
from pycr_common.agents.openai_baselines.common.torch_layers import BaseFeaturesExtractor, \
    FlattenExtractor, MlpExtractor, NatureCNN, create_mlp
from pycr_common.agents.config.agent_config import AgentConfig
from pycr_common.agents.openai_baselines.common.distributions import (Distribution, make_proba_distribution)
from pycr_common.agents.openai_baselines.common.vec_env.subproc_vec_env import SubprocVecEnv
from pycr_common.agents.openai_baselines.common.vec_env.dummy_vec_env import DummyVecEnv


class BaseModel(nn.Module, ABC):
    """
    The base model object: makes predictions in response to observations.

    In the case of policies, the prediction is an action. In the case of critics, it is the
    estimated value of the observation.

    :param observation_space: (gym.spaces.Space) The observation space of the environment
    :param action_space: (gym.spaces.Space) The action space of the environment
    :param features_extractor_class: (Type[BaseFeaturesExtractor]) Features extractor to use.
    :param features_extractor_kwargs: (Optional[Dict[str, Any]]) Keyword arguments
        to pass to the feature extractor.
    :param features_extractor: (nn.Module) Network to extract features
        (a CNN when using images, a nn.Flatten() layer otherwise)
    :param normalize_images: (bool) Whether to normalize images or not,
         dividing by 255.0 (True by default)
    :param optimizer_class: (Type[th.optim.Optimizer]) The optimizer to use,
        ``th.optim.Adam`` by default
    :param optimizer_kwargs: (Optional[Dict[str, Any]]) Additional keyword arguments,
        excluding the learning rate, to pass to the optimizer
    """

    def __init__(
        self,
        observation_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        features_extractor_class: Type[BaseFeaturesExtractor] = FlattenExtractor,
        features_extractor_kwargs: Optional[Dict[str, Any]] = None,
        features_extractor: Optional[nn.Module] = None,
        normalize_images: bool = True,
        optimizer_class: Type[th.optim.Optimizer] = th.optim.Adam,
        optimizer_kwargs: Optional[Dict[str, Any]] = None,
        agent_config: AgentConfig = None
    ):
        super(BaseModel, self).__init__()

        if optimizer_kwargs is None:
            optimizer_kwargs = {}

        if features_extractor_kwargs is None:
            features_extractor_kwargs = {}

        self.observation_space = observation_space
        self.action_space = action_space
        self.features_extractor = features_extractor
        self.normalize_images = normalize_images

        self.optimizer_class = optimizer_class
        self.optimizer_kwargs = optimizer_kwargs
        self.optimizer = None  # type: Optional[th.optim.Optimizer]

        self.features_extractor_class = features_extractor_class
        self.features_extractor_kwargs = features_extractor_kwargs
        self.agent_config = agent_config

    @abstractmethod
    def forward(self, *args, **kwargs):
        del args, kwargs

    def extract_features(self, obs: th.Tensor) -> th.Tensor:
        """
        Preprocess the observation if needed and extract features.

        :param obs: (th.Tensor)
        :return: (th.Tensor)
        """
        assert self.features_extractor is not None, "No feature extractor was set"
        preprocessed_obs = preprocess_obs(obs, self.observation_space, normalize_images=self.normalize_images)
        return self.features_extractor(preprocessed_obs)

    def _get_data(self) -> Dict[str, Any]:
        """
        Get data that need to be saved in order to re-create the model.
        This corresponds to the arguments of the constructor.

        :return: (Dict[str, Any])
        """
        return dict(
            observation_space=self.observation_space,
            action_space=self.action_space,
            # Passed to the constructor by child class
            # squash_output=self.squash_output,
            # features_extractor=self.features_extractor
            normalize_images=self.normalize_images,
        )

    @property
    def device(self) -> th.device:
        """Infer which device this policy lives on by inspecting its parameters.
        If it has no parameters, the 'auto' device is used as a fallback.

        :return: (th.device)"""
        for param in self.parameters():
            return param.device
        return get_device("auto")

    def save(self, path: str) -> None:
        """
        Save model to a given location.

        :param path: (str)
        """
        th.save({"state_dict": self.state_dict(), "data": self._get_data()}, path)

    @classmethod
    def load(cls, path: str, device: Union[th.device, str] = "auto") -> "BaseModel":
        """
        Load model from path.

        :param path: (str)
        :param device: (Union[th.device, str]) Device on which the policy should be loaded.
        :return: (BasePolicy)
        """
        device = get_device(device)
        saved_variables = th.load(path, map_location=device)
        # Create policy object
        model = cls(**saved_variables["data"])  # pytype: disable=not-instantiable
        # Load weights
        model.load_state_dict(saved_variables["state_dict"])
        model.to(device)
        return model

    def load_from_vector(self, vector: np.ndarray):
        """
        Load parameters from a 1D vector.

        :param vector: (np.ndarray)
        """
        th.nn.utils.vector_to_parameters(th.FloatTensor(vector).to(self.device), self.parameters())

    def parameters_to_vector(self) -> np.ndarray:
        """
        Convert the parameters to a 1D vector.

        :return: (np.ndarray)
        """
        return th.nn.utils.parameters_to_vector(self.parameters()).detach().cpu().numpy()


class BasePolicy(BaseModel):
    """The base policy object.

    Parameters are mostly the same as `BaseModel`; additions are documented below.

    :param args: positional arguments passed through to `BaseModel`.
    :param kwargs: keyword arguments passed through to `BaseModel`.
    :param squash_output: (bool) For continuous actions, whether the output is squashed
        or not using a ``tanh()`` function.
    """

    def __init__(self, *args, squash_output: bool = False, **kwargs):
        super(BasePolicy, self).__init__(*args, **kwargs)
        self._squash_output = squash_output

    @staticmethod
    def _dummy_schedule(progress_remaining: float) -> float:
        """ (float) Useful for pickling policy."""
        del progress_remaining
        return 0.0

    @property
    def squash_output(self) -> bool:
        """(bool) Getter for squash_output."""
        return self._squash_output

    @staticmethod
    def init_weights(module: nn.Module, gain: float = 1) -> None:
        """
        Orthogonal initialization (used in PPO and A2C)
        """
        if isinstance(module, (nn.Linear, nn.Conv2d)):
            nn.init.orthogonal_(module.weight, gain=gain)
            if module.bias is not None:
                module.bias.data.fill_(0.0)

    @abstractmethod
    def _predict(self, observation: th.Tensor, deterministic: bool = False, env_state: BaseEnvState = None,
                env_config: BaseEnvConfig = None, m_index : int = None) -> th.Tensor:
        """
        Get the action according to the policy for a given observation.

        By default provides a dummy implementation -- not all BasePolicy classes
        implement this, e.g. if they are a Critic in an Actor-Critic method.

        :param observation: (th.Tensor)
        :param deterministic: (bool) Whether to use stochastic or deterministic actions
        :return: (th.Tensor) Taken action according to the policy
        """

    def predict(
        self,
        observation: np.ndarray,
        state: Optional[np.ndarray] = None,
        mask: Optional[np.ndarray] = None,
        deterministic: bool = False,
        env_config: BaseEnvConfig = None,
        env_configs: BaseEnvConfig = None,
        env_state: BaseEnvState = None,
        env_idx: int = None,
        m_index: int = None,
        infos=None,
        env=None,
        mask_actions: bool = True,
        attacker: bool = True
    ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Get the policy action and state from an observation (and optional state).
        Includes sugar-coating to handle different observations (e.g. normalizing images).

        :param observation: (np.ndarray) the input observation
        :param state: (Optional[np.ndarray]) The last states (can be None, used in recurrent policies)
        :param mask: (Optional[np.ndarray]) The last masks (can be None, used in recurrent policies)
        :param deterministic: (bool) Whether or not to return deterministic actions.
        :return: (Tuple[np.ndarray, Optional[np.ndarray]]) the model's action and the next state
            (used in recurrent policies)
        """
        observation = np.array(observation)
        #vectorized_env = is_vectorized_observation(observation, self.observation_space)
        if observation.shape != self.observation_space.shape:
            observation = observation.reshape((-1,) + self.observation_space.shape)
        observation = th.as_tensor(observation).to(self.device)
        with th.no_grad():
            actions = self._predict(observation, deterministic=deterministic, env_config=env_config,
                                    env_state=env_state, m_index=m_index, infos=infos, env=env,
                                    env_configs=env_configs, env_idx=env_idx, mask_actions=mask_actions,
                                    attacker=attacker)
        if type(actions) == th.Tensor:
            # Convert to numpy
            actions = actions.cpu().numpy()
        return actions, state

class ActorCriticPolicy(BasePolicy):
    """
    Policy class for actor-critic algorithms (has both policy and value prediction).
    Used by A2C, PPO and the likes.

    :param observation_space: (gym.spaces.Space) Observation space
    :param action_space: (gym.spaces.Space) Action space
    :param lr_schedule: (Callable) Learning rate schedule (could be constant)
    :param net_arch: ([int or dict]) The specification of the policy and value networks.
    :param activation_fn: (Type[nn.Module]) Activation function
    :param ortho_init: (bool) Whether to use or not orthogonal initialization
    :param log_std_init: (float) Initial value for the log standard deviation
    :param full_std: (bool) Whether to use (n_features x n_actions) parameters
        for the std instead of only (n_features,)
    :param use_expln: (bool) Use ``expln()`` function instead of ``exp()`` to ensure
        a positive standard deviation (cf paper). It allows to keep variance
        above zero and prevent it from growing too fast. In practice, ``exp()`` is usually enough.
    :param squash_output: (bool) Whether to squash the output using a tanh function
    :param features_extractor_class: (Type[BaseFeaturesExtractor]) Features extractor to use.
    :param features_extractor_kwargs: (Optional[Dict[str, Any]]) Keyword arguments
        to pass to the feature extractor.
    :param normalize_images: (bool) Whether to normalize images or not,
         dividing by 255.0 (True by default)
    :param optimizer_class: (Type[th.optim.Optimizer]) The optimizer to use,
        ``th.optim.Adam`` by default
    :param optimizer_kwargs: (Optional[Dict[str, Any]]) Additional keyword arguments,
        excluding the learning rate, to pass to the optimizer
    """

    def __init__(
        self,
        observation_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        lr_schedule: Callable[[float], float],
        net_arch: Optional[List[Union[int, Dict[str, List[int]]]]] = None,
        activation_fn: Type[nn.Module] = nn.Tanh,
        ortho_init: bool = True,
        log_std_init: float = 0.0,
        full_std: bool = True,
        use_expln: bool = False,
        squash_output: bool = False,
        features_extractor_class: Type[BaseFeaturesExtractor] = FlattenExtractor,
        features_extractor_kwargs: Optional[Dict[str, Any]] = None,
        normalize_images: bool = True,
        optimizer_class: Type[th.optim.Optimizer] = th.optim.Adam,
        optimizer_kwargs: Optional[Dict[str, Any]] = None,
        agent_config: AgentConfig = None,
        m_selection: bool = False,
        m_action: bool = False
    ):

        if optimizer_kwargs is None:
            optimizer_kwargs = {}
            # Small values to avoid NaN in Adam optimizer
            if optimizer_class == th.optim.Adam:
                optimizer_kwargs["eps"] = 1e-5
        super(ActorCriticPolicy, self).__init__(
            observation_space,
            action_space,
            features_extractor_class,
            features_extractor_kwargs,
            optimizer_class=optimizer_class,
            optimizer_kwargs=optimizer_kwargs,
            squash_output=squash_output,
            agent_config=agent_config
        )

        self.m_selection = m_selection
        self.m_action = m_action

        # Default network architecture, from stable-baselines
        if net_arch is None:
            if features_extractor_class == FlattenExtractor:
                net_arch = [dict(pi=[64, 64], vf=[64, 64])]
            else:
                net_arch = []

        self.net_arch = net_arch
        self.activation_fn = activation_fn
        self.ortho_init = ortho_init

        self.features_extractor = features_extractor_class(self.observation_space, **self.features_extractor_kwargs)
        self.features_dim = self.features_extractor.features_dim

        self.normalize_images = normalize_images
        self.log_std_init = log_std_init
        dist_kwargs = None

        self.dist_kwargs = dist_kwargs

        # Action distribution
        self.action_dist = make_proba_distribution(action_space, dist_kwargs=dist_kwargs)

        self.lr_schedule = lr_schedule

        self._build(lr_schedule)

    def copy(self):
        c = ActorCriticPolicy(
            observation_space=self.observation_space,
            action_space=self.action_space,
            lr_schedule=self.lr_schedule,
            net_arch=self.net_arch,
            activation_fn = self.activation_fn,
            ortho_init=self.ortho_init,
            log_std_init=self.log_std_init,
            squash_output=self.squash_output,
            features_extractor_class=self.features_extractor_class,
            features_extractor_kwargs=self.features_extractor_kwargs,
            agent_config=self.agent_config,
            m_selection=self.m_selection,
            m_action=self.m_action
        )
        c.mlp_extractor = copy.deepcopy(self.mlp_extractor)
        c.action_net = copy.deepcopy(self.action_net)
        c.value_net = copy.deepcopy(self.value_net)
        c.optimizer = copy.deepcopy(self.optimizer)
        return c

    def _get_data(self) -> Dict[str, Any]:
        data = super()._get_data()

        default_none_kwargs = self.dist_kwargs or collections.defaultdict(lambda: None)

        data.update(
            dict(
                net_arch=self.net_arch,
                activation_fn=self.activation_fn,
                log_std_init=self.log_std_init,
                squash_output=default_none_kwargs["squash_output"],
                full_std=default_none_kwargs["full_std"],
                use_expln=default_none_kwargs["use_expln"],
                lr_schedule=self._dummy_schedule,  # dummy lr schedule, not needed for loading policy alone
                ortho_init=self.ortho_init,
                optimizer_class=self.optimizer_class,
                optimizer_kwargs=self.optimizer_kwargs,
                features_extractor_class=self.features_extractor_class,
                features_extractor_kwargs=self.features_extractor_kwargs,
            )
        )
        return data

    def _build(self, lr_schedule: Callable[[float], float]) -> None:
        """
        Create the networks and the optimizer.

        :param lr_schedule: (Callable) Learning rate schedule
            lr_schedule(1) is the initial learning rate
        """
        self.mlp_extractor = MlpExtractor(self.features_dim, net_arch=self.net_arch, activation_fn=self.activation_fn)

        latent_dim_pi = self.mlp_extractor.latent_dim_pi

        self.action_net = self.action_dist.proba_distribution_net(latent_dim=latent_dim_pi)
        self.value_net = nn.Linear(self.mlp_extractor.latent_dim_vf, 1)

        # Init weights: use orthogonal initialization
        # with small initial weight for the output
        if self.ortho_init:
            # TODO: check for features_extractor
            # Values from stable-baselines.
            # feature_extractor/mlp values are
            # originally from openai/baselines (default gains/init_scales).
            module_gains = {
                self.features_extractor: np.sqrt(2),
                self.mlp_extractor: np.sqrt(2),
                self.action_net: 0.01,
                self.value_net: 1,
            }
            for module, gain in module_gains.items():
                module.apply(partial(self.init_weights, gain=gain))

        # Setup optimizer with initial learning rate
        self.optimizer = self.optimizer_class(self.parameters(), lr=lr_schedule(1), **self.optimizer_kwargs)

    def forward(self, obs: th.Tensor, deterministic: bool = False,
                m_index : int = None, env = None, infos=None, mask_actions: bool = True, attacker: bool = True,
                return_distribution = False) \
            -> Tuple[th.Tensor, th.Tensor, th.Tensor]:
        """
        Forward pass in all the networks (actor and critic)

        :param obs: (th.Tensor) Observation
        :param deterministic: (bool) Whether to sample or use deterministic actions
        :return: (Tuple[th.Tensor, th.Tensor, th.Tensor]) action, value and log probability of the action
        """

        latent_pi, latent_vf = self._get_latent(obs)
        # Evaluate the values for the given observations
        values = self.value_net(latent_vf)

        # Masking legal actions
        if self.m_action:
            actions = list(range(self.agent_config.output_dim_2))
        else:
            actions = list(range(self.agent_config.output_dim))

        non_legal_actions_total = []
        if mask_actions:
            for i in range(env.num_envs):
                if isinstance(env, DummyVecEnv):
                    non_legal_actions = []
                    if self.agent_config.filter_illegal_actions:
                        if self.agent_config.ar_policy:
                            if self.m_action:
                                non_legal_actions = list(filter(lambda action: not env.envs[i].is_attack_action_legal(
                                    action, env_config=env.envs[i].env_config, env_state=env.envs[i].env_state,
                                    m_action=True, m_index = m_index), actions))
                            elif self.m_selection:
                                non_legal_actions = list(filter(lambda action: not env.envs[i].is_attack_action_legal(
                                    action, env_config=env.envs[i].env_config,
                                    env_state=env.envs[i].env_state, m_selection=True), actions))
                        else:
                            if attacker:
                                non_legal_actions = list(filter(lambda action: not env.envs[i].is_attack_action_legal(
                                    action, env_config=env.envs[i].env_config,
                                    env_state=env.envs[i].env_state), actions))
                            else:
                                non_legal_actions = list(filter(lambda action: not env.envs[i].is_defense_action_legal(
                                    action, env_config=env.envs[i].env_config,
                                    env_state=env.envs[i].env_state), actions))
                    non_legal_actions_total.append(non_legal_actions)
                elif isinstance(env, SubprocVecEnv):
                    if attacker:
                        non_legal_actions_total.append(infos[i][constants.INFO_DICT.ATTACKER_NON_LEGAL_ACTIONS])
                    else:
                        non_legal_actions_total.append(infos[i][constants.INFO_DICT.ATTACKER_NON_LEGAL_ACTIONS])
                else:
                    raise ValueError("Unrecognized env")
        distribution = self._get_action_dist_from_latent(latent_pi, non_legal_actions=non_legal_actions_total)
        actions = distribution.get_actions(deterministic=deterministic)
        log_prob = distribution.log_prob(actions)
        if return_distribution:
            return actions, values, log_prob, distribution
        else:
            return actions, values, log_prob

    def _get_latent(self, obs: th.Tensor) -> Tuple[th.Tensor, th.Tensor, th.Tensor]:
        """
        Get the latent code (i.e., activations of the last layer of each network)
        for the different networks.

        :param obs: (th.Tensor) Observation
        :return: (Tuple[th.Tensor, th.Tensor, th.Tensor]) Latent codes
            for the actor, the value function
        """
        # Preprocess the observation if needed
        features = self.extract_features(obs)
        latent_pi, latent_vf = self.mlp_extractor(features)

        return latent_pi, latent_vf

    def _get_action_dist_from_latent(self, latent_pi: th.Tensor,
                                     non_legal_actions : List[int] = None) -> Distribution:
        """
        Retrieve action distribution given the latent codes.

        :param latent_pi: (th.Tensor) Latent code for the actor
        :return: (Distribution) Action distribution
        """
        mean_actions = self.action_net(latent_pi)
        if self.agent_config.output_dim == 1:
            mean_actions = th.sigmoid(mean_actions)
        #mean_actions = mean_actions*100
        action_logits = mean_actions.clone()
        if non_legal_actions is not None:
            for i in range(len(non_legal_actions)):
                if non_legal_actions is not None and len(non_legal_actions) > 0 and len(non_legal_actions[i]) > 0:
                    if len(action_logits.shape) == 1:
                        # action_probs_1[non_legal_actions] = 0.00000000000001 # Don't set to zero due to invalid distribution errors
                        action_logits[non_legal_actions[i]] = self.agent_config.illegal_action_logit
                    elif len(action_logits.shape) == 2:
                        # action_probs_1[:, non_legal_actions] = 0.00000000000001  # Don't set to zero due to invalid distribution errors
                        action_logits[i][non_legal_actions[i]] = self.agent_config.illegal_action_logit
                    else:
                        raise AssertionError("Invalid shape of action probabilties")
        action_logits_1 = action_logits.to(self.device)
        return self.action_dist.proba_distribution(action_logits=action_logits_1)


    def _predict(self, observation: th.Tensor, deterministic: bool = False, env_state: BaseEnvState = None,
                 env_config: BaseEnvConfig = None, m_index : int = None, env = None, infos = None,
                 env_configs: List[BaseEnvConfig] = None, env_idx: int = None, mask_actions: bool = True,
                 attacker : bool = True) -> th.Tensor:
        """
        Get the action according to the policy for a given observation.

        :param observation: (th.Tensor)
        :param deterministic: (bool) Whether to use stochastic or deterministic actions
        :return: (th.Tensor) Taken action according to the policy
        """
        latent_pi, _ = self._get_latent(observation)

        # Masking legal actions
        if self.m_action:
            actions = list(range(self.agent_config.output_dim_2))
        else:
            actions = list(range(self.agent_config.output_dim))

        #non_legal_actions_total = []
        non_legal_actions = []

        if mask_actions:
            if env is None or isinstance(env, DummyVecEnv):
                non_legal_actions = []
                if self.agent_config.filter_illegal_actions:
                    if self.agent_config.ar_policy:
                        if self.m_action:
                            non_legal_actions = list(filter(lambda action: not env.envs[0].is_attack_action_legal(
                                action, env_config=env_config, env_state=env_state, m_action=True, m_index=m_index), actions))
                        elif self.m_selection:
                            non_legal_actions = list(filter(lambda action: not env.envs[0].is_attack_action_legal(
                                action, env_config=env_config, env_state=env_state, m_selection=True), actions))
                    else:
                        if attacker:
                            non_legal_actions = list(filter(lambda action: not env.envs[0].is_attack_action_legal(
                                action, env_config=env_config, env_state=env_state), actions))
                        else:
                            non_legal_actions = list(filter(lambda action: not env.envs[0].is_defense_action_legal(
                                action, env_config=env_config, env_state=env_state), actions))
                non_legal_actions = [non_legal_actions]
            elif isinstance(env, SubprocVecEnv):
                if attacker:
                    non_legal_actions = infos[0][constants.INFO_DICT.ATTACKER_NON_LEGAL_ACTIONS]
                else:
                    non_legal_actions = infos[0][constants.INFO_DICT.DEFENDER_NON_LEGAL_ACTIONS]
                non_legal_actions = [non_legal_actions]
            else:
                pass
                #raise ValueError("Unrecognized env: {}".format(env))

        distribution = self._get_action_dist_from_latent(latent_pi, non_legal_actions=non_legal_actions)
        return distribution.get_actions(deterministic=deterministic)

    def evaluate_actions(self, obs: th.Tensor, actions: th.Tensor) -> Tuple[th.Tensor, th.Tensor, th.Tensor]:
        """
        Evaluate actions according to the current policy,
        given the observations.

        :param obs: (th.Tensor)
        :param actions: (th.Tensor)
        :return: (th.Tensor, th.Tensor, th.Tensor) estimated value, log likelihood of taking those actions
            and entropy of the action distribution.
        """
        latent_pi, latent_vf = self._get_latent(obs)
        distribution = self._get_action_dist_from_latent(latent_pi)
        log_prob = distribution.log_prob(actions.long())
        values = self.value_net(latent_vf)
        return values, log_prob, distribution.entropy()


class ActorCriticCnnPolicy(ActorCriticPolicy):
    """
    CNN policy class for actor-critic algorithms (has both policy and value prediction).
    Used by A2C, PPO and the likes.

    :param observation_space: (gym.spaces.Space) Observation space
    :param action_space: (gym.spaces.Space) Action space
    :param lr_schedule: (Callable) Learning rate schedule (could be constant)
    :param net_arch: ([int or dict]) The specification of the policy and value networks.
    :param activation_fn: (Type[nn.Module]) Activation function
    :param ortho_init: (bool) Whether to use or not orthogonal initialization
    :param log_std_init: (float) Initial value for the log standard deviation
    :param full_std: (bool) Whether to use (n_features x n_actions) parameters
        for the std instead of only (n_features,)
    :param use_expln: (bool) Use ``expln()`` function instead of ``exp()`` to ensure
        a positive standard deviation (cf paper). It allows to keep variance
        above zero and prevent it from growing too fast. In practice, ``exp()`` is usually enough.
    :param squash_output: (bool) Whether to squash the output using a tanh function
    :param features_extractor_class: (Type[BaseFeaturesExtractor]) Features extractor to use.
    :param features_extractor_kwargs: (Optional[Dict[str, Any]]) Keyword arguments
        to pass to the feature extractor.
    :param normalize_images: (bool) Whether to normalize images or not,
         dividing by 255.0 (True by default)
    :param optimizer_class: (Type[th.optim.Optimizer]) The optimizer to use,
        ``th.optim.Adam`` by default
    :param optimizer_kwargs: (Optional[Dict[str, Any]]) Additional keyword arguments,
        excluding the learning rate, to pass to the optimizer
    """

    def __init__(
        self,
        observation_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        lr_schedule: Callable,
        net_arch: Optional[List[Union[int, Dict[str, List[int]]]]] = None,
        activation_fn: Type[nn.Module] = nn.Tanh,
        ortho_init: bool = True,
        log_std_init: float = 0.0,
        full_std: bool = True,
        use_expln: bool = False,
        squash_output: bool = False,
        features_extractor_class: Type[BaseFeaturesExtractor] = NatureCNN,
        features_extractor_kwargs: Optional[Dict[str, Any]] = None,
        normalize_images: bool = True,
        optimizer_class: Type[th.optim.Optimizer] = th.optim.Adam,
        optimizer_kwargs: Optional[Dict[str, Any]] = None,
    ):
        super(ActorCriticCnnPolicy, self).__init__(
            observation_space,
            action_space,
            lr_schedule,
            net_arch,
            activation_fn,
            ortho_init,
            log_std_init,
            full_std,
            use_expln,
            squash_output,
            features_extractor_class,
            features_extractor_kwargs,
            normalize_images,
            optimizer_class,
            optimizer_kwargs,
        )


class ContinuousCritic(BaseModel):
    """
    Critic network(s) for DDPG/SAC/TD3.
    It represents the action-state value function (Q-value function).
    Compared to A2C/PPO critics, this one represents the Q-value
    and takes the continuous action as input. It is concatenated with the state
    and then fed to the network which outputs a single value: Q(s, a).
    For more recent algorithms like SAC/TD3, multiple networks
    are created to give different estimates.

    By default, it creates two critic networks used to reduce overestimation
    thanks to clipped Q-learning (cf TD3 paper).

    :param observation_space: (gym.spaces.Space) Obervation space
    :param action_space: (gym.spaces.Space) Action space
    :param net_arch: ([int]) Network architecture
    :param features_extractor: (nn.Module) Network to extract features
        (a CNN when using images, a nn.Flatten() layer otherwise)
    :param features_dim: (int) Number of features
    :param activation_fn: (Type[nn.Module]) Activation function
    :param normalize_images: (bool) Whether to normalize images or not,
         dividing by 255.0 (True by default)
    :param n_critics: (int) Number of critic networks to create.
    """

    def __init__(
        self,
        observation_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        net_arch: List[int],
        features_extractor: nn.Module,
        features_dim: int,
        activation_fn: Type[nn.Module] = nn.ReLU,
        normalize_images: bool = True,
        n_critics: int = 2,
    ):
        super().__init__(
            observation_space,
            action_space,
            features_extractor=features_extractor,
            normalize_images=normalize_images,
        )

        action_dim = get_action_dim(self.action_space)

        self.n_critics = n_critics
        self.q_networks = []
        for idx in range(n_critics):
            q_net = create_mlp(features_dim + action_dim, 1, net_arch, activation_fn)
            q_net = nn.Sequential(*q_net)
            self.add_module(f"qf{idx}", q_net)
            self.q_networks.append(q_net)

    def forward(self, obs: th.Tensor, actions: th.Tensor) -> Tuple[th.Tensor, ...]:
        # Learn the features extractor using the policy loss only
        with th.no_grad():
            features = self.extract_features(obs)
        qvalue_input = th.cat([features, actions], dim=1)
        return tuple(q_net(qvalue_input) for q_net in self.q_networks)

    def q1_forward(self, obs: th.Tensor, actions: th.Tensor) -> th.Tensor:
        """
        Only predict the Q-value using the first network.
        This allows to reduce computation when all the estimates are not needed
        (e.g. when updating the policy in TD3).
        """
        with th.no_grad():
            features = self.extract_features(obs)
        return self.q_networks[0](th.cat([features, actions], dim=1))


_policy_registry = dict()  # type: Dict[Type[BasePolicy], Dict[str, Type[BasePolicy]]]


def get_policy_from_name(base_policy_type: Type[BasePolicy], name: str) -> Type[BasePolicy]:
    """
    Returns the registered policy from the base type and name.
    See `register_policy` for registering policies and explanation.

    :param base_policy_type: (Type[BasePolicy]) the base policy class
    :param name: (str) the policy name
    :return: (Type[BasePolicy]) the policy
    """
    if base_policy_type not in _policy_registry:
        raise KeyError(f"Error: the policy type {base_policy_type} is not registered!")
    if name not in _policy_registry[base_policy_type]:
        raise KeyError(
            f"Error: unknown policy type {name},"
            f"the only registed policy type are: {list(_policy_registry[base_policy_type].keys())}!"
        )
    return _policy_registry[base_policy_type][name]


def register_policy(name: str, policy: Type[BasePolicy]) -> None:
    """
    Register a policy, so it can be called using its name.
    e.g. SAC('MlpPolicy', ...) instead of SAC(MlpPolicy, ...).

    The goal here is to standardize policy naming, e.g.
    all algorithms can call upon "MlpPolicy" or "CnnPolicy",
    and they receive respective policies that work for them.
    Consider following:

    OnlinePolicy
    -- OnlineMlpPolicy ("MlpPolicy")
    -- OnlineCnnPolicy ("CnnPolicy")
    OfflinePolicy
    -- OfflineMlpPolicy ("MlpPolicy")
    -- OfflineCnnPolicy ("CnnPolicy")

    Two policies have name "MlpPolicy" and two have "CnnPolicy".
    In `get_policy_from_name`, the parent class (e.g. OnlinePolicy)
    is given and used to select and return the correct policy.

    :param name: (str) the policy name
    :param policy: (Type[BasePolicy]) the policy class
    """
    sub_class = None
    for cls in BasePolicy.__subclasses__():
        if issubclass(policy, cls):
            sub_class = cls
            break
    if sub_class is None:
        raise ValueError(f"Error: the policy {policy} is not of any known subclasses of BasePolicy!")

    if sub_class not in _policy_registry:
        _policy_registry[sub_class] = {}
    if name in _policy_registry[sub_class]:
        # Check if the registered policy is same
        # we try to register. If not so,
        # do not override and complain.
        if _policy_registry[sub_class][name] != policy:
            raise ValueError(f"Error: the name {name} is already registered for a different policy, will not override.")
    _policy_registry[sub_class][name] = policy