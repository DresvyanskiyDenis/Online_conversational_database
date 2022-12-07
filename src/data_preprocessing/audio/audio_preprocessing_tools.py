import glob
from collections import defaultdict
from typing import Dict, Optional
from pyannote.audio import Pipeline
from pyannote.audio.pipelines import VoiceActivityDetection
import numpy as np
import pandas as pd
import torch
import os
import gc

from scipy.io import wavfile


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

    del speech_regions
    return speaker_to_segments

def initialize_voice_activity_detector(device:str='cuda', onset:float=0.5, offset:float=0.5, min_duration_on:float=0.0, min_duration_off:float=0.0):
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
    print('Speech regions saved to the file %s...'%(path+'.csv'))
    # clean RAM
    del file_to_save
    gc.collect()

def n_to_mono_channel_audio_in_one(path_to_audio:str, output_path:str)->None:
    # read audio file in wave format
    sample_rate, audio=wavfile.read(path_to_audio)
    # convert audio to the 1 channel
    audio=audio.astype(float)
    audio=audio.mean(axis=1)
    audio = audio.astype('int32')
    # save converted audio file
    wavfile.write(output_path, sample_rate, audio)


def apply_speech_regions_to_audio(audio_array:np.ndarray, speech_regions:pd.DataFrame, sample_rate:int=44100,
                                  speaker_ID:int=0) -> np.ndarray:
    # tak only speaker with specified Speaker_ID
    speech_regions = speech_regions[speech_regions['Speaker_ID']==speaker_ID]
    # go through speech_regions dataframe and silence all parts, which are not indicated
    # columns of the speech_regions: speaker_ID, segment_start, segment_end
    end_of_last_segment_idx=0
    for idx in range(0, speech_regions.shape[0]):
        # convert start of the segment from seconds to index of wave data
        start_segment_idx=int(speech_regions.iloc[idx].segment_start * sample_rate)
        # silent sounds from end of last segment to start of current segment
        audio_array[end_of_last_segment_idx:start_segment_idx]=0
        # save end of current segment for future calculations
        end_of_last_segment_idx = int(speech_regions.iloc[idx].segment_end * sample_rate)
    # silence the segment from end of the very last segment to end of the audio
    audio_array[end_of_last_segment_idx:]=0

    return audio_array

def apply_speech_regions_to_audio_in_subdirs(path_to_dir:str, path_to_dir_speech_regions:str,
                                             name_of_audio_file='audio_microphone.wav')->None:
    # find names of dirs with speech regions - these are names of participants' codes
    participants_ids=os.listdir(path_to_dir_speech_regions)
    for participants_id in participants_ids:
        # find directory with the audioname specified in name_of_audio_file and participants_id
        path_to_audio_for_processing=glob.glob(os.path.join(path_to_dir, "**", participants_id, name_of_audio_file))
        print("preprocessing the %s file..." % path_to_audio_for_processing)
        # check if only one path was found
        if len(path_to_audio_for_processing)==1:
            path_to_audio_for_processing=path_to_audio_for_processing[0]
        else:
            raise Exception('The number of found paths is more than one.')
        # read file with speech regions
        speech_regions=pd.read_csv(os.path.join(path_to_dir_speech_regions, participants_id, "speech_regions.csv"))
        # read audio to be processed
        sample_rate, audio = wavfile.read(path_to_audio_for_processing)
        audio= apply_speech_regions_to_audio(audio, speech_regions, sample_rate, speaker_ID=0)
        # save processed audio
        path_for_saving=path_to_audio_for_processing[:path_to_audio_for_processing.rfind("/")]
        path_for_saving=os.path.join(path_for_saving, name_of_audio_file.split(".")[0]+'_speaker_0.wav')
        wavfile.write(path_for_saving, sample_rate, audio)


def convert_wav_to_mono_channel_for_all_files_in_subdirs(path_to_dir:str, name_of_audio_file='audio_kinect.wav',
                                                         output_path:str=None)->None:
    # create output dir if it does not exist
    if not output_path is None:
        os.makedirs(output_path, exist_ok=True)

    for root, dirs, files in os.walk(os.path.abspath(path_to_dir)):
        for file in files:
            if file==name_of_audio_file:
                print("preprocessing the %s file..." % str(os.path.join(root, name_of_audio_file)))
                if not output_path is None:
                    final_output_path = os.path.join(output_path, root.split('/')[-1], name_of_audio_file.split('.')[0]+'_compressed.wav')
                    n_to_mono_channel_audio_in_one(path_to_audio=os.path.join(root, name_of_audio_file), output_path=final_output_path)
                else:
                    n_to_mono_channel_audio_in_one(path_to_audio=os.path.join(root, name_of_audio_file),
                                                   output_path=os.path.join(root, name_of_audio_file.split('.')[0]+'_compressed.wav'))
                # clear RAM
                gc.collect()



def generate_speech_regions_for_all_files_in_subdirs(path_to_dir:str, name_of_audio_file='audio_kinect.wav', output_path:str=None):

    if not output_path is None:
        os.makedirs(output_path, exist_ok=True)

    for root, dirs, files in os.walk(os.path.abspath(path_to_dir)):
        for file in files:
            if file==name_of_audio_file:
                vad = initialize_voice_activity_detector()
                print("preprocessing the %s file..."%str(os.path.join(root,name_of_audio_file)))
                speech_regions=get_speech_regions(path_to_audiofile=os.path.join(root,name_of_audio_file), voice_activity_detector=vad)
                if not output_path is None:
                    final_output_path=os.path.join(output_path, root.split('/')[-1],'speech_regions')
                    if not os.path.exists(os.path.join(output_path, root.split('/')[-1])):
                        os.makedirs(os.path.join(output_path, root.split('/')[-1]))
                    save_speech_regions(speech_regions, path=final_output_path)
                else:
                    save_speech_regions(speech_regions, path=os.path.join(root, 'speech_regions'))
                # clean RAM
                del vad
                torch.cuda.empty_cache()
                gc.collect()



if __name__ == '__main__':

    #vad = initialize_voice_activity_detector()

    #speech_regions = get_speech_regions(path_to_audiofile=r"tmp_audio_microphone.wav",
    #                                    voice_activity_detector=vad)

    #print(speech_regions)
    #save_speech_regions(speech_regions, 'tmp_dataframe')

    ########################################
    #convert_wav_to_mono_channel_for_all_files_in_subdirs('/media/external_hdd_1/DyCoVa/', output_path=None)
    ########################################

    apply_speech_regions_to_audio_in_subdirs(path_to_dir="/media/external_hdd_1/DyCoVa/", path_to_dir_speech_regions="/work/home/dsu/results/",
                                             name_of_audio_file='audio_kinect_compressed.wav')

