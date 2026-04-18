"""Table asset config for v6 pick replay.

Reuses the SeattleLabTable Nucleus asset already used by the reach env.
Table height in sim = 0.0 by default (top of the table is ~0.0 with ground
offset at -0.07). Robot mount offset vs table top is reconciled in Step 3
of the Sim→Real plan (mount height audit vs ESP32 FK pose).
"""

import isaaclab.sim as sim_utils
from isaaclab.assets import AssetBaseCfg
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR

# Matches reach_env_cfg.ReachSceneCfg.table positioning (rotated 90deg about +Z).
TABLE_NUCLEUS_USD = f"{ISAAC_NUCLEUS_DIR}/Props/Mounts/SeattleLabTable/table_instanceable.usd"

TABLE_CFG = AssetBaseCfg(
    prim_path="{ENV_REGEX_NS}/Table",
    spawn=sim_utils.UsdFileCfg(usd_path=TABLE_NUCLEUS_USD),
    init_state=AssetBaseCfg.InitialStateCfg(
        pos=(0.55, 0.0, 0.0),
        rot=(0.70711, 0.0, 0.0, 0.70711),
    ),
)
