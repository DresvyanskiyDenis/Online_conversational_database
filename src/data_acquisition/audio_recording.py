import os
import pyaudio
import wave


def audio_stream_initialization(audio_format=pyaudio.paInt16, rate:int=44100,
                                num_channels:int=1, buffer_chunk_size:int=512,
                                device_index:int=0)-> pyaudio.PyAudio:
    stream = audio.open(format=audio_format, channels=num_channels,
                        rate=rate, input=True, input_device_index=device_index,
                        frames_per_buffer=buffer_chunk_size)
    return stream


def print_indexes_of_devices(audio:pyaudio.PyAudio)-> None:
    print("----------------------record device list---------------------")
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
    print("-------------------------------------------------------------")




if __name__ == '__main__':
    import argparse
    # parsing
    parser = argparse.ArgumentParser(description='Audio data recording using any microphone could be accessed.')
    parser.add_argument('--format', action='store', type=str, default='int32')
    parser.add_argument('--rate', action='store', type=int, default=44100)
    parser.add_argument('--num_channels', action='store', type=int, default=1)
    parser.add_argument('--device_index', action='store', type=int, default=0)
    parser.add_argument('--chunk_size', action='store', type=int, default=512)
    parser.add_argument('--time', action='store', type=int, default=60) # in seconds
    parser.add_argument('--output_path', action='store', type=str, default='results')
    parser.add_argument('--output_filename', action='store', type=str, default='audio_result.wav')
    args = parser.parse_args()


    # transfer formats of audio recordings to readable format for pyaudio
    audio_formats={'int8':pyaudio.paInt8, 'int16':pyaudio.paInt16,'int24':pyaudio.paInt24,'int32':pyaudio.paInt32}
    if args.format not in audio_formats.keys():
        raise Exception('Invalid argument value for audio recording format.')
    # initialization of audio recording stream
    audio = pyaudio.PyAudio()
    print_indexes_of_devices(audio)
    stream = audio_stream_initialization(audio_format=audio_formats[args.format], rate=args.rate,
                                num_channels=args.num_channels, buffer_chunk_size=args.chunk_size,
                                device_index=args.device_index)

    # start of the recording
    Recordframes = []
    for i in range(0, int(args.rate / args.chunk_size * args.time)):
        data = stream.read(args.chunk_size)
        Recordframes.append(data)
    print("audio recording is stopped")

    # finalizing the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # create output directory if does not exist
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path, exist_ok=True)

    # save recorded audio in the waveform
    waveFile = wave.open(os.path.join(args.output_path, args.output_filename), 'wb')
    waveFile.setnchannels(args.num_channels)
    waveFile.setsampwidth(audio.get_sample_size(audio_formats[args.format]))
    waveFile.setframerate(args.rate)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()
