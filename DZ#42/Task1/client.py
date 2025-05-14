import socket
import json
import tkinter as tk
from tkinter import messagebox

class TicTacToeClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.symbol = None
        self.current_turn = None
        self.board = [' ' for _ in range(9)]
        self.game_active = False
        
        # GUI
        self.root = tk.Tk()
        self.root.title("Крестики-нолики")
        
        self.status_label = tk.Label(self.root, text="Подключение к серверу...", font=('Arial', 14))
        self.status_label.pack(pady=10)
        
        self.start_button = tk.Button(self.root, text="Начать игру", command=self.start_game, state=tk.DISABLED)
        self.start_button.pack(pady=5)
        
        self.quit_button = tk.Button(self.root, text="Выйти из игры", command=self.quit_game, state=tk.DISABLED)
        self.quit_button.pack(pady=5)
        
        self.restart_button = tk.Button(self.root, text="Начать заново", command=self.request_restart, state=tk.DISABLED)
        self.restart_button.pack(pady=5)
        
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)
        self.buttons = []
        for i in range(9):
            row, col = divmod(i, 3)
            button = tk.Button(self.board_frame, text=' ', font=('Arial', 20), width=5, height=2,
                               command=lambda idx=i: self.make_move(idx), state=tk.DISABLED)
            button.grid(row=row, column=col)
            self.buttons.append(button)
        
        self.connect_to_server()
        
    def connect_to_server(self):
        try:
            self.client.connect((self.host, self.port))
            threading.Thread(target=self.receive_data).start()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось подключиться к серверу: {e}")
            self.root.quit()
    
    def receive_data(self):
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')
                if not data:
                    break
                
                if data.startswith("SYMBOL"):
                    self.symbol = data.split()[1]
                    self.status_label.config(text=f"Вы играете за {self.symbol}. Ожидание второго игрока...")
                    self.start_button.config(state=tk.NORMAL)
                
                elif data == "SERVER_FULL":
                    messagebox.showinfo("Информация", "Сервер переполнен. Попробуйте позже.")
                    self.root.quit()
                    break
                
                elif data == "GAME_START":
                    self.game_active = True
                    self.status_label.config(text="Игра началась!")
                    self.start_button.config(state=tk.DISABLED)
                    self.quit_button.config(state=tk.NORMAL)
                
                elif data.startswith("TURN"):
                    turn = data.split()[1]
                    self.current_turn = turn
                    if turn == self.symbol:
                        self.status_label.config(text="Ваш ход!")
                        for button in self.buttons:
                            button.config(state=tk.NORMAL)
                    else:
                        self.status_label.config(text=f"Ход противника ({turn})...")
                        for button in self.buttons:
                            button.config(state=tk.DISABLED)
                
                elif data.startswith("BOARD"):
                    board_data = json.loads(data.split()[1])
                    self.board = board_data
                    self.update_board()
                
                elif data.startswith("WINNER"):
                    winner = data.split()[1]
                    self.game_active = False
                    for button in self.buttons:
                        button.config(state=tk.DISABLED)
                    
                    if winner == self.symbol:
                        self.status_label.config(text="Вы победили!")
                    else:
                        self.status_label.config(text="Вы проиграли!")
                    
                    self.restart_button.config(state=tk.NORMAL)
                
                elif data == "DRAW":
                    self.game_active = False
                    self.status_label.config(text="Ничья!")
                    for button in self.buttons:
                        button.config(state=tk.DISABLED)
                    self.restart_button.config(state=tk.NORMAL)
                
                elif data == "GAME_RESTART":
                    self.game_active = True
                    self.board = [' ' for _ in range(9)]
                    self.update_board()
                    self.status_label.config(text="Игра началась заново!")
                    self.restart_button.config(state=tk.DISABLED)
                
                elif data == "OPPONENT_QUIT":
                    self.game_active = False
                    messagebox.showinfo("Информация", "Противник вышел из игры. Вы победили!")
                    self.status_label.config(text="Противник вышел. Вы победили!")
                    for button in self.buttons:
                        button.config(state=tk.DISABLED)
                    self.restart_button.config(state=tk.NORMAL)
                
            except Exception as e:
                print(f"Ошибка: {e}")
                break
    
    def start_game(self):
        self.client.send("START".encode('utf-8'))
    
    def quit_game(self):
        self.client.send("QUIT".encode('utf-8'))
        self.game_active = False
        self.quit_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.DISABLED)
        for button in self.buttons:
            button.config(state=tk.DISABLED)
    
    def request_restart(self):
        self.client.send("RESTART".encode('utf-8'))
        self.restart_button.config(state=tk.DISABLED)
    
    def make_move(self, index):
        if self.board[index] == ' ' and self.current_turn == self.symbol:
            self.client.send(f"MOVE {index}".encode('utf-8'))
            for button in self.buttons:
                button.config(state=tk.DISABLED)
    
    def update_board(self):
        for i in range(9):
            self.buttons[i].config(text=self.board[i])
    
    def run(self):
        self.root.mainloop()
        self.client.close()

if __name__ == "__main__":
    import threading
    client = TicTacToeClient()
    client.run()