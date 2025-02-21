from app.models.users import User, Admin
from app.models.chatroom import Chatroom
import json
import uuid
from datetime import datetime

class Database():
    def __init__(self):
        self.__user_accounts = []
        self.__authenticated_users = {}
        self.__admins = []
        self.__chatrooms = []
        self.read()
        self.__initialize_admin()
    
    def read(self):
        try:
            with open("app/controllers/db/users.json", "r") as file:
                user_data = json.load(file)
                self.__user_accounts = [User(**data) for data in user_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.__user_accounts.append(User("convidado", "000000"))
        
        try:
            with open("app/controllers/db/chatrooms.json", "r") as file:
                chatroom_data = json.load(file)
                self.__chatrooms = [Chatroom(**data) for data in chatroom_data]
                for chatroom in self.__chatrooms:
                    for message in chatroom.messages:
                        if 'timestamp' not in message:
                            message['timestamp'] = datetime.now().strftime('%H:%M:%S')
        except (FileNotFoundError, json.JSONDecodeError):
            self.__chatrooms.append(Chatroom("General"))
            
    def write_users(self):
        with open("app/controllers/db/users.json", "w") as file:
            user_data = [vars(user_account) for user_account in self.__user_accounts + self.__admins]
            json.dump(user_data, file, indent=4)
    
    def write_chatrooms(self):
        with open("app/controllers/db/chatrooms.json", "w") as file:
            chatroom_data = [vars(chatroom) for chatroom in self.__chatrooms]
            json.dump(chatroom_data, file, indent=4)
    
    def create_chatroom(self, name):
        new_chatroom = Chatroom(name)
        self.__chatrooms.append(new_chatroom)
        self.write_chatrooms()
    
    def get_chatrooms(self):
        return self.__chatrooms
    
    def get_chatroom(self, name):
        return next((chatroom for chatroom in self.__chatrooms if chatroom.name == name), None)
    
    def get_current_user(self, session_id):
        if session_id in self.__authenticated_users:
            user = self.__authenticated_users[session_id]
            username = user.username
            print("GET_CURRENT_USER: Usuário: ", username)
            return user
        else:
            return None  
    
    def get_username(self, session_id):
        print(f"Authenticated users: {self.__authenticated_users}")
        print(f"Session ID: {session_id}")
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id].username
        else:
            print("Não entrou no if do get_username")
            return None
    
    def get_session_id(self, username):
        for session_id in self.__authenticated_users:
            if self.__authenticated_users[session_id].username == username:
                return session_id
        return None
    
    def check_user(self, username, password):
        print(f"Verificando usuário: {username}")
        for user in self.__user_accounts + self.__admins:
            print(f"Checando usuário: {user.username} com senha: {user.password}")
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4())
                self.__authenticated_users[session_id] = user
                print(f"CHECK_USER: Usuário checado e está autenticado. Session ID: {session_id}")
                return session_id
        print("Usuário ou senha incorretos.")
        return None

    def logout_user(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]

    def __initialize_admin(self):
        admin_user = next((user for user in self.__user_accounts if user.username == "admin"), None)
        if admin_user:
            self.__user_accounts.remove(admin_user)
            self.__admins.append(Admin(admin_user.username, admin_user.password))
        else:
            self.__admins.append(Admin("admin", "admin"))

    def is_admin(self, username):
        return any(admin.username == username for admin in self.__admins)

    def get_all_users(self):
        return self.__user_accounts + self.__admins

    def add_message_to_chatroom(self, chatroom_name, username, message):
        chatroom = self.get_chatroom(chatroom_name)
        if chatroom:
            chatroom.add_message(username, message)
            self.write_chatrooms()
            return chatroom
        return None

    def write(self, username, password, is_admin=False):
        if is_admin:
            new_user = Admin(username, password)
            self.__admins.append(new_user)
        else:
            new_user = User(username, password)
            self.__user_accounts.append(new_user)
        self.write_users()

    def delete_all_messages(self):
        for chatroom in self.__chatrooms:
            chatroom.messages = []
        self.write_chatrooms()