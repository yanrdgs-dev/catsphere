import eventlet
eventlet.monkey_patch()

from bottle import Bottle, route, run, request, static_file, redirect, template, response
import socketio
from app.controllers.application import Application
from datetime import datetime

app = Bottle()
ctl = Application()

sio = socketio.Server(async_mode='eventlet')
app_sio = socketio.WSGIApp(sio, app)

@app.route("/static/<filepath:path>")
def serve_static(filepath):
    return static_file(filepath, root="./app/static")

@app.route("/")
def index(info=None):
    return ctl.render("index")

# Rotas login
@app.route("/login", method="GET")
def login():
    return ctl.render("login")

@app.route("/login", method="POST")
def do_login():
    username = request.forms.get("username")
    password = request.forms.get("password")
    
    print(f"Tentativa de login com usuário: {username} e senha: {password}")
    auth_result = ctl.authenticate_user(username, password)
    if auth_result:
        session_id, username = auth_result
        print(f"Login bem-sucedido. Session id inserido: {session_id}")
        response.set_cookie("session_id", session_id, secure=False, max_age=3600)
        redirect("/chatrooms")
    else:
        print("Falha no login. Nome de usuário ou senha incorretos.")
        return ctl.render("login", {"error": "Nome de usuário ou senha incorretos"})

# Rotas registro
@app.route("/register", method="GET")
def register():
    return ctl.render("register")

@app.route("/register", method="POST")
def do_register():
    username = request.forms.get("username")
    password = request.forms.get("password")
    
    if ctl.register_user(username, password):
        redirect("/login")
    else:
        return ctl.render("register", {"error": "Usuário já existe"})
    
# Rotas user_data
@app.route("/user_data", method="GET")
@app.route("/user_data/<username>", method="GET")
def do_pagina(username=None):
    if not username:
        return redirect('/login')
    else:
        return ctl.render("user_data", {"username": username})

# Rota logout
@app.route("/logout", method="GET")
def logout():
    ctl.logout_user()
    redirect('/')

@app.route('/chat')
def chat():
    return template('app/views/html/chat')

@app.route("/chatrooms", method="GET")
def chatrooms():
    return ctl.render("chatrooms")

@app.route("/admin/create_chatroom", method="POST")
def create_chatroom():
    name = request.forms.get("name")
    ctl.create_chatroom(name)
    return redirect("/admin")

@app.route("/admin", method="GET")
def admin():
    return ctl.render("admin")

@app.route("/is_admin", method="GET")
def is_admin():
    session_id = request.get_cookie("session_id")
    current_user = ctl._Application__db.get_current_user(session_id)
    if current_user and ctl._Application__db.is_admin(current_user.username):
        return f"Usuário {current_user.username} é admin."
    else:
        return "Usuário não é admin ou não está autenticado."

@app.route("/chatroom/<chatroom_name>", method="GET")
def chatroom(chatroom_name):
    print(f"Rota acessada: /chatroom/{chatroom_name}")
    return ctl.render("chatroom", {"chatroom_name": chatroom_name})

@app.route("/admin/delete_all_messages", method="POST")
def delete_all_messages():
    ctl.delete_all_messages()
    return redirect("/admin")

@sio.on('send_message')
def handle_send_message(sid, data):
    username = data['username']
    chatroom_name = data['chatroom_name']
    message = data['message']
    chatroom = ctl.send_message(chatroom_name, username, message)
    if chatroom:
        timestamp = datetime.now().strftime('%H:%M:%S')
        sio.emit('receive_message', {'chatroom_name': chatroom_name, 'username': username, 'message': message, 'timestamp': timestamp}, room=chatroom_name)

@sio.on('join')
def handle_join(sid, data):
    chatroom_name = data['chatroom_name']
    username = data['username']
    sio.enter_room(sid, chatroom_name)
    print(f"Usuário {username} ({sid}) entrou no chatroom {chatroom_name}")
    sio.emit('user_joined', {'chatroom_name': chatroom_name, 'username': username}, room=chatroom_name)

@sio.on('leave')
def handle_leave(sid, data):
    chatroom_name = data['chatroom_name']
    username = data['username']
    sio.leave_room(sid, chatroom_name)
    print(f"Usuário {username} ({sid}) saiu do chatroom {chatroom_name}")
    sio.emit('user_left', {'chatroom_name': chatroom_name, 'username': username}, room=chatroom_name)

@app.route("/chatroom/<chatroom_name>/send", method="POST")
def send_message(chatroom_name):
    username = request.get_cookie("username")
    message = request.forms.get("message")
    ctl.send_message(chatroom_name, username, message)
    return redirect(f"/chatroom/{chatroom_name}")

@sio.event
def connect(sid, environ):
    print('Cliente conectado:', sid)
    ctl.clients.append(sid)

@sio.event
def disconnect(sid):
    print('Cliente desconectado:', sid)
    ctl.clients.remove(sid)

@sio.event
def message(sid, data):
    print('Mensagem recebida:', data)
    for client in ctl.clients:
        if client != sid:
            sio.send(data, to=client)

if __name__ == "__main__":
    import eventlet.wsgi
    print("Servidor iniciado e ouvindo em http://0.0.0.0:8080")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), app_sio)