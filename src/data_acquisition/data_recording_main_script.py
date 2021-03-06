import os
import sys

import pyaudio

module_path = os.path.abspath(os.getcwd())
if module_path not in sys.path:
    sys.path.append(module_path)

import subprocess
import src.data_acquisition.data_recording_config as rec_config
import shutil

from src.data_acquisition.anonymization import generate_pseudoanonimization_time_room


def get_device_id_by_name(name:str)->int:
    # automatic device id recognition using specified name
    audio = pyaudio.PyAudio()
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    device_id = 0
    device_name = name
    for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            if device_name in audio.get_device_info_by_host_api_device_index(0, i).get('name').lower():
                device_id = i
                break
    audio.terminate()
    return device_id



if __name__ == '__main__':
    import argparse
    # parsing
    parser = argparse.ArgumentParser(description='Data recording with Azure Kinect and external Microphone.')
    parser.add_argument('--room_name', action='store', type=str, required=True)
    parser.add_argument('--session_num', action='store', type=str, required=True)
    parser.add_argument('--date', action='store', type=str, required=True)
    parser.add_argument('--output_path', action='store', type=str, required=True)
    args = parser.parse_args()

    # run cmd command for the kinect video and depth recording
    cmd_for_kinect = "python src\\video_acquisition.py --res %i --color_format %i --depth_mode %i --fps %i " \
                     "--synchro %r --device_id %i --output_path %s --rec_time %i"% \
                     (rec_config.KINECT_RESOLUTION, rec_config.KINECT_IMAGE_FORMAT, rec_config.KINECT_DEPTH_MODE,
                      rec_config.KINECT_FPS, rec_config.KINECT_SYNCHRO, rec_config.KINECT_DEVICE_ID,
                      rec_config.KINECT_OUTPUT_PATH, rec_config.KINECT_RECORDING_TIME)

    # add cmd for the kinect audio recording (microphone array)
    kinect_audio_device_id=get_device_id_by_name('kinect')
    cmd_for_kinect_audio = "python src\\audio_recording.py --format %s --rate %i --num_channels %i " \
                           "--device_index %i --chunk_size %i --time %i " \
                           "--output_path %s --output_filename %s"%(rec_config.AUDIO_KINECT_FORMAT, rec_config.AUDIO_KINECT_RATE,
                                                                    rec_config.AUDIO_KINECT_NUM_CHANNELS, kinect_audio_device_id,
                                                                    rec_config.AUDIO_KINECT_CHUNK_SIZE, rec_config.AUDIO_KINECT_RECORDING_TIME,
                                                                    rec_config.AUDIO_KINECT_OUTPUT_PATH, rec_config.AUDIO_KINECT_OUTPUT_FILENAME)

    # add cmd for the external audio recorded (microphone)
    external_microphone_device_id = get_device_id_by_name('sennheiser')
    cmd_for_external_audio = "python src\\audio_recording.py --format %s --rate %i --num_channels %i " \
                           "--device_index %i --chunk_size %i --time %i " \
                           "--output_path %s --output_filename %s"%(rec_config.AUDIO_MICROPHONE_FORMAT, rec_config.AUDIO_MICROPHONE_RATE,
                                                                    rec_config.AUDIO_MICROPHONE_NUM_CHANNELS, external_microphone_device_id,
                                                                    rec_config.AUDIO_MICROPHONE_CHUNK_SIZE, rec_config.AUDIO_MICROPHONE_RECORDING_TIME,
                                                                    rec_config.AUDIO_MICROPHONE_OUTPUT_PATH, rec_config.AUDIO_MICROPHONE_OUTPUT_FILENAME)

    # run recording processes in parallel
    processes = []
    p=subprocess.Popen(cmd_for_kinect, shell=True)
    processes.append(p)
    p=subprocess.Popen(cmd_for_kinect_audio, shell=True)
    processes.append(p)
    p = subprocess.Popen(cmd_for_external_audio, shell=True)
    processes.append(p)
    for process in processes:
        process.wait()


    # reallocate the recorded files to the output path
    # create folder if does not exists
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path, exist_ok=True)
    # create folder for session if does not exasts
    day, month, year = args.date.split('.')
    session_full_name= 'Session_%i_date_%s_%s_%s'%(int(args.session_num), day, month, year)
    if not os.path.exists(os.path.join(args.output_path,session_full_name)):
        os.makedirs(os.path.join(args.output_path,session_full_name), exist_ok=True)

    # generate pseudoanonimized name
    pseudo_name=generate_pseudoanonimization_time_room(room_name=args.room_name)


    # reallocate files
    path_for_moving = os.path.join(args.output_path,session_full_name, pseudo_name)
    # create the folder if does not exists
    if not os.path.exists(path_for_moving):
        os.makedirs(path_for_moving)
    # Moving files from Kinect
    filenames=os.listdir(rec_config.KINECT_OUTPUT_PATH)
    for filename in filenames:
        shutil.move(os.path.join(rec_config.KINECT_OUTPUT_PATH, filename), os.path.join(path_for_moving, filename))

    # Moving files from Audio-Kinect
    filenames = os.listdir(rec_config.AUDIO_KINECT_OUTPUT_PATH)
    for filename in filenames:
        shutil.move(os.path.join(rec_config.AUDIO_KINECT_OUTPUT_PATH, filename), os.path.join(path_for_moving, filename))

    # Moving files from External audio device
    filenames = os.listdir(rec_config.AUDIO_MICROPHONE_OUTPUT_PATH)
    for filename in filenames:
        shutil.move(os.path.join(rec_config.AUDIO_MICROPHONE_OUTPUT_PATH, filename), os.path.join(path_for_moving, filename))

