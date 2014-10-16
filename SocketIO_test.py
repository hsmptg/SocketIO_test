from flask import Flask, render_template
from flask_socketio import SocketIO

print("Flask-SocketIO running...")
app = Flask(__name__)
app.debug = False
socketio = SocketIO(app)

@app.before_first_request
def initialize():
    print "Called only once, when the first request comes in"        
        
@app.route('/')
def index():
    print('Rendering index.html')
    return render_template('index.html')

@socketio.on('ledCtrl', namespace='/test')
def ledCtrl(message):
    print(message['led'])

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)