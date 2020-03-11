import os
import subprocess as sp
def ttsPlay(text):
    os.system("~/g_speak.sh "+text)

def ttsProcPlay(text):
    sp.Popen("~/g_speak.sh "+text,shell=True)
