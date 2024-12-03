# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# Copyright (c) 2024, Tokyo Robotics Inc.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

# needed to import for allowing type-hinting: np.ndarray | None
from __future__ import annotations

import gymnasium as gym
import math
import numpy as np
import torch
from collections.abc import Sequence
from typing import Any, ClassVar

from omni.isaac.version import get_version

from omni.isaac.lab.managers import CommandManager, CurriculumManager, RewardManager, TerminationManager

from omni.isaac.lab.envs.common import VecEnvStepReturn
from omni.isaac.lab.envs.manager_based_rl_env import ManagerBasedRLEnv
from torobo_isaac_lab.envs.bipedal_manager_based_rl_env_cfg import BipedalManagerBasedRLEnvCfg


class BipedalManagerBasedRLEnv(ManagerBasedRLEnv, gym.Env):
    """The superclass for the manager-based workflow reinforcement learning-based environments.

    This class inherits from :class:`ManagerBasedEnv` and implements the core functionality for
    reinforcement learning-based environments. It is designed to be used with any RL
    library. The class is designed to be used with vectorized environments, i.e., the
    environment is expected to be run in parallel with multiple sub-environments. The
    number of sub-environments is specified using the ``num_envs``.

    Each observation from the environment is a batch of observations for each sub-
    environments. The method :meth:`step` is also expected to receive a batch of actions
    for each sub-environment.

    While the environment itself is implemented as a vectorized environment, we do not
    inherit from :class:`gym.vector.VectorEnv`. This is mainly because the class adds
    various methods (for wait and asynchronous updates) which are not required.
    Additionally, each RL library typically has its own definition for a vectorized
    environment. Thus, to reduce complexity, we directly use the :class:`gym.Env` over
    here and leave it up to library-defined wrappers to take care of wrapping this
    environment for their agents.

    Note:
        For vectorized environments, it is recommended to **only** call the :meth:`reset`
        method once before the first call to :meth:`step`, i.e. after the environment is created.
        After that, the :meth:`step` function handles the reset of terminated sub-environments.
        This is because the simulator does not support resetting individual sub-environments
        in a vectorized environment.

    """

    is_vector_env: ClassVar[bool] = True
    """Whether the environment is a vectorized environment."""
    metadata: ClassVar[dict[str, Any]] = {
        "render_modes": [None, "human", "rgb_array"],
        "isaac_sim_version": get_version(),
    }
    """Metadata for the environment."""

    cfg: BipedalManagerBasedRLEnvCfg
    """Configuration for the environment."""

    def __init__(self, cfg: BipedalManagerBasedRLEnvCfg, render_mode: str | None = None, **kwargs):
        """Initialize the environment.

        Args:
            cfg: The configuration for the environment.
            render_mode: The render mode for the environment. Defaults to None, which
                is similar to ``"human"``.
        """
        # initialize the base class to setup the scene.

        # define episode length for gait phase here
        self.episode_length_buf = torch.zeros(cfg.scene.num_envs, device=cfg.sim.device, dtype=torch.long)
        super().__init__(cfg=cfg)

    """
    Properties.
    """

    @property
    def gait_phase(self) -> torch.Tensor:
        # gait time length (s) = step time length(0.02 s) * gait_step_num
        # gait time legnth means the time length of one gait cycle (ex. right foot stance -> left foot stance -> right foot stance)
        phase = torch.sin(2 * torch.pi * self.episode_length_buf / self.cfg.gait_step_num)

        stance_mask = torch.zeros((self.num_envs, 2), device=self.device)
        # left foot stance
        stance_mask[:, 0] = phase >= 0
        # right foot stance
        stance_mask[:, 1] = phase < 0
        # Double support phase
        stance_mask[torch.abs(phase) < 0.1] = 1
        return stance_mask