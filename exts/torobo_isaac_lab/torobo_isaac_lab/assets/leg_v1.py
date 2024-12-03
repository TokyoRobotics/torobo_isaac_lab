# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# Copyright (c) 2024, Tokyo Robotics Inc.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration for Torobo Leg V1 robot.
"""

import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.actuators import ActuatorNetMLPCfg, DCMotorCfg, ImplicitActuatorCfg
from omni.isaac.lab.assets.articulation import ArticulationCfg
from omni.isaac.lab.utils.assets import ISAACLAB_NUCLEUS_DIR

##
# Configuration - Actuators.
##

TOROBO_LEG_V1_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path="exts/torobo_isaac_lab/data/usd/leg_v1.usd",
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False, solver_position_iteration_count=4, solver_velocity_iteration_count=4
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 1.19082),
        joint_pos={
            "(right|left)_leg_joint_1": 0.3911798987199639,
            "right_leg_joint_2": 0.0012423084323551653,
            "left_leg_joint_2": -0.0012423084323551653,
            "right_leg_joint_3": 0.0005505230847620535,
            "left_leg_joint_3": -0.0005505230847620535,
            "(right|left)_leg_joint_4": 0.792139781767314,
            "(right|left)_leg_joint_5": -0.401659587652539,
            "right_leg_joint_6": -0.0004349101512974649,
            "left_leg_joint_6": 0.0004349101512974649,
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        "legs": ImplicitActuatorCfg(
            joint_names_expr=["right_leg_joint_[^6]", "left_leg_joint_[^6]"],
            effort_limit=300,
            velocity_limit=100.0,
            stiffness={
                "right_leg_joint_[^6]": 150.0,
                "left_leg_joint_[^6]": 150.0,
            },
            damping={
                "right_leg_joint_[^6]": 5.0,
                "left_leg_joint_[^6]": 5.0,
            },
        ),
        "feet": ImplicitActuatorCfg(
            joint_names_expr=[".*_leg_joint_6"],
            effort_limit=100,
            velocity_limit=100.0,
            stiffness={".*_leg_joint_6": 20.0},
            damping={".*_leg_joint_6": 4.0},
        ),
    },
)
"""Configuration for the Leg V1 robot."""


TOROBO_LEG_V1_MINIMAL_CFG = TOROBO_LEG_V1_CFG.copy()
TOROBO_LEG_V1_MINIMAL_CFG.spawn.usd_path = "exts/torobo_isaac_lab/data/usd/leg_v1.usd"