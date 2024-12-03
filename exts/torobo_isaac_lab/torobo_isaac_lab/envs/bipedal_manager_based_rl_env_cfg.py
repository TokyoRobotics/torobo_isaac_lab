# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# Copyright (c) 2024, Tokyo Robotics Inc.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from dataclasses import MISSING

from omni.isaac.lab.utils import configclass

from omni.isaac.lab.envs.manager_based_rl_env_cfg import ManagerBasedRLEnvCfg


@configclass
class BipedalManagerBasedRLEnvCfg(ManagerBasedRLEnvCfg):
    """Configuration for a reinforcement learning environment with the manager-based workflow."""

    gait_step_num: int = MISSING

