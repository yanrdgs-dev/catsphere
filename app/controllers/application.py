from bottle import template, request, response, redirect
from app.controllers.database import Database

class Application():
    def __init__(self):
        self.pages = {
            "index": self.index,
            "login": self.login,
            "user_data": self.user_data,
            "register": self.register,
            "admin": self.admin,
            "chatrooms": self.chatrooms,
            "chatroom": self.chatroom
        }
        self.__db = Database()
        self.clients = []
    
    def render(self, page, params=None):
        content = self.pages.get(page, self.page_not_found)
        if params is None:
            params = {}
        return content(**params)
        
    def index(self, **params):
        return template("app/views/html/index.tpl", **params)
    
    def login(self, **params):
        return template("app/views/html/login.tpl", **params)
    
    def register(self, **params):
        return template("app/views/html/register.tpl", **params)
    
    def page_not_found(self, **params):
        return template("app/views/html/404.tpl", **params)
    
    def user_data(self, username=None, **params):
        if self.is_authenticated(username):
            session_id = self.get_session_id()
            user = self.__db.get_current_user(session_id)
            print(f"User Data sendo enviado ao servidor: {user.username}")
            return template("app/views/html/user_data.tpl", current_user=user, **params)
        else:
            return template("app/views/html/404.tpl", **params)
        
    def get_session_id(self):
        session_id = request.get_cookie("session_id")
        print(f"Session ID atual (Cookie): {session_id}")
        return session_id
    
    def is_authenticated(self, username):
        session_id = self.get_session_id()
        current_username = self.__db.get_username(session_id)
        print(f"IS AUTHENTICATED: Usuário autenticado: {current_username}")
        return username == current_username
    
    def authenticate_user(self, username, password):
        session_id = self.__db.check_user(username, password)
        if session_id:
            self.logout_user()
            print("AUTHENTICATE_USER: Usuário foi autenticado. Username: ", username)
            return session_id, username
        return None
    
    def logout_user(self):
        session_id = self.get_session_id()
        if session_id:
            self.__db.logout_user(session_id)
            response.delete_cookie("session_id")
            print("Usuário deslogado com sucesso.")
    
    def register_user(self, username, password):
        if self.__db.get_session_id(username) is None:
            self.__db.write(username, password)
            return True
        return False

    def admin(self, **params):
        session_id = self.get_session_id()
        current_user = self.__db.get_current_user(session_id)
        if current_user and self.__db.is_admin(current_user.username):
            return template("app/views/html/admin.tpl", users=self.__db.get_all_users(), current_user=current_user, **params)
        else:
            return template("app/views/html/404.tpl", **params)
    
    def chatrooms(self, **params):
        chatrooms = self.__db.get_chatrooms()
        current_user = self.__db.get_current_user(self.get_session_id())
        return template("app/views/html/chatrooms.tpl", chatrooms=chatrooms, current_user=current_user, **params)
    
    def create_chatroom(self, name):
        self.__db.create_chatroom(name)

    def chatroom(self, chatroom_name, **params):
        print(f"Tentando acessar o chatroom: {chatroom_name}")
        chatroom = self.__db.get_chatroom(chatroom_name)
        current_user = self.__db.get_current_user(self.get_session_id())
        if chatroom and current_user:
            print(f"Chatroom encontrado: {chatroom.name}")
            return template("app/views/html/chatroom.tpl", chatroom=chatroom, current_user=current_user, **params)
        else:
            print("Chatroom não encontrado ou usuário não autenticado")
            return redirect("/login")
    
    def send_message(self, chatroom_name, username, message):
        self.__db.add_message_to_chatroom(chatroom_name, username, message)
        return self.__db.get_chatroom(chatroom_name)
    
    def delete_all_messages(self):
        self.__db.delete_all_messages()
