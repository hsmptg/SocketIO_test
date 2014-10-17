from flask import Flask, render_template
from flask_socketio import SocketIO
import myComm

ser = myComm.mySerial()

print('Flask-SocketIO running...')
app = Flask(__name__)
app.debug = False
socketio = SocketIO(app)

@app.before_first_request
def initialize():
    print('Called only once, when the first request comes in')
    ser.connect('COM5')      
        
@app.route('/')
def index():
    print('Rendering index.html')
    return render_template('index.html')

@socketio.on('ledCtrl', namespace='/test')
def ledCtrl(message):
    print(message['led'])
    if message['led']:
        ser.sendMsg('l1')
    else:
        ser.sendMsg('l0')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)