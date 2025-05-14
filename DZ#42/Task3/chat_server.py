import socket
import threading
import json
import hashlib
import time
from datetime import datetime

class ChatServer:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = {}
        self.active_users = {}
        self.user_credentials = self.load_user_credentials()
        print(f"Сервер чата запущен на {host}:{port}")

    def load_user_credentials(self):
        try:
            with open('users.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'admin': {'password': self.hash_password('admin'), 'active': False}}

    def save_user_credentials(self):
        with open('users.json', 'w') as f:
            json.dump(self.user_credentials, f)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        if username in self.user_credentials:
            return False
        self.user_credentials[username] = {
            'password': self.hash_password(password),
            'active': False
        }
        self.save_user_credentials()
        return True

    def authenticate_user(self, username, password):
        if username not in self.user_credentials:
            return False
        stored_password = self.user_credentials[username]['password']
        return stored_password == self.hash_password(password)

    def broadcast(self, message, sender=None):
        current_time = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{current_time}] {message}"
        
        for client, user_info in list(self.clients.items()):
            try:
                client.send(formatted_message.encode('utf-8'))
            except:
                self.remove_client(client, user_info['username'])

    def remove_client(self, client, username):
        if client in self.clients:
            del self.clients[client]
            if username in self.active_users:
                del self.active_users[username]
                self.user_credentials[username]['active'] = False
                self.broadcast(f"Пользователь {username} покинул чат")
                print(f"Пользователь {username} отключился")

    def handle_client(self, conn, addr):
        username = None
        try:
            # Получаем тип операции (логин/регистрация)
            operation = conn.recv(1024).decode('utf-8')
            
            if operation.startswith("REGISTER"):
                _, username, password = operation.split()
                if self.register_user(username, password):
                    conn.send("REGISTER_SUCCESS".encode('utf-8'))
                else:
                    conn.send("REGISTER_FAIL".encode('utf-8'))
                    conn.close()
                    return
            
            elif operation.startswith("LOGIN"):
                _, username, password = operation.split()
                if not self.authenticate_user(username, password):
                    conn.send("LOGIN_FAIL".encode('utf-8'))
                    conn.close()
                    return
                
                if self.user_credentials[username]['active']:
                    conn.send("ALREADY_LOGGED_IN".encode('utf-8'))
                    conn.close()
                    return
                
                conn.send("LOGIN_SUCCESS".encode('utf-8'))
                self.user_credentials[username]['active'] = True
            else:
                conn.close()
                return

            # Добавляем клиента в список активных
            self.clients[conn] = {'username': username, 'addr': addr}
            self.active_users[username] = conn
            self.broadcast(f"Пользователь {username} присоединился к чату")
            print(f"Пользователь {username} подключился с {addr}")

            # Обрабатываем сообщения от клиента
            while True:
                message = conn.recv(1024).decode('utf-8')
                if not message:
                    break
                
                if message == "LOGOUT":
                    self.remove_client(conn, username)
                    break
                
                if message.startswith("@"):
                    # Личное сообщение
                    recipient, _, msg = message[1:].partition(' ')
                    if recipient in self.active_users:
                        private_msg = f"[ЛС от {username}] {msg}"
                        self.active_users[recipient].send(private_msg.encode('utf-8'))
                        conn.send(f"[ЛС для {recipient}] {msg}".encode('utf-8'))
                    else:
                        conn.send(f"Пользователь {recipient} не в сети".encode('utf-8'))
                else:
                    # Общее сообщение
                    self.broadcast(f"{username}: {message}")

        except Exception as e:
            print(f"Ошибка с клиентом {addr}: {e}")
        finally:
            if username:
                self.remove_client(conn, username)
            conn.close()

    def start(self):
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    server = ChatServer()
    server.start()