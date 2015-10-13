from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
ws = SocketIO(app)
app.debug = True
thread = None

@app.route('/')
def index():
    return render_template('index.html')

@ws.on('message sent')
def message_sent(message):
    emit('broadcast', message, broadcast=True)
if __name__ == '__main__':
    ws.run(app)
