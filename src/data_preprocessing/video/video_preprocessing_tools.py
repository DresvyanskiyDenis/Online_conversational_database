import subprocess
import os
import gc
from typing import Union, Tuple, Optional

from moviepy.editor import VideoFileClip, CompositeVideoClip


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

def get_sequence_of_video(video:Union[str, VideoFileClip], limits:Tuple[float, float],
                          resize:Optional[Tuple[int, int]]=None, with_audio:Optional[bool]=True,
                          save_video:Optional[bool]=False, output_path:Optional[str]=None)->VideoFileClip:
    """ Get a sequence of a video and save it in a new video file.

    :param video: Union[str, cv2.VideoCapture]
        Path to the video or a cv2.VideoCapture object.
    :param limits: Tuple[float, float]
        Tuple with the start and end time of the sequence. (in seconds)
    :param output_path: str
        Path to the output video.
    :param resize: Optional[Tuple[int, int]]
        Tuple with the new width and height of the video, if specified.
    :param with_audio: Optional[bool]
        If True, the audio of the original video is included in the output video.
    :param save_video: Optional[bool]
        If True, the output video is saved using the output_path.
    :return: VideoFileClip
    """
    clip = VideoFileClip(video).subclip(limits[0], limits[1])
    fps = clip.fps
    if resize is not None:
        clip = clip.resize(resize)
    if with_audio is False:
        clip.audio=None
    if save_video is True:
        clip.write_videofile(output_path, fps=fps, threads=4)
    else:
        return clip



def compose_three_videos(video1:Union[str, VideoFileClip], video2:Union[str, VideoFileClip], video3:Union[str, VideoFileClip],
                         final_resolution:Tuple[int, int],
                         save_video:Optional[bool]=False, output_path:Optional[str]=None) ->CompositeVideoClip:
    """ Compose three videos in a single video.

    :param video1: Union[str, cv2.VideoCapture]
        Path to the first video or a cv2.VideoCapture object.
    :param video2: Union[str, cv2.VideoCapture]
        Path to the second video or a cv2.VideoCapture object.
    :param video3: Union[str, cv2.VideoCapture]
        Path to the third video or a cv2.VideoCapture object.
    :param save_video: Optional[bool]
        If True, the output video is saved using the output_path.
    :param output_path: str
        Path to the output video.
    :param final_resolution: Tuple[int, int]
        Tuple with the new width and height of the video
    :return:
    """
    if isinstance(video1, str):
        clip1 = VideoFileClip(video1)
    else:
        clip1 = video1
    clip1_size = (clip1.w, clip1.h) # (width, height)
    clip1_fps = clip1.fps
    if isinstance(video2, str):
        clip2 = VideoFileClip(video2)
    else:
        clip2 = video2
    clip2_size = (clip2.w, clip2.h) # (width, height)
    clip2_fps = clip2.fps
    if isinstance(video3, str):
        clip3 = VideoFileClip(video3)
    else:
        clip3 = video3
    clip3_size = (clip3.w, clip3.h) # (width, height)
    clip3_fps = clip3.fps

    if clip1_fps != clip2_fps or clip1_fps != clip3_fps:
        raise ValueError("The fps of the videos are not equal.")

    if clip1_size != clip2_size or clip1_size != clip3_size:
        raise ValueError("The height and/or width of the videos are not equal.")

    # resizing the videos
    new_size = (final_resolution[0]//2-20, final_resolution[1]//2-20) # (width, height)
    clip1 = clip1.resize(new_size).margin(10, color=(0, 0, 0))
    clip2 = clip2.resize(new_size).margin(10, color=(0, 0, 0))
    clip3 = clip3.resize(new_size).margin(10, color=(0, 0, 0))

    # calculate positions
    pos1 = (0, 0)
    pos2 = (final_resolution[0]//2, 0)
    pos3 = (final_resolution[0]//4, final_resolution[1]//2)
    # make the composition
    final_clip = CompositeVideoClip([clip1.set_position(pos1),
                           clip2.set_position(pos2),
                           clip3.set_position(pos3)], size=final_resolution)

    if save_video is True:
        final_clip.write_videofile(output_path, fps=clip1_fps, threads=8)
    else:
        return final_clip



if __name__ == '__main__':
    extract_and_reencode_all_videos_with_name(path_to_dir='/media/external_hdd_1/DyCoVa/', name_of_videofile='result.mkv', output_path=None)