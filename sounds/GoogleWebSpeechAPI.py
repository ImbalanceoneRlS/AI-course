#from pocketsphinx import LiveSpeech
#for phrase in LiveSpeech(audio_device="4"): print(phrase)

import speech_recognition as sr
sample_rate = 48000
chunk_size = 2048
# obtain audio from the microphone
r = sr.Recognizer()

def startSpeechRecognition():
    with sr.Microphone(device_index = 2, sample_rate = sample_rate,
                       chunk_size = chunk_size) as source:


        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)

        # recognize speech using Sphinx
    try:
        return r.recognize_google(audio,language = "ru-RU")
    except sr.UnknownValueError:
        print("google could not understand audio")
        exit(0)
    except sr.RequestError as e:
        print("error; {0}".format(e))
        exit(0)


