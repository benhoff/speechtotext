import wave
import os
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
        f.setsampwidth(sample_width)
        f.setframerate(rate)
        while True:
            data = self.audio_socket.recv_multipart()
            rate = int(data.pop(0))
            sample_width = int(data.pop(0))

            stream_data = b"".join(data)
            f.writeframes(stream_data)
            # TODO
            # NOTE: need to log the sample rate and format that are 
            # coming in for each stream.
            f.close()
            print('sample width', sample_width)
            audio_data = sr.AudioData(stream_data, rate, sample_width)

            msg = self.recognizer.recognize_ibm(audio_data,
                                                os.getenv('IBM_USERNAME'),
                                                os.getenv('IBM_PASSWORD'),
                                                show_all=True)

            print(msg)

            msg = self.recognizer.recognize_google(audio_data,
                                                   show_all =True)

            print(msg)
