from datetime import datetime

class Chatroom:
    def __init__(self, name, messages=None):
        self.name = name
        self.messages = messages if messages is not None else []
    
    def add_message(self, username, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.messages.append({"username": username, "message": message, "timestamp": timestamp})
