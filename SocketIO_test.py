import gevent.monkey
gevent.monkey.patch_thread()

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
import myComm

import sys #exit
import signal #signal

net = 0
ser = 0
socketio = 0

def signal_handler(signal, frame):
    print('\rYou pressed Ctrl+C!')
    ser.stop()
    net.stop()
    print('Exit!')
    sys.exit(0)
    
def onSerialMsg(msg):
    global socketio
    
    print(msg)
    but = True if msg=='b1' else False
#    but = True if msg=='BUT oN' else False
    socketio.emit('butAState', {'but': but}, namespace='/test')

def onNetMsg(msg):
    global socketio
    
    print(msg)
    but = True if msg=='Button ON' else False
    socketio.emit('butRState', {'but': but}, namespace='/test')
    
def main():
    global socketio
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print('Flask-SocketIO running...')
    app = Flask(__name__)
    Bootstrap(app)
    app.debug = False    
    socketio = SocketIO(app)

    ser = myComm.mySerial()
    net = myComm.myNet()
    
    @app.before_first_request
    def initialize():
        print('Called only once, when the first request comes in')
        ser.onMsg = onSerialMsg
        ser.connect('COM3')
#        ser.connect('COM5')
#        ser.connect('/dev/ttyACM0')
        net.onMsg = onNetMsg
        net.connect('192.168.1.91', 12345)
#        net.connect('10.0.0.4', 12345)
    
    @app.route('/')
    def index():
        print('Rendering index.html')
        return render_template('index.html')
    
    @app.route('/2')
    def index2():
        return render_template('index2.html')

    @socketio.on('ledACtrl', namespace='/test')
    def ledACtrl(message):
        print(message['led'])
        if message['led']:
            ser.sendMsg('l1')
        else:
            ser.sendMsg('l0')
    
    @socketio.on('ledRCtrl', namespace='/test')
    def ledRCtrl(message):
        print(message['led'])
        if message['led']:
            net.sendMsg('l1')
        else:
            net.sendMsg('l0')

    socketio.run(app, host = '0.0.0.0', port = 5001)
        
if __name__ == '__main__':
    main()