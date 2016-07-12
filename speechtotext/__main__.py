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
    google_api_key = kwargs.pop('google_api_key')
    speech_text = SpeechText(google_api_key)
    messaging = Messaging(speech_text, *args, **kwargs)
    messaging.run()


def _get_kwargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_address',
                        action='store',
                        default='tcp://127.0.0.1:5555')

    parser.add_argument('--publish_address',
                        action='store',
                        default='tcp://127.0.0.1:6003')

    parser.add_argument('--google_api_key',
                        action='store',
                        default=None)

    return vars(parser.parse_args())


if __name__ == '__main__':
    kwargs = _get_kwargs()
    main(**kwargs)
