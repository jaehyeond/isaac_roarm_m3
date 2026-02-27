import gymnasium as gym

from . import agents

##
# Register Gym environments.
##

gym.register(
    id="Isaac-RoArm-M3-Reach-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": f"{__name__}.joint_pos_env_cfg:RoArmM3ReachEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ReachPPORunnerCfg",
    },
    disable_env_checker=True,
)

gym.register(
    id="Isaac-RoArm-M3-Reach-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": f"{__name__}.joint_pos_env_cfg:RoArmM3ReachEnvCfg_PLAY",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ReachPPORunnerCfg",
    },
    disable_env_checker=True,
)
