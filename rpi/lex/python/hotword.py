from os import environ, path
import pyaudio
from pocketsphinx import *
from sphinxbase import *

MODELDIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/model/"
p = pyaudio.PyAudio()
# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/'))
config.set_string('-lm', '3268.lm')
config.set_string('-dict', '3268.dic')
config.set_float('-kws_threshold',  1e-15)
config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)
decoder.set_keyphrase("kws", "LIBBY")
decoder.set_search("kws")

def start(callback):
    # Decode streaming data.
    decoder.start_utt()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                    input=True,
                    frames_per_buffer=20480)

    stream.start_stream()
    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
        if decoder.hyp() is not None:
            print(decoder.hyp().hypstr)
            decoder.end_utt()
            callback()
            break
