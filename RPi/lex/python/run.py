from lex import Lex
#from snowboy import snowboydecoder

lex = Lex()

lex.record()
print("Recording done")
response = lex.post_content()

lex.play_response(response)

print("Finished!")

#detector = snowboydecoder.HotwordDetector(model, sensitivy=0.5)

#detector.start(detected_callback = snowboydecoder.play_audio_file, 
#        interrupt_check = interrupt_callback, sleep_time=0.03)


#detector.terminate()
