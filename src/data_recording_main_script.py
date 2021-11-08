import subprocess
import os
import src.data_recording_config as rec_config

if __name__ == '__main__':
    cmd_for_kinect = "python video_acquisition.py --res %i --color_format %i --depth_mode %i --fps %i " \
                     "--synchro %r --device_id %i --output_path %s --rec_time %i"% \
                     (rec_config.KINECT_RESOLUTION, rec_config.KINECT_IMAGE_FORMAT, rec_config.KINECT_DEPTH_MODE,
                      rec_config.KINECT_FPS, rec_config.KINECT_SYNCHRO, rec_config.KINECT_DEVICE_ID,
                      rec_config.KINECT_OUTPUT_PATH, rec_config.KINECT_RECORDING_TIME)


    cmd_for_kinect_audio = "python audio_recording.py --format %s --rate %i --num_channels %i " \
                           "--device_index %i --chunk_size %i --time %i " \
                           "--output_path %s --output_filename %s"%(rec_config.AUDIO_KINECT_FORMAT,rec_config.AUDIO_KINECT_RATE,
                                                                    rec_config.AUDIO_KINECT_NUM_CHANNELS, rec_config.AUDIO_KINECT_DEVICE_INDEX,
                                                                    rec_config.AUDIO_KINECT_CHUNK_SIZE, rec_config.AUDIO_KINECT_RECORDING_TIME,
                                                                    rec_config.AUDIO_KINECT_OUTPUT_PATH, rec_config.AUDIO_KINECT_OUTPUT_FILENAME)

    # add cmd for the external audio recorded (microphone)


    # run recording processes in parallel
    processes = []
    p=subprocess.Popen(cmd_for_kinect, shell=True)
    processes.append(p)
    p=subprocess.Popen(cmd_for_kinect_audio, shell=True)
    processes.append(p)
    for process in processes:
        process.wait()