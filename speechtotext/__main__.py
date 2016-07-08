import argparse

from speechtotext.speechtext import SpeechText
from speechtotext.messaging import Messaging


def main(*args, **kwargs):
    """
    args:
        context
    kwargs:
        audio_address
        text_address
    """
    speech_text = SpeechText()
    messaging = Messaging(speech_text, *args, **kwargs)
    messaging.run()


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
