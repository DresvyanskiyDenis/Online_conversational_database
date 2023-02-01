import os
from typing import Union

import numpy as np
import pandas as pd
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ColorClip

from src.data_preprocessing.video.video_cutting import cut_one_video_on_sequences
from src.data_preprocessing.video.video_preprocessing_tools import compose_three_videos


def color_clip_with_audio(audio:Union[str, AudioFileClip],size, duration, fps=30, color=(0,0,0), output='color.mp4'):
    if isinstance(audio, str):
        audio = AudioFileClip(audio)
    clip=ColorClip(size, color, duration=duration)
    clip.audio = audio
    clip.write_videofile(output, fps=fps)

def cut_audio_on_sequences_with_black_video(audio_path:str, sequence_length:float, output_path:str)->None:
    """
    Cuts audio on sequences and generates from every audio sequence black video with the corresponding audio.
    :param audio_path: str
        Path to the audio.
    :param sequence_length: float
        Length of the sequences in seconds.
    :param output_path: str
        Path to the output folder.
    :return: None
    """
    # create output dir if needed
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    # calculate the number of sequences out from one video using sequence_length
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    audio_name = audio_path.split(os.path.sep)[-1].split('.')[0].split("_")[0]+"_video"
    number_of_sequences = int(np.ceil(audio_duration/sequence_length))
    # extract sequences one by one
    metadata = pd.DataFrame(columns=['video_name', 'sequence_ID', 'start_time', 'end_time'])
    for seq_idx in range(number_of_sequences):
        start_time = seq_idx*sequence_length
        end_time = start_time+sequence_length
        if end_time>audio_duration:
            end_time = audio_duration
            start_time = end_time-sequence_length
        color_clip_with_audio(audio.subclip(start_time, end_time), size=(1920, 1080), duration=sequence_length, output=os.path.join(output_path, "%s_seq_%i.mp4"%(audio_name, seq_idx)))
        metadata = metadata.append({'audio_name': audio_name,
                                    'sequence_ID': seq_idx,
                                    'start_time': start_time,
                                    'end_time': end_time
                                    }, ignore_index=True)
    # write metadata to the output path
    metadata.to_csv(os.path.join(output_path, "metadata.csv"), index=False)

def session_5_preparation():
    # this is a special case, therefore we have one separate function for it
    # In general, the speciality of the session is that one participant has no video. Therefore, we should form the video from only other two participants
    # session 5
    video_1 = r"E:\rendered_video\session_5\24112114310A\24112114310A_video.mp4"
    audio_2 = r"E:\rendered_video\session_5\24112114320\24112114320_audio_microphone.wav"
    video_3 = r"E:\rendered_video\session_5\24112114321\24112114321_video.mp4"
    output_path = r"E:\rendered_video\session_5\composed_videos"

    # create output dir if needed
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    # cut videos on sequences
    paths = [video_1, video_3]
    sequences = [1.,
                 15.,
                 60.]
    filenames = [path.split(os.path.sep)[-1].split('.')[0] for path in paths]

    # normal videos
    for path in paths:
        for sequence_length in sequences:
            filename = path.split(os.path.sep)[-1].split('.')[0]
            final_output_path = os.path.join(output_path, "%s_sequence_length_%f" % (filename, sequence_length))
            cut_one_video_on_sequences(path, sequence_length, output_path=final_output_path,
                                       resize=None)

    # the participant with no video - we just put the black screen instead
    # therefore, we don't need to cut the video on 1.0-second sequences
    sequences = [15., 60.]
    for sequence_length in sequences:
        filename = audio_2.split(os.path.sep)[-1].split('.')[0].split("_")[0] + "_video"
        final_output_path = os.path.join(output_path, "%s_sequence_length_%f" % (filename, sequence_length))
        cut_audio_on_sequences_with_black_video(audio_2, sequence_length, output_path=final_output_path)

    # combine 15- and 60-seconds sequences into one video
    combined_15_output_path = os.path.join(output_path, "combined_15_sec")
    combined_60_output_path = os.path.join(output_path, "combined_60_sec")
    # create output dirs if needed
    if not os.path.exists(combined_15_output_path):
        os.makedirs(combined_15_output_path, exist_ok=True)
    if not os.path.exists(combined_60_output_path):
        os.makedirs(combined_60_output_path, exist_ok=True)
    # open metadata files
    metadata_15_seconds_file_0 = pd.read_csv(
        os.path.join(output_path, "%s_sequence_length_%f" % (filenames[0], 15), "metadata.csv"))
    metadata_15_seconds_file_1 = pd.read_csv(
        os.path.join(output_path, "%s_sequence_length_%f" % (filenames[1], 15), "metadata.csv"))
    metadata_60_seconds_file_0 = pd.read_csv(
        os.path.join(output_path, "%s_sequence_length_%f" % (filenames[0], 60), "metadata.csv"))
    metadata_60_seconds_file_1 = pd.read_csv(
        os.path.join(output_path, "%s_sequence_length_%f" % (filenames[1], 60), "metadata.csv"))
    # append one more filename to filenames, since we have generated black screen for the participant with no video
    filenames.insert(1, audio_2.split(os.path.sep)[-1].split('.')[0].split("_")[0]+"_video")
    # combine 15-seconds sequences
    combined_files_metadata = pd.DataFrame(columns=['video_name', 'sequence_ID', 'start_time', 'end_time'])
    for idx in range(len(metadata_15_seconds_file_0)):
        compose_three_videos(video1=os.path.join(output_path, "%s_sequence_length_%f" % (filenames[0], 15),
                                                 "%s_seq_%i.mp4" % (filenames[0], idx)),
                             video2=os.path.join(output_path, "%s_sequence_length_%f" % (filenames[1], 15),
                                                 "%s_seq_%i.mp4" % (filenames[1], idx)),
                             video3=os.path.join(output_path, "%s_sequence_length_%f" % (filenames[2], 15),
                                                 "%s_seq_%i.mp4" % (filenames[2], idx)),
                             final_resolution=(1920, 1080),
                             save_video=True,
                             output_path=os.path.join(combined_15_output_path, "combined_seq_%i.mp4" % idx))
        combined_files_metadata = combined_files_metadata.append({'video_name': "combined_seq_%i.mp4" % idx,
                                                                  'sequence_ID': idx,
                                                                  'start_time': metadata_15_seconds_file_0.iloc[idx][
                                                                      'start_time'],
                                                                  'end_time': metadata_15_seconds_file_0.iloc[idx][
                                                                      'end_time']
                                                                  }, ignore_index=True)
    # write metadata to the output path
    combined_files_metadata.to_csv(os.path.join(combined_15_output_path, "metadata.csv"), index=False)
    # combine 60-seconds sequences
    combined_files_metadata = pd.DataFrame(columns=['video_name', 'sequence_ID', 'start_time', 'end_time'])
    for idx in range(len(metadata_60_seconds_file_0)):
        compose_three_videos(video1=os.path.join(output_path, "%s_sequence_length_%f" % (filenames[0], 60),
                                                 "%s_seq_%i.mp4" % (filenames[0], idx)),
                             video2=os.path.join(output_path, "%s_sequence_length_%f" % (filenames[1], 60),
                                                 "%s_seq_%i.mp4" % (filenames[1], idx)),
                             video3=os.path.join(output_path, "%s_sequence_length_%f" % (filenames[2], 60),
                                                 "%s_seq_%i.mp4" % (filenames[2], idx)),
                             final_resolution=(1920, 1080),
                             save_video=True,
                             output_path=os.path.join(combined_60_output_path, "combined_seq_%i.mp4" % idx))
        combined_files_metadata = combined_files_metadata.append({'video_name': "combined_seq_%i.mp4" % idx,
                                                                  'sequence_ID': idx,
                                                                  'start_time': metadata_60_seconds_file_0.iloc[idx][
                                                                      'start_time'],
                                                                  'end_time': metadata_60_seconds_file_0.iloc[idx][
                                                                      'end_time']
                                                                  }, ignore_index=True)
    # write metadata to the output path
    combined_files_metadata.to_csv(os.path.join(combined_60_output_path, "metadata.csv"), index=False)

