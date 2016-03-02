import sys
import argparse
import subprocess
import microphone
import atexit

from os import path
from threading import Thread

from speechtext import SpeechText



def main(audio_address='tcp://*:5555',
         text_address='tcp://*:6003'):

    speech_text = SpeechText(audio_address, text_address)

    thread = Thread(target=microphone.main)
    thread.daemon = True
    thread.start()

    """
    microphone_dir = path.dirname(microphone.__file__)
    main_microphone_file = path.join(microphone_dir, '__main__.py')

    microphone_process = subprocess.Popen(sys.executable,
                                          main_microphone_file)
    """

    speech_text.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_address',
                        action='store',
                        default='tcp://*:5655')

    parser.add_argument('--text_address',
                        action='store',
                        default='tcp://*:6003')

    args = parser.parse_args()
    main(args.audio_address, args.text_address)
