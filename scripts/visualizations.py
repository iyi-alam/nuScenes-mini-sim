import os
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from pyquaternion import Quaternion
from nuscenes.nuscenes import NuScenes
from PIL import Image


def get_lidar_and_boxes(nusc, sample, return_camera=False, camera_name="CAM_FRONT"):

    lidar_token = sample["data"]["LIDAR_TOP"]
    sd_record = nusc.get("sample_data", lidar_token)

    lidar_path = os.path.join(nusc.dataroot, sd_record["filename"])

    pc = np.fromfile(lidar_path, dtype=np.float32).reshape((-1, 5))

    cs_record = nusc.get("calibrated_sensor", sd_record["calibrated_sensor_token"])
    ego_pose = nusc.get("ego_pose", sd_record["ego_pose_token"])

    lidar_translation = np.array(cs_record["translation"])
    lidar_rotation = Quaternion(cs_record["rotation"])

    ego_translation = np.array(ego_pose["translation"])
    ego_rotation = Quaternion(ego_pose["rotation"])

    boxes_bev = []

    for ann_token in sample["anns"]:

        box = nusc.get_box(ann_token)

        box.translate(-ego_translation)
        box.rotate(ego_rotation.inverse)

        box.translate(-lidar_translation)
        box.rotate(lidar_rotation.inverse)

        corners = box.corners()

        x = corners[0, [0, 1, 5, 4, 0]]
        y = corners[1, [0, 1, 5, 4, 0]]

        boxes_bev.append((x, y))
    
    if return_camera:
        cam_token = sample["data"][camera_name]
        cam_sd = nusc.get("sample_data", cam_token)

        cam_path = os.path.join(nusc.dataroot, cam_sd["filename"])

        # Load image (PIL or cv2 depending on your pipeline)
        image = Image.open(cam_path).convert("RGB")

        return pc, boxes_bev, image

    return pc, boxes_bev


def plot_bev(pc, boxes, xlim=50, ylim=50, scatter_label = None, save_path=None):

    x = pc[:, 0]
    y =  - pc[:, 1] # need to invert y
    if scatter_label is not None:
        scatter = np.where(pc[:, -1] == scatter_label)

    plt.figure(figsize=(12, 12))



    sc = plt.scatter(x, y, c='gray', cmap="viridis", s=1.0)
    if scatter_label is not None:
        plt.scatter(x[scatter], y[scatter], c="red", s=0.5)

    for bx, by in boxes:
        plt.plot(bx, by, "g-", linewidth=2)

    plt.xlabel("X (meters)", fontsize=30)
    plt.ylabel("Y (meters)", fontsize=30)
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    #plt.title("LiDAR BEV with Ground Truth Boxes")

    plt.axis("equal")
    plt.xlim(-xlim, xlim)
    plt.ylim(-ylim, ylim)

    if save_path:
        plt.savefig(save_path, dpi=300)
    else:
        plt.show()


def plot_bev_multiple(pc1, pc2, boxes1, boxes2, xlim=50, ylim=50, scatter_label=None, save_path=None):

    x1, y1 = pc1[:, 0], pc1[:, 1]
    x2, y2 = pc2[:, 0], pc2[:, 1]

    if scatter_label is not None:
        scatter = np.where(pc2[:, -1] == scatter_label)

    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    # pc1 plot
    axes[0].scatter(x1, y1, c='gray', s=1.0)

    for bx, by in boxes1:
        axes[0].plot(bx, by, "g-", linewidth=2)

    axes[0].set_xlabel("X (meters)", fontsize=20)
    axes[0].set_ylabel("Y (meters)", fontsize=20)
    axes[0].set_title("Point Cloud 1", fontsize=22)

    axes[0].axis("equal")
    axes[0].set_xlim(-xlim, xlim)
    axes[0].set_ylim(-ylim, ylim)

    # pc2 plot
    axes[1].scatter(x2, y2, c='gray', s=1.0)

    if scatter_label is not None:
        axes[1].scatter(x2[scatter], y2[scatter], c="red", s=0.5)

    for bx, by in boxes2:
        axes[1].plot(bx, by, "g-", linewidth=2)

    axes[1].set_xlabel("X (meters)", fontsize=20)
    axes[1].set_ylabel("Y (meters)", fontsize=20)
    axes[1].set_title("Point Cloud 2", fontsize=22)

    axes[1].axis("equal")
    axes[1].set_xlim(-xlim, xlim)
    axes[1].set_ylim(-ylim, ylim)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    else:
        plt.show()


def plot_lidar_camera(pc, boxes, image, xlim=50, ylim=50, scatter_label=None, save_path=None):

    x = pc[:, 0]
    y = pc[:, 1]

    if scatter_label is not None:
        scatter = np.where(pc[:, -1] == scatter_label)

    fig, axes = plt.subplots(1, 2, figsize=(18, 8))

    # -------- Left: LiDAR BEV --------
    axes[0].scatter(x, y, c='gray', s=1.0)

    if scatter_label is not None:
        axes[0].scatter(x[scatter], y[scatter], c="red", s=0.5)

    for bx, by in boxes:
        axes[0].plot(bx, by, "g-", linewidth=2)

    axes[0].set_xlabel("X (meters)", fontsize=18)
    axes[0].set_ylabel("Y (meters)", fontsize=18)
    axes[0].set_title("LiDAR BEV", fontsize=20)

    axes[0].axis("equal")
    axes[0].set_xlim(-xlim, xlim)
    axes[0].set_ylim(-ylim, ylim)

    # -------- Right: Camera --------
    axes[1].imshow(image)
    axes[1].set_title("Camera Image", fontsize=20)
    axes[1].axis("off")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    else:
        plt.show()


def plot_lidar_camera_multiple(
    pc1, pc2, boxes1, boxes2,
    image1, image2,
    xlim=50, ylim=50,
    scatter_label=None,
    save_path=None
):

    x1, y1 = pc1[:, 0], pc1[:, 1]
    x2, y2 = pc2[:, 0], pc2[:, 1]

    if scatter_label is not None:
        scatter = np.where(pc2[:, -1] == scatter_label)

    fig, axes = plt.subplots(2, 2, figsize=(18, 14))

    # -------- Top Left: pc1 --------
    axes[0, 0].scatter(x1, y1, c='gray', s=1.0)

    for bx, by in boxes1:
        axes[0, 0].plot(bx, by, "g-", linewidth=2)

    axes[0, 0].set_title("PC1", fontsize=18)
    axes[0, 0].axis("equal")
    axes[0, 0].set_xlim(-xlim, xlim)
    axes[0, 0].set_ylim(-ylim, ylim)

    # -------- Top Right: image1 --------
    axes[0, 1].imshow(image1)
    axes[0, 1].set_title("Image 1", fontsize=18)
    axes[0, 1].axis("off")

    # -------- Bottom Left: pc2 --------
    axes[1, 0].scatter(x2, y2, c='gray', s=1.0)

    if scatter_label is not None:
        axes[1, 0].scatter(x2[scatter], y2[scatter], c="red", s=0.5)

    for bx, by in boxes2:
        axes[1, 0].plot(bx, by, "g-", linewidth=2)

    axes[1, 0].set_title("PC2", fontsize=18)
    axes[1, 0].axis("equal")
    axes[1, 0].set_xlim(-xlim, xlim)
    axes[1, 0].set_ylim(-ylim, ylim)

    # -------- Bottom Right: image2 --------
    axes[1, 1].imshow(image2)
    axes[1, 1].set_title("Image 2", fontsize=18)
    axes[1, 1].axis("off")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    else:
        plt.show()