import os
import io
from os import path

import speech_recognition as sr


class SpeechText:
    def __init__(self, google_api_key):
        self.recognizer = sr.Recognizer()
        self._api_key = google_api_key
        self._number_channels = None

    def get_msg(self, data, rate, sample_width, number_channels):
        audio_data = sr.AudioData(data, rate, sample_width)

        msg = self.recognizer.recognize_google(audio_data,
                                               key=self._api_key,
                                               show_all=True)
        if not msg:
            msg = self.recognizer.recognize_sphinx(audio_data)

        return msg
