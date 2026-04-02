"""
General script to plot BEV map of lidar point cloud to visualize bounding boxes and effect of different simulations done on point cloud
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import visualizations as vis
from nuscenes.nuscenes import NuScenes
import argparse


def plot_single_bev(nusc: NuScenes, sample: dict, save_dir: str = None, show_image = False, camera_name: str = "CAM_FRONT"):
    result = vis.get_lidar_and_boxes(nusc, sample, return_camera=show_image, camera_name=camera_name)

    if not show_image:
        pc, bev_boxes = result
        vis.plot_bev(pc, bev_boxes, save_path=os.path.join(save_dir, f"{sample['token']}.png") if save_dir else None)
    else:
        pc, bev_boxes, image = result
        vis.plot_lidar_camera(pc, bev_boxes, image)

def plot_multiple_bev(nusc1: NuScenes, nusc2: NuScenes, sample: dict, save_dir: str = None, show_image = False, camera_name: str = "CAM_FRONT"):
    result1 = vis.get_lidar_and_boxes(nusc1, sample, return_camera=show_image, camera_name=camera_name)
    result2 = vis.get_lidar_and_boxes(nusc2, sample, return_camera=show_image, camera_name=camera_name)

    if not show_image:
        pc1, bev_boxes1 = result1
        pc2, bev_boxes2 = result2
        vis.plot_bev_multiple(pc1, pc2, bev_boxes1, bev_boxes2, save_path=os.path.join(save_dir, f"{sample['token']}.png") if save_dir else None)
    else:
        pc1, bev_boxes1, image1 = result1
        pc2, bev_boxes2, image2 = result2
        vis.plot_lidar_camera_multiple(pc1, pc2, bev_boxes1, bev_boxes2, image1, image2, save_path=os.path.join(save_dir, f"{sample['token']}.png") if save_dir else None)




if __name__ == "__main__":
   
    parser = argparse.ArgumentParser()

    parser.add_argument("--nusc-root", dest="nusc_root",
                        help="Path to NuScenes data", default="original")

    parser.add_argument("--sim-root", dest="sim_root",
                        help="Path to simulated data", default="simulated")

    parser.add_argument("--save-dir", dest="save_dir",
                        help="Directory to save plots", default=None)

    parser.add_argument("--plot-multiple", dest="plot_multiple",
                        help="Plot multiple BEV images", action="store_true")

    parser.add_argument("--show-image", dest="show_image",
                        help="Show camera image", action="store_true")

    parser.add_argument("--camera-name", choices=[
                            "CAM_FRONT", "CAM_FRONT_LEFT", "CAM_FRONT_RIGHT",
                            "CAM_BACK", "CAM_BACK_LEFT", "CAM_BACK_RIGHT"
                        ], default="CAM_FRONT")

    parser.add_argument("--sample-index", dest="sample_index",
                        help="Index of the sample to plot", type=int, default=None)

    args = parser.parse_args()
   
    nusc_orig = NuScenes(version="v1.0-mini", dataroot=args.nusc_root)

    # chose a random_sample
    if args.sample_index is None:
        sample = np.random.choice(nusc_orig.sample)
    else:
        sample = nusc_orig.sample[args.sample_index]

    if not args.plot_multiple:
        plot_single_bev(nusc_orig, sample, save_dir=args.save_dir, show_image=args.show_image, camera_name=args.camera_name)
    else:
        assert args.sim_root is not None, "Simulated data root path is required for multiple BEV plotting"
        nusc_sim = NuScenes(version="v1.0-mini", dataroot=args.sim_root)
        plot_multiple_bev(nusc_orig, nusc_sim, sample, save_dir=args.save_dir, show_image=args.show_image, camera_name=args.camera_name)
    
