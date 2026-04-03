#!bin/bash

ORIG_ROOT="original"
OUT_SIM_ROOT="simulated"

MODE=$1   # create | plot | stats

# Create Dataset
if [ "$MODE" == "create" ]; then
    # possible values
    # sensor: [weather, lidar_corrupt, camera_corrupt]
    # fault-type: [fog_stf, fog_wedit, rain, snow, noise, density, blur, exposure_illumination, isp_color, sensor_noise]
    # fault-sub-type: [beam_drop, channel_drop, object_drop, object_background, object_gaussian_rad, object_upsample, scene_background, scene_gaussian_rad, scene_upsample]
    # Note: fault sub type is only applicable for lidar noise and density simulation

    python scripts/create_data.py \
        --orig-root "$ORIG_ROOT" \
        --out-root "$OUT_SIM_ROOT" \
        --sensor "weather" \
        --fault-type "snow" \
        --fault-sub-type ""


# Plot and Visualize images and point clouds with bounding boxes
elif [ "$MODE" == "plot" ]; then
    python scripts/plot_bev_anns.py \
        --nusc-root "$ORIG_ROOT" \
        --sim-root "$OUT_SIM_ROOT" \
        --plot-multiple \
        --show-image \
        --camera-name CAM_FRONT \
        --sample-index 50

# Print weather scatter and drop stats
elif [ "$MODE" == "stats" ]; then
    python scripts/weather_stats.py \
        --nusc-root "$ORIG_ROOT" \
        --fault "fog_stf" \
        --sample-index 50

else
    echo "Invalid mode. Use one of: create | plot | stats"
fi