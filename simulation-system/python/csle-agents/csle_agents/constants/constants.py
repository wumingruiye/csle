"""
Constants for csle-agents
"""


class COMMON:
    """
    Common string constants among all agents
    """
    AVERAGE_REWARD = "average_reward"
    EVAL_EVERY = "eval_every"
    EVAL_BATCH_SIZE = "eval_batch_size"
    NUM_TRAINING_TIMESTEPS = "num_training_timesteps"
    NUM_NEURONS_PER_HIDDEN_LAYER = "num_neurons_per_hidden_layer"
    NUM_HIDDEN_LAYERS = "num_hidden_layers"
    BATCH_SIZE = "batch_size"
    LEARNING_RATE = "learning_rate"
    DEVICE = "device"
    GAMMA = "gamma"


class PPO:
    """
    String constants related to PPO
    """
    STEPS_BETWEEN_UPDATES = "steps_between_updates"
    GAE_LAMBDA = "gae_lambda"
    CLIP_RANGE = "clip_range"
    CLIP_RANGE_VF = "clip_range_vf"
    ENT_COEF = "ent_coef"
    VF_COEF = "vf_coef"
    MAX_GRAD_NORM = "max_grad_norm"
    TARGET_KL = "target_kl"
    MLP_POLICY = "MlpPolicy"


class T_SPSA:
    """
    String constants related to T-SPSA
    """
    a = "a"
    c = "c"
    LAMBDA = "lambda"
    A = "A"
    EPSILON = "epsilon"
    N = "N"
    L = "L"
    THETA1 = "theta1"
    THETAS = "thetas"
    THRESHOLDS = "thresholds"
    R = "R"