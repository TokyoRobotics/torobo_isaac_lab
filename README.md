# torobo_isaac_lab

[![IsaacSim](https://img.shields.io/badge/IsaacSim-4.2.0-silver.svg)](https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html)
[![Isaac Lab](https://img.shields.io/badge/IsaacLab-1.2.0-silver)](https://isaac-sim.github.io/IsaacLab)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://docs.python.org/3/whatsnew/3.10.html)
[![Linux platform](https://img.shields.io/badge/platform-linux--64-orange.svg)](https://releases.ubuntu.com/20.04/)
[![Windows platform](https://img.shields.io/badge/platform-windows--64-orange.svg)](https://www.microsoft.com/en-us/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/license/mit)

## Overview

This repository is an extension project based on Isaac Lab. It allows you to develop in an isolated environment, outside of the core Isaac Lab repository.

If you want to run the trained policy in MuJoCo, please refer to [torobo_mujoco](https://github.com/TokyoRobotics/torobo_mujoco).

## Installation

- Install Isaac Sim version 4.2.0 by following the [installation guide](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_workstation.html).

- Install Isaac Lab by following the [installation guide](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html). We recommend using the conda installation as it simplifies calling Python scripts from the terminal. If you want to install by binary-install, please clone versin 1.2.0 by adding `-b v1.2.0`.

- Clone the repository separately from the Isaac Lab installation (i.e. outside the `IsaacLab` directory):

```bash
git clone https://github.com/TokyoRobotics/torobo_isaac_lab.git
```

- Then, using a python interpreter that has Isaac Lab installed, install the library

```bash
python -m pip install -e exts/torobo_isaac_lab
```

- You can verify that the extension is correctly installed by running the following command:

```bash
python scripts/rsl_rl/train.py --task=Isaac-Velocity-Flat-Torobo-Leg-v1-v0 --num_envs 4
```

<details>
<summary>Set up IDE (Optional)</summary>

To setup the IDE, please follow these instructions:

- Run VSCode Tasks, by pressing `Ctrl+Shift+P`, selecting `Tasks: Run Task` and running the `setup_python_env` in the drop down menu. When running this task, you will be prompted to add the absolute path to your Isaac Sim installation.

If everything executes correctly, it should create a file .python.env in the `.vscode` directory. The file contains the python paths to all the extensions provided by Isaac Sim and Omniverse. This helps in indexing all the python modules for intelligent suggestions while writing code.
</details>

<details>
<summary>Setup as Omniverse Extension (Optional)</summary>

We provide an example UI extension that will load upon enabling your extension defined in `exts/torobo_isaac_lab/torobo_isaac_lab/ui_extension_example.py`. For more information on UI extensions, enable and check out the source code of the `omni.isaac.ui_template` extension and refer to the introduction on [Isaac Sim Workflows 1.2.3. GUI](https://docs.omniverse.nvidia.com/isaacsim/latest/introductory_tutorials/tutorial_intro_workflows.html#gui).

To enable your extension, follow these steps:

1. **Add the search path of your repository** to the extension manager:
    - Navigate to the extension manager using `Window` -> `Extensions`.
    - Click on the **Hamburger Icon** (☰), then go to `Settings`.
    - In the `Extension Search Paths`, enter the absolute path to `IsaacLabExtensionTemplate/exts`
    - If not already present, in the `Extension Search Paths`, enter the path that leads to Isaac Lab's extension directory directory (`IsaacLab/source/extensions`)
    - Click on the **Hamburger Icon** (☰), then click `Refresh`.

2. **Search and enable your extension**:
    - Find your extension under the `Third Party` category.
    - Toggle it to enable your extension.
</details>

## Example

Leg v1 model bipedal walking (Leg v1 model is now under research and development and is not currently scheduled for sale)

<img src="./doc/leg_v1_walk.gif" width="400">


```bash
# train
python scripts/rsl_rl/train.py --task=Isaac-Velocity-Flat-Torobo-Leg-v1-v0 --headless

# play
python scripts/rsl_rl/play.py --task=Isaac-Velocity-Flat-Torobo-Leg-v1-Play-v0 --num_envs 4
```

If you want to play on the specific checkpoint, please execute the following command.

The checkpoint data exists in logs/rsl_rl/torobo_leg_v1_flat/(date)/model_(iteration_num).pt .
```bash
python scripts/rsl_rl/play.py --task=Isaac-Velocity-Flat-Torobo-Leg-v1-Play-v0 --num_envs 4 --load_run (date) --checkpoint model_(iteration_num).pt
```

If you want to resume from the specific checkpoint, please execute the following command.
```bash
python scripts/rsl_rl/train.py --task=Isaac-Velocity-Flat-Torobo-Leg-v1-v0 --resume --load_run (date) --checkpoint model_(iteration_num).pt
```

If you want to extract the trained policy, please play on the specific checkpoint (mode_1000.pt is recommended) and use the policy in logs/rsl_rl/torobo_leg_v1_flat/(date)/exported .


## Code formatting

We have a pre-commit template to automatically format your code.
To install pre-commit:

```bash
pip install pre-commit
```

Then you can run pre-commit with:

```bash
pre-commit run --all-files
```

## Troubleshooting

### Pylance Missing Indexing of Extensions

In some VsCode versions, the indexing of part of the extensions is missing. In this case, add the path to your extension in `.vscode/settings.json` under the key `"python.analysis.extraPaths"`.

```json
{
    "python.analysis.extraPaths": [
        "<path-to-ext-repo>/exts/torobo_isaac_lab"
    ]
}
```

### Pylance Crash

If you encounter a crash in `pylance`, it is probable that too many files are indexed and you run out of memory.
A possible solution is to exclude some of omniverse packages that are not used in your project.
To do so, modify `.vscode/settings.json` and comment out packages under the key `"python.analysis.extraPaths"`
Some examples of packages that can likely be excluded are:

```json
"<path-to-isaac-sim>/extscache/omni.anim.*"         // Animation packages
"<path-to-isaac-sim>/extscache/omni.kit.*"          // Kit UI tools
"<path-to-isaac-sim>/extscache/omni.graph.*"        // Graph UI tools
"<path-to-isaac-sim>/extscache/omni.services.*"     // Services tools
...
```
