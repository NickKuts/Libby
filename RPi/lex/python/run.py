from lex import Lex
# import snowboy.snowboydecoder
# from snowboy import snowboydecoder

lex = Lex()

# lex.record()
# print("Recording done")
response = lex.post_content()

lex.play_response(response)

# print("Finished!")


def record_and_post():
    lex.record()
    response = lex.post_content()
    lex.play_response(response)


def interrupt_callback():
    return False

model = "snowboy/resources/snowboy.umdl"
# detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

# detector.start(detected_callback = record_and_post,
#        interrupt_check = interrupt_callback, sleep_time=0.03)


# detector.terminate()
