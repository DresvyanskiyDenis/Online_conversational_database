import subprocess
import os
import gc


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


if __name__ == '__main__':
    extract_and_reencode_all_videos_with_name(path_to_dir='/media/external_hdd_1/DyCoVa/', name_of_videofile='result.mkv', output_path=None)