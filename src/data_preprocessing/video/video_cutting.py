from src.data_preprocessing.video.video_preprocessing_tools import get_sequence_of_video, compose_three_videos

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

