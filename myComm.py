import serial
import threading
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
            self.t1_stop = threading.Event()
            self.th = threading.Thread(target = self._th_read, args=(1, self.t1_stop))
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
            
    def _th_read(self, arg1, stop_event):
        while(not stop_event.is_set()):
            stop_event.wait(.001)        
            try:
                cmd = self.ser.readline().rstrip('\r\n')
                if cmd <> "":
                    if self.onMsg:
                        self.onMsg(cmd)
            except serial.SerialException as e:
                print(e)
                
    def stop(self):
        self.t1_stop.set()
        self.th.join()

class myNet(object):
    def __init__(self, parent=None):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.onMsg = None   
    
    def connect(self, ip, port):
        try:
            self.soc.connect((ip, port))
            self.t1_stop = threading.Event()
            self.th = threading.Thread(target = self._th_read, args=(1, self.t1_stop))
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

    def _th_read(self, arg1, stop_event):
        self.soc.settimeout(1)
        buf = ""
        while(not stop_event.is_set()):
#            stop_event.wait(.001)        
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

    def stop(self):
        self.t1_stop.set()
        self.th.join()
            