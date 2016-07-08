import os
import io
from os import path

import speech_recognition as sr
from vexmessage import create_vex_message
from speechtotext.messaging import Messaging


class SpeechText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def get_msg(self, data, rate, sample_width, message):
        audio_data = sr.AudioData(data, rate, sample_width)

        msg = self.recognizer.recognize_google(audio_data,
                                               show_all =True)

        return msg
