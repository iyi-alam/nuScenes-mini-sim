import os
import shutil
from pathlib import Path
import argparse


def copy_file_with_fallback(src_sim, src_orig, dst):
    """
    Copy file from sim if exists, else from original.
    """
    if src_sim.exists():
        shutil.copy2(src_sim, dst)
    elif src_orig.exists():
        shutil.copy2(src_orig, dst)
    else:
        print(f"[WARNING] Missing file in both: {src_sim} | {src_orig}")


def merge_sensor_folder(folder_name, orig_root, sim_root, out_root):
    """
    Merge samples/sweeps with fallback logic.
    """
    orig_dir = Path(orig_root) / folder_name
    sim_dir = Path(sim_root) / folder_name
    out_dir = Path(out_root) / folder_name

    for root, _, files in os.walk(orig_dir):
        rel_path = Path(root).relative_to(orig_dir)

        for file in files:
            orig_file = Path(root) / file
            sim_file = sim_dir / rel_path / file
            out_file = out_dir / rel_path / file

            out_file.parent.mkdir(parents=True, exist_ok=True)
            copy_file_with_fallback(sim_file, orig_file, out_file)


def copy_folder(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def create_nuscenes_mini_like(orig_root, sim_root, out_root):
    orig_root = Path(orig_root)
    sim_root = Path(sim_root)
    out_root = Path(out_root)

    out_root.mkdir(parents=True, exist_ok=True)

    print("Merging samples...")
    merge_sensor_folder("samples", orig_root, sim_root, out_root)

    print("Merging sweeps...")
    merge_sensor_folder("sweeps", orig_root, sim_root, out_root)

    print("Copying maps...")
    copy_folder(orig_root / "maps", out_root / "maps")

    print("Copying metadata (v1.0-mini)...")
    copy_folder(orig_root / "v1.0-mini", out_root / "v1.0-mini")

    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a NuScenes mini-like dataset with simulation data.")
    parser.add_argument("--orig-root", help="Path to the original NuScenes data.", default="original")
    parser.add_argument("--out-root", help="Path to the output directory.", default="simulated")
    parser.add_argument("--sensor", help="Path to the sensor simulation data.")
    parser.add_argument("--fault-type", help="Type of fault to gather data from.")
    parser.add_argument("--fault-sub-type", help="Sub-type of fault to gather data from (only for lidar noise and density).", default = "")

    args = parser.parse_args()

    sim_root = os.path.join(args.sensor, args.fault_type, args.fault_sub_type)

    create_nuscenes_mini_like(
        orig_root=args.orig_root,
        sim_root=sim_root,
        out_root=args.out_root
    )