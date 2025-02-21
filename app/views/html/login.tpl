<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Catsphere</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/css/login.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="text-center">Login</h1>
        <form action="/login" method="post">
            <div class="mb-3">
                <label for="username" class="form-label">Nome de usuário:</label>
                <input type="text" name="username" id="username" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Senha:</label>
                <input type="password" name="password" id="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-submit w-100">Entrar</button>
        </form>
        <div class="text-center mt-3 links">
            <a href="/register">Cadastrar</a> | <a href="/forgot-password">Esqueci minha senha</a>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
