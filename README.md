# isaac_roarm_m3

An Isaac Lab extension for the Waveshare **RoArm-M3 Pro**, a low-cost 6-axis desktop arm (5 arm joints and a gripper). It packages the robot as an Isaac Lab articulation, registers an end-effector reach task, and trains it with PPO (RSL-RL). It also holds the sponge and table assets I used to replay real teleoperation recordings in simulation.

This repository is the simulation side of my RoArm work. The data collection, VLA fine-tuning and real-robot deployment are described in [roarm-robotics](https://github.com/jaehyeond/roarm-robotics).

## What is here

| Part | File | What it does |
|---|---|---|
| Robot | `src/isaac_roarm_m3/robots/roarm_m3/roarm_m3.py`, `urdf/roarm_m3.urdf` (Waveshare) | URDF-based `ArticulationCfg`. Fixed base, self-collision on. Implicit PD actuators with stiffness and damping scaled by the mass each joint moves (base 200 / 80 down to wrist roll 50 / 20). The initial pose is the mean joint pose of my teleoperation dataset |
| Reach task | `src/isaac_roarm_m3/tasks/reach/` | Manager-based RL env, `Isaac-RoArm-M3-Reach-v0` and a `-Play-v0` variant. 4,096 parallel envs, 60 Hz physics with decimation 2, 12 s episodes |
| PPO config | `tasks/reach/agents/rsl_rl_ppo_cfg.py` | RSL-RL on-policy runner: actor and critic MLP [64, 64], ELU, adaptive learning rate from 1e-3, 1,000 iterations |
| Assets | `src/isaac_roarm_m3/assets/sponge_cfg.py`, `table_cfg.py` | Rigid-box sponge (125 x 47 x 20 mm, about 5 g, measured on the real sponge) and the table, for replaying real recordings in Isaac Sim |
| Scripts | `src/isaac_roarm_m3/scripts/` | `train`, `play` (exports the trained policy as TorchScript and ONNX) and `zero_agent` |

### Reach task design

- **Action:** joint position targets for the 5 arm joints (scale 0.5, offset from the default pose). The gripper is not used in this task.
- **Observation:** joint positions and velocities relative to default (with small uniform noise), the commanded end-effector pose, and the last action.
- **Command:** a target position for `gripper_link`, resampled every 5 s inside a desktop workspace (x -0.15 to 0.15 m, y -0.30 to -0.05 m, z 0.05 to 0.30 m).
- **Reward:** position error (weight -0.2) plus a fine-grained tanh term (0.1). Orientation tracking is turned off to learn position first. Small action-rate and joint-velocity penalties grow through a curriculum after 4,500 steps.
- **Reset:** joint positions scaled by 0.5 to 1.5 of the default pose.

## Install

Requires Linux, Python 3.11, an NVIDIA GPU and Isaac Lab (installed from `pypi.nvidia.com`, with PyTorch for CUDA 12.8). The project uses [uv](https://github.com/astral-sh/uv):

```bash
git clone https://github.com/jaehyeond/isaac_roarm_m3.git
cd isaac_roarm_m3
uv sync
```

If you already have an Isaac Lab environment, `pip install -e .` inside it also works.

## Run

```bash
# Train the reach policy (headless, 4,096 envs)
uv run train --task Isaac-RoArm-M3-Reach-v0 --headless

# Play the latest checkpoint and export policy.pt / policy.onnx
uv run play --task Isaac-RoArm-M3-Reach-Play-v0

# Sanity check the env with zero actions
uv run zero_agent --task Isaac-RoArm-M3-Reach-v0
```

The commands are the entry points defined in `pyproject.toml`. Logs and checkpoints go to `logs/rsl_rl/roarm_m3_reach/`.

## Scope and limits

- This repository contains the reach task only. Later staged tasks (lift, grasp) and the replay scripts live in my private research repository and are not published here.
- No trained checkpoints or result numbers are included. I do not claim a success rate for this task.
- The sponge is a rigid box. Soft-body deformation is out of scope.
- Actuator gains are hand-set from the mass each joint moves. They are not identified from the real ST3235 servos.

## Acknowledgements

Built on [Isaac Lab](https://github.com/isaac-sim/IsaacLab) and its manager-based reach task, and on [RSL-RL](https://github.com/leggedrobotics/rsl_rl). The robot URDF comes from Waveshare's RoArm-M3 Pro model. The code was written with help from AI coding tools.


