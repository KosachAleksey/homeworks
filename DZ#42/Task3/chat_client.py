import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

class ChatClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.logged_in = False
        
        # GUI
        self.root = tk.Tk()
        self.root.title("Чат-приложение")
        
        # Окно авторизации
        self.show_login_window()
        
        # Запускаем основной цикл
        self.root.mainloop()
    
    def show_login_window(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Авторизация")
        self.login_window.grab_set()
        
        tk.Label(self.login_window, text="Логин:").grid(row=0, column=0, padx=5, pady=5)
        self.login_entry = tk.Entry(self.login_window)
        self.login_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.login_window, text="Пароль:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.login_button = tk.Button(self.login_window, text="Войти", command=self.login)
        self.login_button.grid(row=2, column=0, padx=5, pady=5)
        
        self.register_button = tk.Button(self.login_window, text="Регистрация", command=self.register)
        self.register_button.grid(row=2, column=1, padx=5, pady=5)
        
        self.status_label = tk.Label(self.login_window, text="", fg="red")
        self.status_label.grid(row=3, column=0, columnspan=2)
    
    def show_chat_window(self):
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.title(f"Чат - {self.username}")
        self.chat_window.protocol("WM_DELETE_WINDOW", self.logout)
        
        # История сообщений
        self.chat_history = scrolledtext.ScrolledText(self.chat_window, state='disabled')
        self.chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Поле ввода сообщения
        self.message_frame = tk.Frame(self.chat_window)
        self.message_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.message_entry = tk.Entry(self.message_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(self.message_frame, text="Отправить", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        
        # Кнопка выхода
        self.logout_button = tk.Button(self.chat_window, text="Выйти", command=self.logout)
        self.logout_button.pack(pady=5)
        
        # Запускаем поток для получения сообщений
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()
    
    def connect_to_server(self):
        try:
            self.client.connect((self.host, self.port))
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось подключиться к серверу: {e}")
            return False
    
    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_label.config(text="Введите логин и пароль")
            return
        
        if not self.connect_to_server():
            return
        
        self.client.send(f"LOGIN {username} {password}".encode('utf-8'))
        response = self.client.recv(1024).decode('utf-8')
        
        if response == "LOGIN_SUCCESS":
            self.username = username
            self.logged_in = True
            self.login_window.d