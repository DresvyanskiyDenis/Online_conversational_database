import os
from argparse import ArgumentParser
from typing import Tuple

from pyk4a import Config, PyK4A, PyK4ARecord, DepthMode, ColorResolution, FPS, ImageFormat, WiredSyncMode


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
    import argparse
    # parsing
    parser=argparse.ArgumentParser(description='Video and depth data acquisitions using the Azure Kinect.')
    parser.add_argument('--res', action='store', type=int, default=ColorResolution.RES_720P)
    parser.add_argument('--color_format', action='store', type=int, default=ImageFormat.COLOR_MJPG)
    parser.add_argument('--depth_mode', action='store', type=int, default=DepthMode.NFOV_2X2BINNED)
    parser.add_argument('--fps', action='store', type=int, default=FPS.FPS_30)
    parser.add_argument('--synchro', action='store', type=bool, default=True)
    parser.add_argument('--device_id', action='store', type=int, default=0)
    parser.add_argument('--output_path', action='store', type=str, default='results')
    parser.add_argument('--rec_time', action='store', type=int, default=1800) #(30 minutes)
    args=parser.parse_args()
    # device and device config initialization
    device, config=device_initialization(color_resolution=args.res,
                                         color_format=args.color_format,
                                         camera_fps=args.fps,
                                         synchronized_images_only=args.synchro,
                                         device_id=args.device_id)

    # check that all the arguments are passed rightly
    if args.fps==0:
        fps=5
    elif args.fps==1:
        fps=15
    elif args.fps==2:
        fps=30
    else:
        raise Exception("Invalid argument for fps parameter.")

    # create the output directory if needed
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path, exist_ok=True)

    # start recording
    record = run_recording(device, config, path_to_output_filename=os.path.join(args.output_path, "result.mkv"))
    recorded_frames = 0
    try:
        print("Recording... Press CTRL-C to stop recording.")
        while True:
            capture = device.get_capture()
            record.write_capture(capture)
            recorded_frames += 1
            if recorded_frames == args.rec_time*fps:
                break
    except KeyboardInterrupt:
        print("CTRL-C pressed. Exiting.")

    record.flush()
    record.close()
    print(f"{record.captures_count} frames written.")
    