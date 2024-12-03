# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# Copyright (c) 2024, Tokyo Robotics Inc.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import torch
from typing import TYPE_CHECKING

from omni.isaac.lab.assets import Articulation
from omni.isaac.lab.managers import SceneEntityCfg
from omni.isaac.lab.sensors import ContactSensor
from omni.isaac.lab.utils.math import quat_rotate_inverse, yaw_quat, quat_error_magnitude, yaw_quat

if TYPE_CHECKING:
    from omni.isaac.lab.envs import ManagerBasedRLEnv

def feet_orientation(env, sensor_cfg: SceneEntityCfg, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot")) -> torch.Tensor:
    """ Penalize the difference between the orientation of the feet and the root """
    asset = env.scene[asset_cfg.name]
    body_quat = asset.data.body_quat_w[:, asset_cfg.body_ids, :].reshape(-1, 4)
    root_quat = asset.data.root_quat_w
    angle_diff = torch.abs(quat_error_magnitude(body_quat, root_quat))
    return angle_diff

def feet_clock_frc(env, sensor_cfg: SceneEntityCfg, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot")) -> torch.Tensor:
    """ Reward for the contact force of the feet during the gait cycle """
    contact_sensor: ContactSensor = env.scene.sensors[sensor_cfg.name]
    stance_mask = env.gait_phase
    swing_mask = -1 * (1 - stance_mask)
    # stance_mask = 1, swing_mask = -1
    stance_swing_mask = stance_mask + swing_mask
    asset = env.scene[asset_cfg.name]
    total_mass = torch.sum(asset.data.default_mass[0])
    max_frc = 0.5 * total_mass * 9.81
    normed_frc = torch.min(contact_sensor.data.net_forces_w_history[:, :, sensor_cfg.body_ids, :].norm(p=2, dim=-1).max(dim=1)[0], max_frc) / max_frc
    rew_normed_frc = normed_frc * stance_swing_mask
    return rew_normed_frc.mean(dim=1)

def feet_clock_vel(env, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot")) -> torch.Tensor:
    """ Reward for the velocity of the feet during the gait cycle """
    stance_mask = env.gait_phase
    swing_mask = -1 * (1 - stance_mask)
    # stance_mask = -1, swing_mask = 1 (reverse of feet_clock_frc)
    stance_swing_mask = stance_mask + swing_mask
    stance_swing_mask *= -1
    asset = env.scene[asset_cfg.name]
    max_vel = torch.tensor(0.3, device="cuda")
    body_vel = asset.data.body_lin_vel_w[:, asset_cfg.body_ids, :]
    normed_vel = torch.min(body_vel.norm(p=2, dim=-1), max_vel) / max_vel
    rew_normed_vel = normed_vel * stance_swing_mask
    return rew_normed_vel.mean(dim=1)

def feet_keep_distance(env, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot")) -> torch.Tensor:
    """ Penalize if the distance between the two feet about the y-axis is not in the range of 0.22m to 0.32m """
    asset = env.scene[asset_cfg.name]
    body_pos = asset.data.body_pos_w[:, asset_cfg.body_ids, :]
    root_pos = asset.data.root_pos_w[:, :]
    root_quat = yaw_quat(asset.data.root_quat_w)
    root_to_body_1 = body_pos[:, 0, :].squeeze(1) - root_pos[:, :]
    root_to_body_2 = body_pos[:, 1, :].squeeze(1) - root_pos[:, :]
    root_to_body_1_b = quat_rotate_inverse(root_quat, root_to_body_1)
    root_to_body_2_b = quat_rotate_inverse(root_quat, root_to_body_2)
    feet_y_distance = torch.abs(root_to_body_1_b[:, 1] - root_to_body_2_b[:, 1])
    rew = torch.where((feet_y_distance > 0.11 * 2) & (feet_y_distance < 0.16 * 2), 0, 1)
    return rew