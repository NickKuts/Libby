import os
import RPi.GPIO as GPIO
from lex import Lex
from subprocess import run
import hotword

basedir = os.path.dirname(os.path.abspath(__file__))
pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)

lex = Lex()
stop_recording = False

def record_and_post():
    GPIO.output(18, GPIO.HIGH)
    response = lex.post_content()
    GPIO.output(18, GPIO.LOW)
    state = lex.play_response(response)

    print('State:', state)

    if state == 'Fulfilled':
        detect()
    elif state != 'Failed':
        record_and_post()
    else:
        stop_recording = True
        detect()


def detect():
    hotword.start(record_and_post)

detect()
