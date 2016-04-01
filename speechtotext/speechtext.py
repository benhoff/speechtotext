import os
import io
from os import path

import speech_recognition as sr
from speechtotext.messaging import Messaging


class SpeechText:
    def __init__(self,
                 *args,
                 **kwargs):
        """
        args:
            context
        kwargs:
            audio_address
            text_address
        """
        self.recognizer = sr.Recognizer()
        self.messaging = Messaging(self, *args, **kwargs)

    def run(self):
        self.messaging.run()

    def _get_msg(self, data, rate, sample_width):
        audio_data = sr.AudioData(data, rate, sample_width)

        msg = self.recognizer.recognize_google(audio_data,
                                               show_all =True)
        print(msg)
