from flask import Flask, render_template, session, redirect, url_for
from flask.ext.socketio import SocketIO, emit, disconnect
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
ws = SocketIO(app)
bootstrap = Bootstrap(app)
app.debug = True
thread = None

class NickForm(Form):
    name = StringField('Nickname: ', validators=[Required()])
    submit = SubmitField('Set Nickname')

@app.route('/chat')
def chat():
    if session.get('nick') != None:
        return render_template('index.html', nickname=session.get('nick'))
    else:
        return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get('nick') != None:
        return redirect(url_for('chat'))
    form = NickForm()
    
    if form.validate_on_submit():
        session['nick'] = form.name.data
        form.name.data = ""
        return redirect(url_for('chat'))
    
    return render_template('nick.html', form=form)

@ws.on('message sent')
def message_sent(message):
    emit('broadcast', message, broadcast=True)

if __name__ == '__main__':
    ws.run(app)
