import serial
from threading import Thread
import time

class mySerial(object):
    def __init__(self, parent=None):
        self.ser = serial.Serial()
        self.onMsg = None
    
    def connect(self, port):
        try:
            self.ser.port = port
            self.ser.baudrate = 115200
            self.ser.timeout = 0 # non-blocking read
            self.ser.open()
            self.th = Thread(target=self._th_read)
            self.th.start()
            return True            
        except serial.SerialException as e:
            print(e)
            return False        
            
    def sendMsg(self, msg):
        try:
            self.ser.write(msg + "\r")
        except serial.SerialException as e:
            print(e)
            
    def _th_read(self):
        while True:
            try:
                time.sleep(0.001)
                cmd = self.ser.readline().rstrip('\r\n')
                if cmd <> "":
                    if self.onMsg:
                        self.onMsg(cmd)
            except serial.SerialException as e:
                print(e)
            