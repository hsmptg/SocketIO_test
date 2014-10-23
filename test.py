#import gevent.monkey
#gevent.monkey.patch_thread()

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

def main():
    print('test running...')
    app = Flask(__name__)
    Bootstrap(app)
    app.debug = True    
    socketio = SocketIO(app)
      
    @app.route('/')
    def index():
        print('Rendering index.html')
        return render_template('index3.html')

    socketio.run(app, host = '0.0.0.0', port = 5001)    

#===============================================================================
# print('test running...')
# app = Flask(__name__)
# Bootstrap(app)
# app.debug = True    
# socketio = SocketIO(app)
#  
# @app.route('/')
# def index():
#     print('Rendering index.html')
#     return render_template('index3.html')
#===============================================================================
    
if __name__ == '__main__':
    main()
#    socketio.run(app, host = '0.0.0.0', port = 5001) 