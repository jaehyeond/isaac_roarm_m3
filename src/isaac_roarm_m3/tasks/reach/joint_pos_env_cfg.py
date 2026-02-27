import isaaclab_tasks.manager_based.manipulation.reach.mdp as mdp
from isaaclab.utils import configclass
from isaac_roarm_m3.robots import ROARM_M3_CFG
from isaac_roarm_m3.tasks.reach.reach_env_cfg import ReachEnvCfg


@configclass
class RoArmM3ReachEnvCfg(ReachEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        # Set robot
        self.scene.robot = ROARM_M3_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # Override rewards — end effector body
        self.rewards.end_effector_position_tracking.params["asset_cfg"].body_names = ["gripper_link"]
        self.rewards.end_effector_position_tracking_fine_grained.params["asset_cfg"].body_names = ["gripper_link"]
        self.rewards.end_effector_orientation_tracking.params["asset_cfg"].body_names = ["gripper_link"]

        # Disable orientation tracking initially (focus on position first)
        self.rewards.end_effector_orientation_tracking.weight = 0.0

        # Override actions — 5 arm joints (exclude gripper for reach task)
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=[
                "base_link_to_link1",
                "link1_to_link2",
                "link2_to_link3",
                "link3_to_link4",
                "link4_to_link5",
            ],
            scale=0.5,
            use_default_offset=True,
        )

        # Override command generator body
        self.commands.ee_pose.body_name = ["gripper_link"]


@configclass
class RoArmM3ReachEnvCfg_PLAY(RoArmM3ReachEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        self.observations.policy.enable_corruption = False
