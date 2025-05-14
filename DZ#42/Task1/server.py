import socket
import threading
import json

class TicTacToeServer:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        self.players = []
        self.current_player = 0
        self.board = [' ' for _ in range(9)]
        self.game_active = False
        self.waiting_for_restart = False
        print(f"Сервер запущен на {host}:{port}")

    def broadcast(self, message):
        for player in self.players:
            try:
                player.send(message.encode('utf-8'))
            except:
                self.players.remove(player)

    def handle_client(self, conn, addr, player_id):
        print(f"Игрок {player_id} подключен: {addr}")
        
        # Отправляем игроку его символ (X или O)
        symbol = 'X' if player_id == 0 else 'O'
        conn.send(f"SYMBOL {symbol}".encode('utf-8'))
        
        while True:
            try:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                
                print(f"Получено от игрока {player_id}: {data}")
                
                if data == "START":
                    if len(self.players) == 2 and not self.game_active:
                        self.game_active = True
                        self.broadcast("GAME_START")
                        self.broadcast(f"TURN X")  # X всегда ходит первым
                
                elif data == "QUIT":
                    opponent_id = 1 if player_id == 0 else 0
                    if len(self.players) > opponent_id:
                        self.players[opponent_id].send("OPPONENT_QUIT".encode('utf-8'))
                    self.game_active = False
                    self.waiting_for_restart = False
                    self.board = [' ' for _ in range(9)]
                    break
                
                elif data.startswith("MOVE"):
                    _, move = data.split()
                    move = int(move)
                    
                    if self.game_active and player_id == self.current_player:
                        if self.board[move] == ' ':
                            self.board[move] = symbol
                            self.broadcast(f"BOARD {json.dumps(self.board)}")
                            
                            if self.check_winner():
                                self.broadcast(f"WINNER {symbol}")
                                self.game_active = False
                                self.waiting_for_restart = True
                            elif ' ' not in self.board:
                                self.broadcast("DRAW")
                                self.game_active = False
                                self.waiting_for_restart = True
                            else:
                                self.current_player = 1 - self.current_player
                                next_symbol = 'X' if self.current_player == 0 else 'O'
                                self.broadcast(f"TURN {next_symbol}")
                
                elif data == "RESTART":
                    if self.waiting_for_restart:
                        self.board = [' ' for _ in range(9)]
                        self.current_player = 0
                        self.game_active = True
                        self.waiting_for_restart = False
                        self.broadcast("GAME_RESTART")
                        self.broadcast(f"TURN X")
                        self.broadcast(f"BOARD {json.dumps(self.board)}")
                
            except Exception as e:
                print(f"Ошибка с игроком {player_id}: {e}")
                break
        
        print(f"Игрок {player_id} отключен")
        if conn in self.players:
            self.players.remove(conn)
        if len(self.players) == 0:
            self.game_active = False
            self.waiting_for_restart = False
            self.board = [' ' for _ in range(9)]
            self.current_player = 0
        conn.close()

    def check_winner(self):
        # Проверка строк
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != ' ':
                return True
        
        # Проверка столбцов
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != ' ':
                return True
        
        # Проверка диагоналей
        if self.board[0] == self.board[4] == self.board[8] != ' ':
            return True
        if self.board[2] == self.board[4] == self.board[6] != ' ':
            return True
        
        return False

    def start(self):
        while True:
            conn, addr = self.server.accept()
            if len(self.players) < 2:
                player_id = len(self.players)
                self.players.append(conn)
                threading.Thread(target=self.handle_client, args=(conn, addr, player_id)).start()
            else:
                conn.send("SERVER_FULL".encode('utf-8'))
                conn.close()

if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()