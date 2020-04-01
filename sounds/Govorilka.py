from ArdSerial import ArdSender as As
import time,sys
import subprocess as sp
ArdSer = As.ArduinoSender()


text = " ".join(sys.argv[1:])


def ttsProcPlay(text):
    PlayProc=sp.Popen("~/g_speak.sh "+text,shell=True)
    return PlayProc

def Skazat(text):
    PlayProc = ttsProcPlay(text)
    while PlayProc.poll()==None:
        print(PlayProc.poll())
        for i in range(20):
            ArdSer.SendStringCommand("f")
            time.sleep(0.03)
        for i in range(20):
            ArdSer.SendStringCommand("e")
            time.sleep(0.03)


Skazat(text)
#ttsProcPlay(text)