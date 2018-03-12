from os import path
import pyaudio
from pocketsphinx.pocketsphinx import Decoder

MODELDIR = "model/"
PATHDIR = ""
p = pyaudio.PyAudio()
# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/'))
config.set_string('-dict', path.join(PATHDIR, '0963.dic'))
config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)

decoder.set_kws("kws", path.join(PATHDIR, 'keywords.txt'))
decoder.set_lm_file("lm", path.join(PATHDIR, '0963.lm'))
decoder.set_search("kws")


def start(callback):
    # Decode streaming data.
    decoder.start_utt()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                    input=True, input_device_index=None,
                    frames_per_buffer=20480)
    stream.start_stream()

    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
        if decoder.hyp() is not None:
            print("Found keyword")
            print(decoder.hyp().hypstr)
            break
    stream.stop_stream()
    stream.close()
    decoder.end_utt()
    callback()
