import sys
import argparse
import subprocess
import microphone
import atexit

from os import path
from threading import Thread

from speechtext import SpeechText



def main(*args, **kwargs):
    """
    args:
        context
    kwargs:
        audio_address
        text_address
    """
    speech_text = SpeechText(*args, **kwargs)
    """
    thread = Thread(target=microphone.main)
    thread.daemon = True
    thread.start()
    """
    microphone_dir = path.dirname(microphone.__file__)
    main_microphone_file = path.join(microphone_dir, '__main__.py')

    microphone_process = subprocess.Popen((sys.executable,
                                           main_microphone_file))

    speech_text.run()


def _get_kwargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_address',
                        action='store',
                        default='tcp://127.0.0.1:5555')

    parser.add_argument('--text_address',
                        action='store',
                        default='tcp://127.0.0.1:6003')

    return vars(parser.parse_args())


if __name__ == '__main__':
    kwargs = _get_kwargs()
    main(**kwargs)
