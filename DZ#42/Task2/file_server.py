import socket
import threading
import os
import hashlib

class FileTransferServer:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = {}
        print(f"Сервер запущен на {host}:{port}")

    def handle_client(self, conn, addr):
        print(f"Новое подключение: {addr}")
        client_id = len(self.clients)
        self.clients[conn] = {'id': client_id, 'addr': addr}
        
        try:
            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break

                if data.startswith("REQUEST_SEND"):
                    _, filename, filesize, target_client_id = data.split()
                    target_conn = self.find_client_by_id(int(target_client_id))
                    if target_conn:
                        target_conn.send(f"INCOMING_FILE {filename} {filesize} {client_id}".encode('utf-8'))
                    else:
                        conn.send("CLIENT_NOT_FOUND".encode('utf-8'))

                elif data.startswith("ACCEPT_FILE"):
                    _, sender_id = data.split()
                    sender_conn = self.find_client_by_id(int(sender_id))
                    if sender_conn:
                        sender_conn.send("TRANSFER_APPROVED".encode('utf-8'))
                        self.start_file_transfer(sender_conn, conn)
                    else:
                        conn.send("SENDER_NOT_FOUND".encode('utf-8'))

                elif data == "REJECT_FILE":
                    _, sender_id = data.split()
                    sender_conn = self.find_client_by_id(int(sender_id))
                    if sender_conn:
                        sender_conn.send("TRANSFER_REJECTED".encode('utf-8'))

                elif data == "LIST_CLIENTS":
                    clients_list = "\n".join([f"{info['id']}: {info['addr']}" for info in self.clients.values()])
                    conn.send(f"CLIENTS_LIST\n{clients_list}".encode('utf-8'))

        except Exception as e:
            print(f"Ошибка с клиентом {addr}: {e}")
        finally:
            print(f"Клиент {addr} отключен")
            del self.clients[conn]
            conn.close()

    def find_client_by_id(self, client_id):
        for conn, info in self.clients.items():
            if info['id'] == client_id:
                return conn
        return None

    def start_file_transfer(self, sender_conn, receiver_conn):
        try:
            # Получаем метаданные файла
            file_info = sender_conn.recv(1024).decode('utf-8')
            filename, filesize, filehash = file_info.split()
            filesize = int(filesize)

            receiver_conn.send(f"FILE_INFO {filename} {filesize} {filehash}".encode('utf-8'))

            # Передача файла
            bytes_received = 0
            while bytes_received < filesize:
                data = sender_conn.recv(4096)
                if not data:
                    break
                receiver_conn.sendall(data)
                bytes_received += len(data)

            print(f"Файл {filename} успешно передан ({bytes_received} байт)")

        except Exception as e:
            print(f"Ошибка при передаче файла: {e}")
            sender_conn.send("TRANSFER_ERROR".encode('utf-8'))
            receiver_conn.send("TRANSFER_ERROR".encode('utf-8'))

    def start(self):
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    server = FileTransferServer()
    server.start()