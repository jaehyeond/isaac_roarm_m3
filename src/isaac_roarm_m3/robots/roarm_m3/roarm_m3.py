from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

TEMPLATE_ASSETS_DATA_DIR = Path(__file__).resolve().parent

##
# Configuration
##

ROARM_M3_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        fix_base=True,
        replace_cylinders_with_capsules=True,
        asset_path=f"{TEMPLATE_ASSETS_DATA_DIR}/urdf/roarm_m3.urdf",
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=8,
            solver_velocity_iteration_count=0,
        ),
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(stiffness=0, damping=0)
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        # No rotation needed — RoArm-M3 URDF has world_to_base_link fixed joint
        # with Z-up orientation already
        joint_pos={
            # Dataset mean positions (degrees -> radians)
            "base_link_to_link1": 0.047,        # 2.71 deg
            "link1_to_link2": 0.704,             # 40.31 deg
            "link2_to_link3": 0.228,             # 13.04 deg
            "link3_to_link4": 1.095,             # 62.75 deg
            "link4_to_link5": -0.046,            # -2.65 deg
            "link5_to_gripper_link": 0.168,      # 9.61 deg
        },
        joint_vel={".*": 0.0},
    ),
    actuators={
        # RoArm-M3 uses ST3235 metal-shell bus servos
        # Stiffness/damping scaled by downstream mass
        #   Base rotation:  moves ALL masses (~0.45 kg total)
        #   Shoulder:       moves upper arm + lower arm + wrist + gripper (~0.19 kg)
        #   Elbow:          moves forearm + wrist + gripper (~0.05 kg)
        #   Wrist pitch:    moves wrist roll + gripper (~0.025 kg)
        #   Wrist roll:     moves gripper only (~0.003 kg)
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[
                "base_link_to_link1",
                "link1_to_link2",
                "link2_to_link3",
                "link3_to_link4",
                "link4_to_link5",
            ],
            effort_limit_sim=1.9,
            velocity_limit_sim=3.14,
            stiffness={
                "base_link_to_link1": 200.0,   # Highest — moves all mass
                "link1_to_link2": 170.0,        # Shoulder — lifts arm
                "link2_to_link3": 120.0,        # Elbow — less mass
                "link3_to_link4": 80.0,         # Wrist pitch
                "link4_to_link5": 50.0,         # Wrist roll — least mass
            },
            damping={
                "base_link_to_link1": 80.0,
                "link1_to_link2": 65.0,
                "link2_to_link3": 45.0,
                "link3_to_link4": 30.0,
                "link4_to_link5": 20.0,
            },
        ),
        "gripper": ImplicitActuatorCfg(
            joint_names_expr=["link5_to_gripper_link"],
            effort_limit_sim=2.5,
            velocity_limit_sim=3.14,
            stiffness=60.0,
            damping=20.0,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of RoArm-M3-Pro robot arm."""
