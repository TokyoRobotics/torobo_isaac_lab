# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# Copyright (c) 2024, Tokyo Robotics Inc.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Common functions that can be used to create observation terms.

The functions can be passed to the :class:`omni.isaac.lab.managers.ObservationTermCfg` object to enable
the observation introduced by the function.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from omni.isaac.lab.envs import ManagerBasedEnv, ManagerBasedRLEnv


def gait_phase(env: ManagerBasedEnv):
    return env.gait_phase