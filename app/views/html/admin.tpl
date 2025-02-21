<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administração - Catsphere</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/css/admin.css" rel="stylesheet">
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
        <h1 class="text-center">Página de Administração</h1>
        <h2 class="mt-4">Usuários</h2>
        <ul class="list-group">
            % for user in users:
                <li class="list-group-item">{{ user.username }}</li>
            % end
        </ul>
        <h2 class="mt-4">Criar Chatroom</h2>
        <form action="/admin/create_chatroom" method="post">
            <div class="mb-3">
                <label for="name" class="form-label">Nome do Chatroom:</label>
                <input type="text" name="name" id="name" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-submit w-100">Criar</button>
        </form>
        <h2 class="mt-4">Deletar Todas as Mensagens</h2>
        <form action="/admin/delete_all_messages" method="post">
            <button type="submit" class="btn btn-danger w-100">Deletar Todas as Mensagens</button>
        </form>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
