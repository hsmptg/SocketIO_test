from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

print("Flask-SocketIO running...")
app = Flask(__name__)
app.debug = False
socketio = SocketIO(app)

@app.before_first_request
def initialize():
    print "Called only once, when the first request comes in"        
        
@app.route('/')
def index():
    print('index')
    return render_template('index.html')

@socketio.on('ledCtrl', namespace='/test')
def ledACtrl(message):
    print(message['led'])

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)