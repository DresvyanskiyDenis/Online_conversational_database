from collections import defaultdict
from typing import Dict

from pyannote.audio import Pipeline
from pyannote.audio.pipelines import VoiceActivityDetection
from scipy.io import wavfile
import numpy as np
import pandas as pd
import os

def get_speech_regions(path_to_audiofile:str, voice_activity_detector:Pipeline)->Dict[int,np.ndarray]:
    # get pyannote.core.Annotation with speech regions of different speakers
    speech_regions=voice_activity_detector(path_to_audiofile)
    # we will represent speech regions in accordance to the speakers, using the dict[speaker_id->speech_regions]
    speaker_to_segments=defaultdict(lambda:np.zeros((0,2)))
    # translate the pyannote.core.Annotation data to the dict format
    for segment in speech_regions._timeline.segments_list_:
        labels=speech_regions.get_labels(segment)
        for label in labels:
            speaker_to_segments[label]=np.append(speaker_to_segments[label],np.array([[segment.start, segment.end]]), axis=0)

    return speaker_to_segments

def initialize_voice_activity_detector(device:str='cpu', onset:float=0.5, offset:float=0.5, min_duration_on:float=0.0, min_duration_off:float=0.0):
    # initialize the VAD using predifened model and device (CPU/GPU), on which it should work
    vad = VoiceActivityDetection(segmentation="pyannote/segmentation", device=device)
    HYPER_PARAMETERS = {
        # onset/offset activation thresholds
        "onset": onset, "offset":offset,
        # remove speech regions shorter than that many seconds.
        "min_duration_on": min_duration_on,
        # fill non-speech regions shorter than that many seconds.
        "min_duration_off": min_duration_off
    }
    vad.instantiate(HYPER_PARAMETERS)
    return vad

def save_speech_regions(speech_regions:Dict[int, np.ndarray], path:str) -> None:
    # columns for the final DataFrame, which will be saved
    columns_of_df=['Speaker_ID', 'segment_start', 'segment_end']
    # DataFrame, which will be saved
    file_to_save=pd.DataFrame(columns=columns_of_df)
    # go through all speakers
    for speaker_id in speech_regions.keys():
        # identify the number of segments of the concrete speaker and concatenate to the segments the speaker ID
        num_segments=speech_regions[speaker_id].shape[0]
        speaker_regions=np.concatenate((
                                        np.ones((num_segments,1), dtype='int32')*speaker_id,
                                        speech_regions[speaker_id]
                                        ),
                                       axis=1)
        # concatenate obtained DataFrame with the final DataFrame
        speaker_regions=pd.DataFrame(columns=columns_of_df, data=speaker_regions)
        file_to_save=file_to_save.append(speaker_regions, ignore_index=True)
    # save file
    file_to_save.to_csv(path+'.csv', index=False)

def generate_speech_regions_for_all_files_in_subdirs(path_to_dir:str, name_of_audio_file='audio_kinect.wav', output_path:str=None):

    vad=initialize_voice_activity_detector()

    for root, dirs, files in os.walk(os.path.abspath(path_to_dir)):
        for file in files:
            if file=='name_of_audio_file':
                speech_regions=get_speech_regions(path_to_audiofile=os.path.join(root,name_of_audio_file), voice_activity_detector=vad)
                if not output_path is None:
                    final_output_path=os.path.join(output_path, root.split('\\|/')[-1],'speech_regions')
                    save_speech_regions(speech_regions, path=final_output_path)
                else:
                    save_speech_regions(speech_regions, path=os.path.join(root, 'speech_regions'))


if __name__ == '__main__':

    #vad = initialize_voice_activity_detector()

    #speech_regions = get_speech_regions(path_to_audiofile=r"tmp_audio_microphone.wav",
    #                                    voice_activity_detector=vad)

    #print(speech_regions)
    #save_speech_regions(speech_regions, 'tmp_dataframe')

    generate_speech_regions_for_all_files_in_subdirs('D:\DyCoVa')


