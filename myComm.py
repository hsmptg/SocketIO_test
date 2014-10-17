import serial
from threading import Thread

class mySerial(object):
    def __init__(self, parent=None):
        self.ser = serial.Serial()
        self.onMsg = None
    
    def connect(self, port):
        try:
            self.ser.port = port
            self.ser.baudrate = 115200
            self.ser.timeout = 1
            self.ser.open()
            self.th = Thread(target=self._th_read)
            self.th.daemon = True
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
                cmd = self.ser.readline().rstrip('\n')
                if cmd <> "":
                    if self.onMsg:
                        self.onMsg(cmd)
            except serial.SerialException as e:
                print(e)
            