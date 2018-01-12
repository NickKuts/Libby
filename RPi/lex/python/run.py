from lex import Lex
from snowboy import snowboydecoder

lex = Lex()
stop_recording = False
model = "Libby.pmdl"
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)


def record_and_post():
    response = lex.post_content()
    state = lex.play_response(response)

    print('State:', state)

    if state == 'Fulfilled':
        detector.terminate()
        detect()
    elif state != 'Failed':
        record_and_post()
    else:
        detector.terminate()
        stop_recording = True


def interrupt_callback():
    return stop_recording


def detect():
    detector.start(detected_callback=record_and_post,
                interrupt_check=interrupt_callback, sleep_time=0.03)

detect()

