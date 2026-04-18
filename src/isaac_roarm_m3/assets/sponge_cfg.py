"""Sponge asset config for Real→Sim replay of v6 pick task.

Physical sponge (measured 2026-04-14): 125 × 47 × 20 mm, ~5 g, pink color.
Stored vertically (125 mm along +Z) in ep0 of v6 collected_data.

This is a rigid-box approximation; soft-body deformation is out of scope for
Plan Phase 1. Grasp success is judged via contact + Z rise in replay.
"""

import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObjectCfg

# Dimensions (m). x=20mm, y=47mm, z=125mm (vertical).
SPONGE_SIZE = (0.020, 0.047, 0.125)

# Mass (kg). Measured ~5 g for a dry kitchen sponge of this size.
SPONGE_MASS = 0.005

# Pink diffuse to match the physical sample (approximate).
SPONGE_COLOR = (0.95, 0.45, 0.60)

SPONGE_CFG = RigidObjectCfg(
    prim_path="{ENV_REGEX_NS}/Sponge",
    spawn=sim_utils.CuboidCfg(
        size=SPONGE_SIZE,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            solver_position_iteration_count=16,
            solver_velocity_iteration_count=1,
            disable_gravity=False,
            max_depenetration_velocity=1.0,
            linear_damping=0.1,
            angular_damping=0.1,
        ),
        collision_props=sim_utils.CollisionPropertiesCfg(
            contact_offset=0.002,
            rest_offset=0.0,
        ),
        mass_props=sim_utils.MassPropertiesCfg(mass=SPONGE_MASS),
        physics_material=sim_utils.RigidBodyMaterialCfg(
            static_friction=1.0,
            dynamic_friction=1.0,
            restitution=0.0,
        ),
        visual_material=sim_utils.PreviewSurfaceCfg(
            diffuse_color=SPONGE_COLOR,
            roughness=0.8,
            metallic=0.0,
        ),
    ),
    init_state=RigidObjectCfg.InitialStateCfg(pos=(0.3, 0.0, SPONGE_SIZE[2] / 2)),
)
"""Pink sponge rigid-body cfg. Per-episode pose is overridden at reset via
`sponge_poses.json` (see sim_scripts/compute_sponge_poses.py)."""
