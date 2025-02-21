<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ chatroom.name }} - Catsphere</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/css/chatroom.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">Catsphere</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link" href="/chatrooms">Chatrooms</a>
                    </li>
                    % if current_user:
                        <li class="nav-item">
                            <a class="nav-link" href="/user_data/{{ current_user.username }}">Dados do Usuário</a>
                        </li>
                    % end
                    % if current_user and current_user.username == 'admin':
                        <li class="nav-item">
                            <a class="nav-link" href="/admin">Admin</a>
                        </li>
                    % end
                </ul>
                <ul class="navbar-nav">
                    % if current_user:
                        <li class="nav-item">
                            <a class="nav-link" href="/logout">Logout</a>
                        </li>
                    % else:
                        <li class="nav-item">
                            <a class="nav-link" href="/login">Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/register">Register</a>
                        </li>
                    % end
                </ul>
            </div>
        </div>
    </nav>
    <div class="container">
        <h1 class="text-center">{{ chatroom.name }}</h1>
        <ul class="list-group mb-3" id="messages">
            % for message in chatroom.messages:
                <li class="list-group-item">
                    <span class="timestamp">{{ message['timestamp'] }}</span> <strong>{{ message['username'] }}:</strong> {{ message['message'] }}
                </li>
            % end
        </ul>
        <form id="messageForm">
            <div class="mb-3">
                <label for="message" class="form-label">No que você está pensando, {{ current_user.username }}?</label>
                <input type="text" name="message" id="message" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-submit w-100">Enviar</button>
        </form>
        <input type="hidden" id="chatroomName" value="{{ chatroom.name }}">
        <input type="hidden" id="username" value="{{ current_user.username }}">
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <script>
        const socket = io();
        const chatroomName = document.getElementById('chatroomName').value;
        const username = document.getElementById('username').value;

        function playMessageSound() {
            const audio = new Audio('/static/sounds/message-received.mp3');
            audio.play();
        }

        function playJoinSound() {
            const audio = new Audio('/static/sounds/chat-joined.mp3');
            audio.play();
        }

        socket.emit('join', { chatroom_name: chatroomName, username: username });

        document.getElementById('messageForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const message = document.getElementById('message').value;
            socket.emit('send_message', { chatroom_name: chatroomName, username: username, message: message });
            document.getElementById('message').value = '';
        });

        socket.on('receive_message', function(data) {
            if (data.chatroom_name === chatroomName) {
                const messageElement = document.createElement('li');
                messageElement.classList.add('list-group-item', 'message');
                messageElement.innerHTML = `<span class="timestamp">${data.timestamp}</span> <strong>${data.username}:</strong> ${data.message}`;
                document.getElementById('messages').appendChild(messageElement);

                // Toca o som
                playMessageSound();
            }
        });

        socket.on('user_joined', function(data) {
            if (data.chatroom_name === chatroomName) {
                const messageElement = document.createElement('li');
                messageElement.classList.add('list-group-item', 'message');
                messageElement.innerHTML = `<span class="timestamp">[Sistema]</span> <strong>${data.username}</strong> entrou no chatroom.`;
                playJoinSound();
                document.getElementById('messages').appendChild(messageElement);
            }
        });

        socket.on('user_left', function(data) {
            if (data.chatroom_name === chatroomName) {
                const messageElement = document.createElement('li');
                messageElement.classList.add('list-group-item', 'message');
                messageElement.innerHTML = `<span class="timestamp">[Sistema]</span> <strong>${data.username}</strong> saiu do chatroom.`;
                document.getElementById('messages').appendChild(messageElement);
            }
        });

        window.addEventListener('beforeunload', function() {
            console.log('Emitindo evento leave');
            socket.emit('leave', { chatroom_name: chatroomName, username: username });
        });
    </script>
</body>
</html>
