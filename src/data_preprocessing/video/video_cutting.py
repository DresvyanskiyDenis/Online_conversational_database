from typing import Union, Tuple, Optional

import cv2
import numpy as np
import pandas as pd
from moviepy.editor import VideoFileClip

from src.data_preprocessing.video.video_preprocessing_tools import get_sequence_of_video, compose_three_videos

if __name__ == '__main__':
    video_path = r"C:\Users\Dresvyanskiy\Desktop\Dark Ambient from Night City.mp4"
    generated_video_path = r"C:\Users\Dresvyanskiy\Desktop\Dark Ambient from Night City_cut.mp4"
    output_path = r"C:\Users\Dresvyanskiy\Desktop\composed_1.mp4"
    get_sequence_of_video(video_path, (0, 10), generated_video_path, (1920, 1080))

    compose_three_videos(generated_video_path, generated_video_path, generated_video_path, output_path, final_resolution=(1920, 1080))

