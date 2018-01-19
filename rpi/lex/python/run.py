from lex import Lex
<<<<<<< HEAD
# import snowboy.snowboydecoder
# from snowboy import snowboydecoder
=======
from snowboy import snowboydecoder
from subprocess import run
>>>>>>> 3e2008d713fffc6ff8ca01bffb0d2277615f40e6

lex = Lex()
stop_recording = False
model = "Libby.pmdl"
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

<<<<<<< HEAD
# lex.record()
# print("Recording done")
response = lex.post_content()

lex.play_response(response)

# print("Finished!")

=======
>>>>>>> 3e2008d713fffc6ff8ca01bffb0d2277615f40e6

def record_and_post():
    run(['play', 'snowboy/resources/ding.wav'])
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

<<<<<<< HEAD
model = "snowboy/resources/snowboy.umdl"
# detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

# detector.start(detected_callback = record_and_post,
#        interrupt_check = interrupt_callback, sleep_time=0.03)
=======

def detect():
    detector.start(detected_callback=record_and_post,
                interrupt_check=interrupt_callback, sleep_time=0.03)
>>>>>>> 3e2008d713fffc6ff8ca01bffb0d2277615f40e6

detect()

<<<<<<< HEAD
# detector.terminate()
=======
>>>>>>> 3e2008d713fffc6ff8ca01bffb0d2277615f40e6
