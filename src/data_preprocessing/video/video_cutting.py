import os

import pandas as pd
import numpy as np
import cv2



def cut_video_on_sequences(video_path:str, sequence_length:int, output_path:str):
    """

    :param video_path:
    :param sequence_length:
    :param output_path:
    :return:
    """
    cap = cv2.VideoCapture(video_path)

    if (cap.isOpened() == False):
        raise Exception("Error opening video stream or file: " + video_path)

    # create the output path if it does not exist
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    path_to_extracted_videos = os.path.join(output_path, video_path.split(os.path.sep)[-1].split('.')[0])
    if not os.pat.exists(path_to_extracted_videos):
        os.makedirs(path_to_extracted_videos, exist_ok=True)
    path_to_metadata = os.path.join(output_path, 'metadata.csv')

    # prepare metadata file
    metadata = pd.DataFrame(columns=['video_filename', 'id', 'start_frame', 'end_frame', 'start_sec', 'end_sec'])


    # using scikit-video lib http://www.scikit-video.org/stable/io.html











def main():
    pass


if __name__== "__main__":
    main()