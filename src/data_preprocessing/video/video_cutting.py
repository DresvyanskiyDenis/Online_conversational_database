import os
from typing import Optional, Tuple

import numpy as np
import pandas as pd

from src.data_preprocessing.video.video_preprocessing_tools import get_sequence_of_video, compose_three_videos
from moviepy.editor import VideoFileClip


def cut_one_video_on_sequences(path_to_video:str, sequence_length:float, output_path:str, resize:Optional[Tuple[int, int]]=None)->None:
    """ Cuts one video on sequences of a given length.

    :param path_to_video: str
        Path to the video.
    :param sequence_length: float
        Length of the sequences in seconds.
    :param output_path: str
        Path to the output folder.
    :param resize: Optional[Tuple[int, int]]
        Tuple with the new width and height of the video, if specified.
    :return: None
    """
    # create output dir if needed
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    # calculate the number of sequences out from one video using sequence_length
    video = VideoFileClip(path_to_video)
    video_duration = video.duration
    video_name = path_to_video.split(os.path.sep)[-1].split('.')[0]
    number_of_sequences = int(np.ceil(video_duration/sequence_length))
    # extract sequences one by one
    metadata = pd.DataFrame(columns=['video_name', 'sequence_ID', 'start_time', 'end_time'])
    for seq_idx in range(number_of_sequences):
        start_time = seq_idx*sequence_length
        end_time = start_time+sequence_length
        if end_time>video_duration:
            end_time = video_duration
            start_time = end_time-sequence_length
        get_sequence_of_video(video, limits = (start_time, end_time),
                                    resize=resize, save_video=True,
                                    output_path=os.path.join(output_path, "%s_seq_%i.mp4"%(video_name, seq_idx)))
        metadata = metadata.append({'video_name': video_name,
                                    'sequence_ID': seq_idx,
                                    'start_time': start_time,
                                    'end_time': end_time
                                    }, ignore_index=True)
    # write metadata to the output path
    metadata.to_csv(os.path.join(output_path, "metadata.csv"), index=False)





if __name__ == '__main__':
    #video_path = r"C:\Users\Dresvyanskiy\Desktop\Dark Ambient from Night City.mp4"
    #generated_video_path = r"C:\Users\Dresvyanskiy\Desktop\Dark Ambient from Night City_cut.mp4"
    #output_path = r"C:\Users\Dresvyanskiy\Desktop\composed_1.mp4"
    #get_sequence_of_video(video_path, (0, 10), generated_video_path, (1920, 1080))

    #compose_three_videos(generated_video_path, generated_video_path, generated_video_path, output_path, final_resolution=(1920, 1080))
    # 8:20 - 27:00
    video_1 = r"E:\rendered_video\session_1\23112110310A\video.mp4"
    video_2 = r"E:\rendered_video\session_1\23112110320\video.mp4"
    video_3 = r"E:\rendered_video\session_1\23112110321\video.mp4"
    output_path = r"E:\rendered_video\session_1\video_composed.mp4"

    video_1 = get_sequence_of_video(video_1, limits=[8*60+20,27*60], resize=None, with_audio=True,
                          save_video=False, output_path=None)
    video_2 = get_sequence_of_video(video_2, limits=[8*60+20,27*60], resize=None, with_audio=True,
                            save_video=False, output_path=None)
    video_3 = get_sequence_of_video(video_3, limits=[8*60+20,27*60], resize=None, with_audio=True,
                            save_video=False, output_path=None)

    compose_three_videos(video1=video_1, video2=video_2, video3=video_3, final_resolution=(1920, 1080),
    save_video = True, output_path = output_path)

