import serial

class mySerial(object):
    def __init__(self, parent=None):
        self.ser = serial.Serial()
    
    def connect(self, port):
        try:
            self.ser.port = port
            self.ser.baudrate = 115200
            self.ser.open()
            return True            
        except serial.SerialException as e:
            print(e)
            return False        
            
    def sendMsg(self, msg):
        try:
            self.ser.write(msg + "\r")
        except serial.SerialException as e:
            print(e)