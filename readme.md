# Introduction

This repository contains nuScenes-mini dataset simulated with wide variety of faults in both LiDAR and Camera useful for use in downstream peception tasks that utilizes multiple sensors (eg., Sensor Fusion) to study the robustness of such systems against input data corruption. We simulate mainly two kind of faults - 
    1. Weather Faults
    2. Sensor Specific Faults
        A. LiDAR only faults
        b. Camera only faults



# Understanding the Dataset
## Environment Setup
Please follow instrcutions given in [nuScenes-devkit](https://github.com/nutonomy/nuscenes-devkit) to setup environment necessary for running scripts on this repo.

## Directory Structure
Please download the data from [nuScenes-mini-sim](https://drive.google.com/drive/folders/1KNyf5MGHZB9c8QzYXIlYEr7o-OfYXo7d). The dataset structure is as follows - 

```text
nuScenes-mini-Sim
    ├── lidar_corrupt
    |        ├── density
    |        │   ├── beam_drop
    |        │   ├── channel_drop
    |        │   └── object_drop
    |        └── noise
    |            ├── object_background
    |            ├── object_gaussian_rad
    |            ├── object_upsample
    |            ├── scene_background
    |            ├── scene_gaussian_rad
    |            └── scene_upsample
    ├── original
    │   ├── maps
    │   ├── samples
    │   ├── sweeps
    │   └── v1.0-mini
    ├── readme.md
    └── weather
        ├── fog
        ├── rain
        └── snow
```

Within each folder we have same directory structure as the original file. For example, if we need fog simulated nuScenes-mini dataset, the corresponding samples and sweeps can be found at ```weather/fog```, similarly for channel drop simulation, it can be found at ```lidar_corrupt/density/channel_drop```.

## Creating Official nuScenes Structure from Simulated Dataset
Note that the respective folders do not contain full dataset as in nuScenes-mini. They only contains the parts which are affected by simulation. For example, in weather faults, the simulated folders contains both camera and lidar files while the sensor specific simulated folders such as ```lidar_corrupt``` and ```camera_corrupt``` only contains files associated with that sensor. To create full nuScenes-mini as is the original version with desired simulation, run the following script.

```bash
bash create_dataset.sh
```

This will create a folder ```simulated``` with official directory structure but some sensor files replaced with desired simulated files.