import wave

import zmq
import pyaudio


class Messaging:
    def __init__(self, stt, context=None, audio_address='', text_address=''):
        # FIXME
        self.speechtotext = stt
        context = context or zmq.Context()
        self.audio_socket = context.socket(zmq.SUB)
        self.audio_socket.bind(audio_address)
        self.audio_socket.setsockopt_unicode(zmq.SUBSCRIBE, '')

        self.text_socket = context.socket(zmq.PUB)
        self.text_socket.bind(text_address)

    def run(self):
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
            rate = int(data.pop(0).decode('ascii'))
            sample_width = int.from_bytes(data.pop(0), 'big')

            stream_data = b"".join(data)
            f.writeframes(stream_data)
            # TODO
            # NOTE: need to log the sample rate and format that are 
            # coming in for each stream.
            f.close()
            self.speechtotext._get_msg(stream_data, rate, sample_width)
