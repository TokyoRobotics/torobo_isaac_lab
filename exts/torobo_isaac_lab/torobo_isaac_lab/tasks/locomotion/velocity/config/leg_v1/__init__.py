# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# Copyright (c) 2024, Tokyo Robotics Inc.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import gymnasium as gym

from . import agents, flat_env_cfg, rough_env_cfg

##
# Register Gym environments.
##

gym.register(
    id="Isaac-Velocity-Flat-Torobo-Leg-v1-v0",
    entry_point="torobo_isaac_lab.envs:BipedalManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": flat_env_cfg.ToroboLegV1FlatEnvCfg,
        "rsl_rl_cfg_entry_point": agents.rsl_rl_cfg.ToroboLegV1FlatPPORunnerCfg,
    },
)


gym.register(
    id="Isaac-Velocity-Flat-Torobo-Leg-v1-Play-v0",
    entry_point="torobo_isaac_lab.envs:BipedalManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": flat_env_cfg.ToroboLegV1FlatEnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": agents.rsl_rl_cfg.ToroboLegV1FlatPPORunnerCfg,
    },
)
