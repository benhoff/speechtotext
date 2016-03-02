import wave
from os import path

import zmq
import pyaudio
import speech_recognition as sr


class SpeechText:
    def __init__(self,
                 audio_address='tcp://*:5655',
                 text_address='tcp://*:6003',
                 context=None):

        context = context or zmq.Context()
        self.audio_socket = context.socket(zmq.SUB)
        self.audio_socket.bind(audio_address)
        self.audio_socket.setsockopt_unicode(zmq.SUBSCRIBE, '')

        self.text_socket = context.socket(zmq.PUB)
        self.text_socket.bind(text_address)
        self.recognizer = sr.Recognizer()

    def run(self):
        # FIXME
        pa = pyaudio.PyAudio()
        info = pa.get_default_input_device_info()
        rate = int(info['defaultSampleRate'])

        f = wave.open('audio.wav', mode='wb')
        f.setnchannels(2)
        sample_width = pa.get_sample_size(pyaudio.paInt16)
        print('sample width', sample_width)
        f.setsampwidth(sample_width)
        f.setframerate(rate)
        while True:
            data = []
            for _ in range(215):
                frame = self.audio_socket.recv()
                f.writeframes(frame)
                data.append(frame)
            # TODO
            stream_data = b"".join(data)
            # NOTE: need to log the sample rate and format that are 
            # coming in for each stream.
            f.close()
            audio_data = sr.AudioData(stream_data, rate, 2)

            msg = self.recognizer.recognize_sphinx(audio_data)
            print(msg)


