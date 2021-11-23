from pyk4a import ColorResolution, ImageFormat, DepthMode, FPS


# KINECT PARAMS
KINECT_RESOLUTION = ColorResolution.RES_1080P
KINECT_IMAGE_FORMAT=ImageFormat.COLOR_MJPG
KINECT_DEPTH_MODE =DepthMode.NFOV_2X2BINNED
KINECT_FPS = FPS.FPS_30
KINECT_SYNCHRO = True
KINECT_DEVICE_ID = 0
KINECT_OUTPUT_PATH = 'Results'
KINECT_RECORDING_TIME = 2400 # in seconds

# AUDIO RECORDING KINECT PARAMS
AUDIO_KINECT_FORMAT = 'int32'
AUDIO_KINECT_RATE = 44100
AUDIO_KINECT_NUM_CHANNELS = 7
AUDIO_KINECT_CHUNK_SIZE = 512
AUDIO_KINECT_RECORDING_TIME = KINECT_RECORDING_TIME # in seconds
AUDIO_KINECT_OUTPUT_PATH = 'Results'
AUDIO_KINECT_OUTPUT_FILENAME = 'audio_kinect.wav'

# AUDIO RECORDING MICROPHONE PARAMS
AUDIO_MICROPHONE_FORMAT = 'int32'
AUDIO_MICROPHONE_RATE = 44100
AUDIO_MICROPHONE_NUM_CHANNELS = 1
AUDIO_MICROPHONE_CHUNK_SIZE = 512
AUDIO_MICROPHONE_RECORDING_TIME = KINECT_RECORDING_TIME # in seconds
AUDIO_MICROPHONE_OUTPUT_PATH = 'Results'
AUDIO_MICROPHONE_OUTPUT_FILENAME = 'audio_microphone.wav'


