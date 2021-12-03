from pyannote.audio import Pipeline
from pyannote.audio.pipelines import VoiceActivityDetection
from scipy.io import wavfile
samplerate, data = wavfile.read(r"C:\Users\Dresvyanskiy\Desktop\audio_kinect.wav")

data=data[int(samplerate*300): int(samplerate*360)]
wavfile.write(r"C:\Users\Dresvyanskiy\Desktop\tmp_audio_microphone.wav", samplerate, data)
del data

MODEL = "hbredin/VoiceActivityDetection-PyanNet-DIHARD"
vad = Pipeline.from_pretrained(MODEL, device="cpu")
speech_regions = vad(r"C:\\Users\\Dresvyanskiy\Desktop\\tmp_audio_microphone.wav")

"""pipeline = VoiceActivityDetection(segmentation="pyannote/segmentation")
HYPER_PARAMETERS = {
  # onset/offset activation thresholds
  "onset": 0.5, "offset": 0.5,
  # remove speech regions shorter than that many seconds.
  "min_duration_on": 0.0,
  # fill non-speech regions shorter than that many seconds.
  "min_duration_off": 0.0
}
pipeline.instantiate(HYPER_PARAMETERS)
vad = pipeline(r"C:\\Users\\Dresvyanskiy\Desktop\\tmp_audio_microphone.wav")
print(vad)"""
# `vad` is a pyannote.core.Annotation instance containing speech regions
# get timesteps
for start,end in speech_regions.get_timeline():
    print(start, end)