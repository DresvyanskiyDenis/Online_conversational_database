from argparse import ArgumentParser
from typing import Tuple

from lib.pyk4a import Config, PyK4A, PyK4ARecord, DepthMode, ColorResolution, FPS, ImageFormat, WiredSyncMode


def device_initialization(color_resolution: ColorResolution = ColorResolution.RES_720P,
        color_format: ImageFormat = ImageFormat.COLOR_MJPG,
        depth_mode: DepthMode = DepthMode.NFOV_2X2BINNED,
        camera_fps: FPS = FPS.FPS_30,
        synchronized_images_only: bool = True,
        depth_delay_off_color_usec: int = 0,
        wired_sync_mode: WiredSyncMode = WiredSyncMode.STANDALONE,
        subordinate_delay_off_master_usec: int = 0,
        disable_streaming_indicator: bool = False,
        device_id:int=0)->Tuple[PyK4A, Config]:


    config = Config(color_resolution = color_resolution,
        color_format = color_format,
        depth_mode = depth_mode,
        camera_fps = camera_fps,
        synchronized_images_only = synchronized_images_only,
        depth_delay_off_color_usec = depth_delay_off_color_usec,
        wired_sync_mode = wired_sync_mode,
        subordinate_delay_off_master_usec = subordinate_delay_off_master_usec,
        disable_streaming_indicator = disable_streaming_indicator)

    device = PyK4A(config=config, device_id=device_id)
    return device, config

def run_recording(device:PyK4A, config:Config, path_to_output_filename:str):
    device.start()
    record = PyK4ARecord(device=device, config=config, path=path_to_output_filename)
    record.create()
    return record




if __name__=="__main__":

    filename = "video_test.mkv"

    device, config=device_initialization()

    record=run_recording(device, config, path_to_output_filename=filename)

    i = 0
    try:
        print("Recording... Press CTRL-C to stop recording.")
        while True:
            capture = device.get_capture()
            record.write_capture(capture)
            i += 1
            if i == 1800:
                break
    except KeyboardInterrupt:
        print("CTRL-C pressed. Exiting.")

    record.flush()
    record.close()
    print(f"{record.captures_count} frames written.")
    