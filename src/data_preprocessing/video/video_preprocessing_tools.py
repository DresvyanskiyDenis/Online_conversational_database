import subprocess
import os
import gc
from typing import Union, Tuple, Optional

from moviepy.editor import VideoFileClip, clips_array, concatenate_videoclips, CompositeVideoClip


def extract_and_reencode_video_from_mkv(path_to_file:str, output_path:str)->None:
    # create output directory if needed
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    filename=path_to_file.split('/')[-1].split('.')[0]
    # extract video from mkv format in .h264 format
    shell_command='mkvextract tracks %s 0:%s'%(path_to_file, os.path.join(output_path, 'tmp.h264'))
    subprocess.run(shell_command, shell=True)
    # convert .h264 format to mp4 with compressing codec
    shell_command='x264 %s -o %s'%(os.path.join(output_path, 'tmp.h264'), os.path.join(output_path, filename+'.mp4'))
    subprocess.run(shell_command, shell=True)

    # delete tmp file
    os.remove(os.path.join(output_path, 'tmp.h264'))
    gc.collect()


def extract_and_reencode_all_videos_with_name(path_to_dir:str, name_of_videofile:str, output_path:str=None)->None:
    # create output directory if needed
    if not output_path is None:
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)

    for root, dirs, files in os.walk(os.path.abspath(path_to_dir)):
        for file in files:
            if file==name_of_videofile:
                print("preprocessing the %s file..." % str(os.path.join(root, file)))
                if not output_path is None:
                    extract_and_reencode_video_from_mkv(path_to_file=os.path.join(root, file), output_path=os.path.join(output_path, root.split('/')[-1]))
                else:
                    extract_and_reencode_video_from_mkv(path_to_file=os.path.join(root, file), output_path=root)

def get_sequence_of_video(video:Union[str, VideoFileClip], limits:Tuple[float, float], output_path:str,
                          resize:Optional[Tuple[int, int]]=None, with_audio:Optional[bool]=True)->None:
    """ Get a sequence of a video and save it in a new video file.

    :param video: Union[str, cv2.VideoCapture]
        Path to the video or a cv2.VideoCapture object.
    :param limits: Tuple[float, float]
        Tuple with the start and end time of the sequence.
    :param output_path: str
        Path to the output video.
    :param resize: Optional[Tuple[int, int]]
        Tuple with the new width and height of the video, if specified.
    :param with_audio: Optional[bool]
        If True, the audio of the original video is included in the output video.
    :return:
    """
    clip = VideoFileClip(video).subclip(limits[0], limits[1])
    fps = clip.fps
    if resize is not None:
        clip = clip.resize(resize)
    if with_audio is False:
        clip.audio=None
    clip.write_videofile(output_path, fps=fps)



def compose_three_videos(video1:Union[str, VideoFileClip], video2:Union[str, VideoFileClip], video3:Union[str, VideoFileClip],
                         output_path:str) ->None:
    """ Compose three videos in a single video.

    :param video1: Union[str, cv2.VideoCapture]
        Path to the first video or a cv2.VideoCapture object.
    :param video2: Union[str, cv2.VideoCapture]
        Path to the second video or a cv2.VideoCapture object.
    :param video3: Union[str, cv2.VideoCapture]
        Path to the third video or a cv2.VideoCapture object.
    :param output_path: str
        Path to the output video.
    :return:
    """
    clip1 = VideoFileClip(video1).resize((940, 520)).margin(10, color=(0, 0, 0))
    clip2 = VideoFileClip(video2).resize((940, 520)).margin(10, color=(0, 0, 0))
    clip3 = VideoFileClip(video3).resize((940, 520)).margin(10, color=(0, 0, 0))
    fps = clip1.fps
    final_clip = CompositeVideoClip([clip1.set_position((0,0)),
                           clip2.set_position((960,0)),
                           clip3.set_position((480,540))], size=(1920, 1080))

    final_clip.write_videofile(output_path, fps=fps)




if __name__ == '__main__':
    extract_and_reencode_all_videos_with_name(path_to_dir='/media/external_hdd_1/DyCoVa/', name_of_videofile='result.mkv', output_path=None)