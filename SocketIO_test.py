from flask import Flask, render_template
from flask_socketio import SocketIO
import serial

ser = serial.Serial()

print("Flask-SocketIO running...")
app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

@app.before_first_request
def initialize():
    print "Called only once, when the first request comes in"       
    try:
        ser.port = "/dev/ttyACM0"
        ser.baudrate = 115200
        ser.open()
    except serial.SerialException as e:
        print(e)
                    
@app.route('/')
def index():
    print('Rendering index.html')
    return render_template('index.html')

@socketio.on('ledCtrl', namespace='/test')
def ledCtrl(message):
    print(message['led'])
    if message['led']:
        ser.write('l1\r')
    else:
        ser.write('l0\r')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)