import serial
import time



class ArdunoSender:

    def __init__(self,Port = "/dev/ttyACM0",Baudrate = 9600,TimeOut=1):
        self.Port = Port
        self.Baudrate = Baudrate
        self.TimeOut=TimeOut
        self.Ser = serial.Serial()
        self.Ser.baudrate = self.Baudrate
        self.Ser.port = self.Port
        self.Ser.timeout = self.TimeOut

        self.Ser.open()
        print("Serial port opened success")
    def __enter__(self):
        return self.Ser
    def __exit__(self, type, value, traceback):
        self.Ser.close()

    def Send (self,Command):


        self.Ser.write(Command)

    def SendStringCommand(self,String):
        String = str(String)
        if len(String)>1:
            print("Warning string must be 1 symbol, take first symbol")
        self.Send(String[0].encode('utf-8'))

    def SerialReadLines(self):
        InLines=[]
        while self.Ser.in_waiting:
            InLines.append(self.Ser.readline())
        return InLines


















