"""
Configurations for helping in analysis and visualization
"""

class LiDARSimulations:
    fog = dict(
        noise_label=1,
        drop_label=1,
        simulation_dir = "weather/fog_stf"
    )
    snow = dict(
        noise_label=2,
        drop_label=3,
        simulation_dir = "weather/snow"
    )
    rain = dict(
        noise_label=1,
        drop_label=0,
        simulation_dir = "weather/rain"
    )
    density = dict(
        beam_drop=dict(simulation_dir = "lidar_corrupt/density/beam_drop"),
        channel_drop=dict(simulation_dir = "lidar_corrupt/density/channel_drop"),
        object_drop=dict(simulation_dir = "lidar_corrupt/density/object_drop")
    )
    noise = dict(
        object_background=dict(simulation_dir = "lidar_corrupt/noise/object_background"),
        object_gaussian_rad=dict(simulation_dir = "lidar_corrupt/noise/object_gaussian_rad"),
        object_upsample=dict(simulation_dir = "lidar_corrupt/noise/object_upsample"),
        scene_background=dict(simulation_dir = "lidar_corrupt/noise/scene_background"),
        scene_gaussian_rad=dict(simulation_dir = "lidar_corrupt/noise/scene_gaussian_rad"),
        scene_upsample=dict(simulation_dir = "lidar_corrupt/noise/scene_upsample")
    )
