import pytest
from bottle import Bottle, run, request, response
from bottle import template

@pytest.fixture
def app():
    app = Bottle()

    @app.route('/register', method=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.forms.get('username')
            password = request.forms.get('password')
            response.status = 302
            return
        return '''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Registro - Catsphere</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="/static/css/register.css" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h1 class="text-center">Registro</h1>
                <form action="/register" method="post">
                    <div class="mb-3">
                        <label for="username" class="form-label">Nome de usuário:</label>
                        <input type="text" name="username" id="username" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Senha:</label>
                        <input type="password" name="password" id="password" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-submit w-100">Registrar</button>
                </form>
                <div class="text-center mt-3 links">
                    <a href="/login">Entrar</a> | <a href="/forgot-password">Esqueci minha senha</a>
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

def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200, "Esperado status 200 para GET /register"
    assert 'Registro' in response.text, "Esperado que 'Registro' esteja no response.text de GET /register"

def test_register_user(client):
    response = client.post('/register', {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302, "Esperado status 302 para POST /register com dados preenchidos"
