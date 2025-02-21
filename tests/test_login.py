import pytest
from bottle import Bottle, run, request, response
from bottle import template

@pytest.fixture
def app():
    app = Bottle()

    @app.route('/login', method=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.forms.get('username')
            password = request.forms.get('password')
            if username == 'testuser' and password == 'testpassword':
                response.status = 302
                return
            response.status = 401
            return "Unauthorized"
        return '''
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
                    <a href="/register">Registrar</a> | <a href="/forgot-password">Esqueci minha senha</a>
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        '''

    return app

@pytest.fixture
def client(app):
    from webtest import TestApp
    return TestApp(app)

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200, "Esperado status 200 para GET /login"
    assert 'Login' in response.text, "Esperado que 'Login' esteja no response.text de GET /login"

def test_login_user_success(client):
    response = client.post('/login', {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302, "Esperado status 302 para POST /login com credenciais corretas"

def test_login_user_failure(client):
    response = client.post('/login', {'username': 'wronguser', 'password': 'wrongpassword'}, expect_errors=True)
    assert response.status_code == 401, "Esperado status 401 para POST /login com credenciais incorretas"
    assert 'Unauthorized' in response.text, "Esperado que 'Unauthorized' esteja no response.text de POST /login com credenciais incorretas"
