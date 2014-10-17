import serial
from threading import Thread
import time
import socket

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

class myNet(object):
    def __init__(self, parent=None):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.onMsg = None   
    
    def connect(self, ip, port):
        try:
            self.soc.connect((ip, port))
            self.th = Thread(target=self._th_read)
            self.th.start()
            return True            
        except Exception,e:
            print str(e)
            return False
  
    def sendMsg(self, msg):
        try:
            self.soc.sendall(msg + "\r\n")
        except AttributeError:
            print("Not connected yet!")
        except socket.error:
            print("Lost connection!")        

    def _th_read(self):
        self.soc.settimeout(1)
        buf = ""
        while True:
            try:
                s = self.soc.recv(1024)
                if s == "":
                    print("Disconnected")
                    break # if conn lost get out!
                buf = buf + s
                while "\r\n" in buf:
                    (cmd, buf) = buf.split("\r\n", 1)
                    if cmd <> "":
                        if self.onMsg:
                            self.onMsg(cmd)
            except socket.timeout:
                continue
            except socket.error:
                print("Lost connection!")
                break            
            