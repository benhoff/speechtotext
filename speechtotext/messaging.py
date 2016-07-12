# import uuid
import wave

import zmq

from vexmessage import create_vex_message, decode_vex_message


class Messaging:
    def __init__(self, stt, context=None, audio_address='', publish_address=''):
        # FIXME
        self.speechtotext = stt
        context = context or zmq.Context()
        self.audio_socket = context.socket(zmq.SUB)
        self.audio_socket.bind(audio_address)
        self.audio_socket.setsockopt_unicode(zmq.SUBSCRIBE, '')

        self.publish_socket = context.socket(zmq.PUB)
        self.publish_socket.connect(publish_address)

    def run(self):
        while True:
            frame = self.audio_socket.recv_multipart()
            message = decode_vex_message(frame)
            if message.type == 'AUDIO':
                sample_rate = message.contents['sample_rate']
                sample_width = message.contents['sample_width']
                number_channels = message.contents['number_channels']
                stream_data = message.contents['audio']

                msg = self.speechtotext.get_msg(stream_data,
                                                sample_rate,
                                                sample_width,
                                                number_channels)


                """
                filename = '{}.wav'.format(uuid.uuid4())

                with wave.open(filename, 'wb') as f:
                    f.setnchannels(number_channels)
                    f.setsampwidth(sample_width)
                    f.setframerate(sample_rate)
                    f.writeframes(stream_data)

                logging.error(msg)
                """

                if msg:
                    try:
                        message = msg.get('alternative')[0]['transcript']
                        alternative = msg.get('alternative')
                    except AttributeError:
                        message = msg
                        alternative = None
                    response = create_vex_message('',
                                                  'speechtotext',
                                                  'MSG',
                                                  message=message,
                                                  alternative=alternative)

                    self.publish_socket.send_multipart(response)
                else:
                    pass
