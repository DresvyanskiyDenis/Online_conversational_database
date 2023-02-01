import sys
sys.path.extend(["C:\\Users\\Dresvyanskiy\\Desktop\\Projects\\Online_conversational_database"])

from src.data_preprocessing.video.session_5 import session_5_preparation
from src.data_preprocessing.video.video_cutting import cut_videos_and_combine_them


def main():

    # session 1
    video_1 = r"E:\rendered_video\session_1\23112110310A\23112110310A_video.mp4"
    video_2 = r"E:\rendered_video\session_1\23112110320\23112110320_video.mp4"
    video_3 = r"E:\rendered_video\session_1\23112110321\23112110321_video.mp4"
    output_path = r"E:\rendered_video\session_1\composed_videos"
    cut_videos_and_combine_them(paths=[video_1, video_2, video_3], output_path=output_path)

    # session 2
    video_1 = r"E:\rendered_video\session_2\23112114310A\23112114310A_video.mp4"
    video_2 = r"E:\rendered_video\session_2\23112114320\23112114320_video.mp4"
    video_3 = r"E:\rendered_video\session_2\23112114321\23112114321_video.mp4"
    output_path = r"E:\rendered_video\session_2\composed_videos"
    cut_videos_and_combine_them(paths=[video_1, video_2, video_3], output_path=output_path)

    # session 3
    video_1 = r"E:\rendered_video\session_3\23112115310А\23112115310А_video.mp4"
    video_2 = r"E:\rendered_video\session_3\23112115320\23112115320_video.mp4"
    video_3 = r"E:\rendered_video\session_3\23112115321\23112115321_video.mp4"
    output_path = r"E:\rendered_video\session_3\composed_videos"
    cut_videos_and_combine_them(paths=[video_1, video_2, video_3], output_path=output_path)

    # session 4
    video_1 = r"E:\rendered_video\session_4\24112110310A\24112110310A_video.mp4"
    video_2 = r"E:\rendered_video\session_4\24112110320\24112110320_video.mp4"
    video_3 = r"E:\rendered_video\session_4\24112110321\24112110321_video.mp4"
    output_path = r"E:\rendered_video\session_4\composed_videos"
    cut_videos_and_combine_them(paths=[video_1, video_2, video_3], output_path=output_path)

    # session 6
    video_1 = r"E:\rendered_video\session_6\24112115310A\24112115310A_video.mp4"
    video_2 = r"E:\rendered_video\session_6\24112115320\24112115320_video.mp4"
    video_3 = r"E:\rendered_video\session_6\24112115321\24112115321_video.mp4"
    output_path = r"E:\rendered_video\session_6\composed_videos"
    cut_videos_and_combine_them(paths=[video_1, video_2, video_3], output_path=output_path)

    # special case: session 5
    session_5_preparation()


if __name__ == '__main__':
    main()