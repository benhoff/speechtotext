import wave
import math

import zmq
import pyaudio

from vexmessage import create_vex_message, decode_vex_message


class Messaging:
    def __init__(self, stt, context=None, audio_address='', text_address=''):
        # FIXME
        self.speechtotext = stt
        context = context or zmq.Context()
        self.audio_socket = context.socket(zmq.SUB)
        self.audio_socket.bind(audio_address)
        self.audio_socket.setsockopt_unicode(zmq.SUBSCRIBE, '')

        self.text_socket = context.socket(zmq.PUB)
        self.text_socket.connect(text_address)
        self._pyaudio = pyaudio.PyAudio()

    def __del__(self):
        self._pyaudio.terminate()

    def run(self):
        while True:

            frame = self.audio_socket.recv_multipart()
            message = decode_vex_message(frame)
            if message.type == 'CMD' and message.get('command') == 'record':

                sample_rate = message.contents['sample_rate']
                sample_width = message.contents['sample_width']
                number_channels = message.contents['number_channels']
                data = message.contents['audio']

            stream_data = b"".join(data)
            msg = self.speechtotext.get_msg(stream_data, sample_rate, sample_width, message)
            if msg:
                response = create_vex_message('', 'speechtotext', 'MSG', message=msg)
                print(response)

                self.messaging.text_socket.send_multipart(response)
            else:
                pass
