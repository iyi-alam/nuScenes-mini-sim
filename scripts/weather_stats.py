"""
Script to compute percentage stats and percentage drop points in different weather faults.
Optionally visualize the scatters
"""
import numpy as np
import os
import argparse
import visualizations as vis
import config
from nuscenes.nuscenes import NuScenes


def weather_stats_and_plot(nusc: NuScenes, sample: dict, simulation_dir, noise_label, drop_label):
    lidar_token = sample["data"]["LIDAR_TOP"]
    sd_record = nusc.get("sample_data", lidar_token)
    sim_path = os.path.join(simulation_dir, sd_record["filename"])
    sim_pc = np.fromfile(sim_path, dtype=np.float32).reshape(-1, 5)

    pc, bev_boxes = vis.get_lidar_and_boxes(nusc, sample)

    noise_pts = np.where(sim_pc[:, -1] == noise_label)
    drop_pts = np.where(sim_pc[:, -1] == drop_label)

    # Print % of noise and drop
    print(f"Percentage of noise points: {len(noise_pts[0]) / len(sim_pc) * 100:.2f}%")
    print(f"Percentage of drop points: {len(drop_pts[0]) / len(sim_pc) * 100:.2f}%")

    # Do potting with scatter
    vis.plot_bev_multiple(pc, sim_pc, bev_boxes, bev_boxes, scatter_label= noise_label, xlim=-75, ylim=-75)



if __name__  == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--nusc-root", type=str, help="Path to the NuScenes dataset", default="original")
    parser.add_argument("--fault", type=str, help="Type of fault to analyze", choices=["fog", "rain", "snow"])
    parser.add_argument("--sample-index", type=int, help="Index of the sample to analyze", default=0)
    args = parser.parse_args()

    
    fault_dict = getattr(config.LiDARSimulations, args.fault)
    simulation_dir = fault_dict["simulation_dir"]
    noise_label = fault_dict["noise_label"]
    drop_label = fault_dict["drop_label"]

    nusc_orig = NuScenes(version="v1.0-mini", dataroot=args.nusc_root)
    sample = nusc_orig.sample[args.sample_index]
    print(f"Processing data for fault: {args.fault} and sample: {args.sample_index}")

    weather_stats_and_plot(nusc_orig, sample, simulation_dir, noise_label, drop_label)



