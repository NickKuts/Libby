import os

from lex import Lex
from subprocess import run
import hotword

basedir = os.path.dirname(os.path.abspath(__file__))

lex = Lex()
stop_recording = False


def record_and_post():
    run(['play', os.path.join(basedir, 'ding.wav')])
    response = lex.post_content()
    state = lex.play_response(response)

    print('State:', state)

    if state == 'Fulfilled':
        detect()
    elif state != 'Failed':
        record_and_post()
    else:
        stop_recording = True
        detect()


def interrupt_callback():
    return stop_recording


def detect():
    hotword.start(record_and_post)

detect()
