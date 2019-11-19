from os import environ, path

from pocketsphinx import *
from sphinxbase import *

MODELDIR="/home/pi/zero_ru_cont_8k_v3/"

config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'zero_ru.cd_cont_4000'))
config.set_string('-lm', path.join(MODELDIR, 'ru.lm'))
config.set_string('-dict', path.join(MODELDIR, 'ruactiv.dic'))
config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)

import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=1024)
stream.start_stream()

in_speech_bf = False
decoder.start_utt()
while True:
    buf = stream.read(2048)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                print ('Result:', decoder.hyp().hypstr)
                decoder.start_utt()
    else:
        break
decoder.end_utt()