import os, sys
import hashlib

# Config
if not os.path.exists('config.py'):
    import shutil
    shutil.copyfile('config.default.py', 'config.py')
import config

# Flask
from flask import Flask, render_template, request, session, redirect, url_for, abort
from flaskutil import jsonify

app = Flask(__name__)

# Session
app.secret_key = config.session_secret

from werkzeug import SharedDataMiddleware
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/': os.path.join(os.path.dirname(__file__), 'static')
})

from flask.ext.compress import Compress
Compress(app)

# Quassel
from quassel import quassel_session
from quassel import QuasselUser, Message, Buffer, Sender, Network
from quassel import MessageType, BufferType

def new_db_session():
    return quassel_session(config.quassel_db_uri)

# Views
@app.route('/')
def index():
    if 'quasseluser_id' not in session:
        return redirect(url_for('login'))
    template_data = {}
    return render_template('page/index.html', **template_data)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        template_data = {}
        return render_template('page/login.html', **template_data)
    elif request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')

        if username and password:
            db = new_db_session()
            quasseluser = db.query(QuasselUser).filter(QuasselUser.username == username).first()
            db.close()

            password_hash = hashlib.sha1(str.encode(password)).hexdigest()
            if password_hash == quasseluser.password:
                # Login Success
                session['quasseluser_id'] = quasseluser.userid
                session['quasseluser_username'] = quasseluser.username
                return redirect(url_for('index'))

        # Login Failed
        template_data = {}
        template_data['username'] = username
        template_data['password'] = password
        return render_template('page/login.html', **template_data)

@app.route('/logout/')
def logout():
    session.pop('quasseluser_id', None)
    session.pop('quasseluser_username', None)
    return redirect(url_for('login'))

@app.route('/api/get_state/')
def api_get_state():
    if 'quasseluser_id' not in session:
        return abort(403)
    
    db = new_db_session()

    query = db.query(Network)
    query = query.filter(Network.userid == session['quasseluser_id'])
    networks = query.all()

    query = db.query(Buffer)
    query = query.filter(Buffer.userid == session['quasseluser_id'])
    buffers = query.all()

    db.close()

    state = {}
    state['networks'] = []
    for n in networks:
        if not n.connected:
            continue

        network = {
            'id': n.id,
            'name': n.name,
            'connected': n.connected,
            'buffers': [],
        }
        for b in buffers:
            if b.networkid != n.id:
                continue
            elif b.type == BufferType.Network:
                continue
            elif b.type == BufferType.Channel and not b.joined:
                continue
            elif b.type == BufferType.Query and b.lastseenmsgid == b.markerlinemsgid:
                continue

            buffer = b.to_dict()
            network['buffers'].append(buffer)
        network['buffers'] = sorted(network['buffers'], key=lambda b: b['name'].lower())
        state['networks'].append(network)
    state['networks'] = sorted(state['networks'], key=lambda n: n['name'].lower())

    data = {}
    data['state'] = state
    data['networks'] = [n.to_dict() for n in networks]
    data['buffers'] = [b.to_dict() for b in buffers]
    return jsonify(data)

@app.route('/api/get_messages/')
def api_get_messages():
    if 'quasseluser_id' not in session:
        return abort(403)

    buffer_id = int(request.args.get('buffer'))
    
    db = new_db_session()

    query = db.query(Buffer)
    query = query.filter(Buffer.userid == session['quasseluser_id'])
    query = query.filter(Buffer.id == buffer_id)
    buffer = query.first()

    query = db.query(Message)
    query = query.filter(Message.bufferid == buffer_id)
    count_all = query.count()
    query = query.filter(Message.type != MessageType.Join)
    query = query.filter(Message.type != MessageType.Part)
    query = query.filter(Message.type != MessageType.Quit)
    query = query.filter(Message.type != MessageType.NetsplitJoin)
    query = query.filter(Message.type != MessageType.NetsplitQuit)
    query = query.filter(Message.type != MessageType.Mode)
    query = query.filter(Message.type != MessageType.Nick)
    count_filtered = query.count()

    end = count_filtered
    start = max(end - 100, 0)
    messages = query[start:end]

    sender_ids = [m.senderid for m in messages]
    senders = []
    if len(sender_ids) > 0:
        senders = db.query(Sender).filter(Sender.id.in_(sender_ids)).all()
    sender_names = {s.id: s.name for s in senders}

    messages2 = []
    for m in messages:
        sender_name = sender_names[m.senderid]
        nick = sender_name
        if nick and '!' in nick:
            nick = nick[0:nick.find('!')]
        message = {
            'id': m.id,
            'message': m.message,
            'time': m.time,
            'type': m.type,
            'sender': {
                'id': m.senderid,
                'name': nick,
                'hash': hash(sender_name) % 16,
            },
        }
        messages2.append(message)


    db.close()

    data = {}
    data['count_all'] = count_all
    data['count_filtered'] = count_filtered
    data['messages'] = messages2
    return jsonify(data)


if __name__ == '__main__':
    app.run(host=config.host, port=config.port, debug=config.debug)
