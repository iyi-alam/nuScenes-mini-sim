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
    |
    |── camera_corrupt/
    |       ├── blur
    |       ├── exposure_illumination
    |       ├── isp_color
    |       └── sensor_noise
    |
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

Within each folder we have same directory structure as the original file. For example, if we need fog simulated nuScenes-mini dataset, the corresponding samples and sweeps can be found at ```weather/fog_stf```, similarly for channel drop simulation, it can be found at ```lidar_corrupt/density/channel_drop```.

## Creating Official nuScenes Structure from Simulated Dataset
Note that the respective folders do not contain full dataset as in nuScenes-mini. They only contains the parts which are affected by simulation. For example, in weather faults, the simulated folders contains both camera and lidar files while the sensor specific simulated folders such as ```lidar_corrupt``` and ```camera_corrupt``` only contains files associated with that sensor. To create full nuScenes-mini as is the original version with desired simulation, run the following script.

```bash
bash main.sh create
```

This will create a folder ```simulated``` with official directory structure but some sensor files replaced with desired simulated files. You can make desired edits in ```main.sh``` script to specify the fault to be consolidated. 

## Visualizations
To visualize the effect of simulations on point cloud and images, we have provided some additional code under ```scripts``` folder. All of them can independently be run as well as they can be run from ```main.sh``` also. 

> To visualize the original and simulated point cloud along with desired camer view, run - 

```bash
bash main.sh plot
```
Or independently run the python with desired arguments
```bash
python scripts/plot_bev_anns.py \
        --nusc-root "original" \
        --sim-root "simulated" \
        --plot-multiple \
        --show-image \
        --camera-name CAM_FRONT \
        --sample-index 50
```
please note that you need to consildate the simulated nuScenes-mini first by runnning ```bash main.sh create``` command as mentioned earlier.

> You can also check the percentage drop in point and percentage noise scatter in lidar weather simulations along with a plot that explicitely shows noise scatters in red color on BEV plot by running the command - 

```bash
bash main.sh stats
```
Or independently running the python command - 
```bash 
python scripts/weather_stats.py \
        --nusc-root "original" \
        --fault "fog_stf" \
        --sample-index 50
```
