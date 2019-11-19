import GoogleWebSpeechAPI as gws
import ttsGoogleTranslateAPI as ttsGT
import time
ReplasingFrom="ты"
Replasingto = "я"

AnswerDict = {"ты":"я","я":"ты","будешь":"буду","тебе":"мне","мне":"тебе","спасибо":"пожалуйста","скажу":"скажешь","меня":"тебя","умеешь":"умею"}


while True:
    input("enter any symbol to start speech recognition")
    textFromSpeech = gws.startSpeechRecognition()
    textFromSpeech=textFromSpeech.lower()
    print(textFromSpeech)
    if textFromSpeech == "спасибо":
        ttsGT.ttsPlay("пожалуйста")
        time.sleep(1)
        ttsGT.ttsPlay("кожаный ублюдок")
        break

    textFromSpeech = textFromSpeech.split()
    print(textFromSpeech)
    for i in range(len(textFromSpeech)):
        if textFromSpeech[i] in AnswerDict:
            textFromSpeech[i] = AnswerDict[textFromSpeech[i]]
    print(textFromSpeech)

    textFromSpeech =" ".join(textFromSpeech)
    ttsGT.ttsPlay(textFromSpeech)
