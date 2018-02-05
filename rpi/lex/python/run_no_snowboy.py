from lex import Lex
from subprocess import run

lex = Lex()
stop_recording = False
model = "Libby.pmdl"


def record_and_post():
    #run(['play', 'snowboy/resources/ding.wav'])
    response = lex.post_content()
    state = lex.play_response(response)

    print('State:', state)

def interrupt_callback():
    return stop_recording


record_and_post()
