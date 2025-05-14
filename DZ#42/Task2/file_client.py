import socket
import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class FileTransferClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id = None
        self.current_transfer = None
        
        # GUI
        self.root = tk.Tk()
        self.root.title("Файловый клиент")
        
        # Информация о подключении
        self.info_label = tk.Label(self.root, text="Не подключено", font=('Arial', 10))
        self.info_label.pack(pady=5)
        
        # Список клиентов
        self.clients_list = scrolledtext.ScrolledText(self.root, height=10, width=40, state='disabled')
        self.clients_list.pack(pady=5)
        
        # Кнопка обновления списка
        self.refresh_button = tk.Button(self.root, text="Обновить список", command=self.request_clients_list)
        self.refresh_button.pack(pady=5)
        
        # Поле для ввода ID клиента
        self.target_frame = tk.Frame(self.root)
        self.target_frame.pack(pady=5)
        tk.Label(self.target_frame, text="ID клиента:").pack(side=tk.LEFT)
        self.target_id_entry = tk.Entry(self.target_frame, width=5)
        self.target_id_entry.pack(side=tk.LEFT, padx=5)
        
        # Кнопки управления
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)
        
        self.send_button = tk.Button(self.button_frame, text="Отправить файл", command=self.select_file)
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        # Статус передачи
        self.status_label = tk.Label(self.root, text="", font=('Arial', 10))
        self.status_label.pack(pady=5)
        
        # Подключаемся к серверу
        self.connect_to_server()
        
        # Запускаем поток для получения данных
        self.receive_thread = threading.Thread(target=self.receive_data, daemon=True)
        self.receive_thread.start()
        
        # Обработчик закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def connect_to_server(self):
        try:
            self.client.connect((self.host, self.port))
            self.info_label.config(text=f"Подключено к {self.host}:{self.port}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось подключиться к серверу: {e}")
            self.root.quit()
    
    def receive_data(self):
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')
                if not data:
                    break
                
                if data.startswith("YOUR_ID"):
                    self.client_id = int(data.split()[1])
                    self.info_label.config(text=f"ID: {self.client_id} | Подключено к {self.host}:{self.port}")
                
                elif data.startswith("CLIENTS_LIST"):
                    clients = data.split('\n')[1:]
                    self.clients_list.config(state='normal')
                    self.clients_list.delete(1.0, tk.END)
                    self.clients_list.insert(tk.END, "Доступные клиенты:\n")
                    for client in clients:
                        self.clients_list.insert(tk.END, client + "\n")
                    self.clients_list.config(state='disabled')
                
                elif data.startswith("INCOMING_FILE"):
                    _, filename, filesize, sender_id = data.split()
                    self.current_transfer = {
                        'filename': filename,
                        'filesize': int(filesize),
                        'sender_id': int(sender_id)
                    }
                    response = messagebox.askyesno(
                        "Входящий файл",
                        f"Клиент {sender_id} хочет отправить вам файл {filename} ({filesize} байт). Принять?"
                    )
                    if response:
                        self.client.send(f"ACCEPT_FILE {sender_id}".encode('utf-8'))
                        self.receive_file()
                    else:
                        self.client.send(f"REJECT_FILE {sender_id}".encode('utf-8'))
                
                elif data == "TRANSFER_APPROVED":
                    self.status_label.config(text="Получатель подтвердил передачу. Начинаем отправку...")
                    self.send_file()
                
                elif data == "TRANSFER_REJECTED":
                    self.status_label.config(text="Получатель отклонил передачу файла.")
                    messagebox.showinfo("Информация", "Получатель отклонил передачу файла.")
                
                elif data.startswith("FILE_INFO"):
                    _, filename, filesize, filehash = data.split()
                    self.current_transfer.update({
                        'filename': filename,
                        'filesize': int(filesize),
                        'filehash': filehash
                    })
                
                elif data == "TRANSFER_COMPLETE":
                    self.status_label.config(text="Передача файла завершена успешно!")
                    messagebox.showinfo("Успех", "Файл успешно передан!")
                
                elif data == "TRANSFER_ERROR":
                    self.status_label.config(text="Ошибка при передаче файла!")
                    messagebox.showerror("Ошибка", "Произошла ошибка при передаче файла!")
                
            except Exception as e:
                print(f"Ошибка при получении данных: {e}")
                break
    
    def request_clients_list(self):
        self.client.send("LIST_CLIENTS".encode('utf-8'))
    
    def select_file(self):
        target_id = self.target_id_entry.get()
        if not target_id.isdigit():
            messagebox.showerror("Ошибка", "Введите корректный ID клиента")
            return
        
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        
        # Вычисляем хеш файла
        filehash = self.calculate_file_hash(filepath)
        
        self.current_transfer = {
            'filepath': filepath,
            'filename': filename,
            'filesize': filesize,
            'filehash': filehash,
            'target_id': int(target_id)
        }
        
        self.client.send(f"REQUEST_SEND {filename} {filesize} {target_id}".encode('utf-8'))
        self.status_label.config(text=f"Запрос на отправку {filename} клиенту {target_id}...")
    
    def calculate_file_hash(self, filepath):
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def send_file(self):
        if not self.current_transfer:
            return
        
        try:
            filepath = self.current_transfer['filepath']
            filename = self.current_transfer['filename']
            filesize = self.current_transfer['filesize']
            filehash = self.current_transfer['filehash']
            
            # Отправляем метаданные
            self.client.send(f"{filename} {filesize} {filehash}".encode('utf-8'))
            
            # Отправляем файл
            bytes_sent = 0
            with open(filepath, 'rb') as f:
                while bytes_sent < filesize:
                    chunk = f.read(4096)
                    self.client.sendall(chunk)
                    bytes_sent += len(chunk)
                    progress = int(bytes_sent / filesize * 100)
                    self.status_label.config(text=f"Отправка: {progress}%")
            
            self.status_label.config(text="Файл успешно отправлен!")
        
        except Exception as e:
            self.status_label.config(text=f"Ошибка при отправке: {e}")
            messagebox.showerror("Ошибка", f"Не удалось отправить файл: {e}")
    
    def receive_file(self):
        if not self.current_transfer:
            return
        
        try:
            filename = self.current_transfer['filename']
            filesize = self.current_transfer['filesize']
            filehash = self.current_transfer['filehash']
            
            save_path = filedialog.asksaveasfilename(
                initialfile=filename,
                title="Сохранить файл как"
            )
            
            if not save_path:
                self.client.send("TRANSFER_CANCELED".encode('utf-8'))
                return
            
            bytes_received = 0
            hash_md5 = hashlib.md5()
            
            with open(save_path, 'wb') as f:
                while bytes_received < filesize:
                    chunk = self.client.recv(4096)
                    if not chunk:
                        break
                    f.write(chunk)
                    hash_md5.update(chunk)
                    bytes_received += len(chunk)
                    progress = int(bytes_received / filesize * 100)
                    self.status_label.config(text=f"Получение: {progress}%")
            
            # Проверяем хеш
            if hash_md5.hexdigest() == filehash:
                self.status_label.config(text="Файл успешно получен и проверен!")
                messagebox.showinfo("Успех", f"Файл {filename} успешно получен!")
            else:
                self.status_label.config(text="Ошибка: файл поврежден при передаче!")
                messagebox.showerror("Ошибка", "Полученный файл не соответствует оригиналу!")
                os.remove(save_path)
        
        except Exception as e:
            self.status_label.config(text=f"Ошибка при получении: {e}")
            messagebox.showerror("Ошибка", f"Не удалось получить файл: {e}")
    
    def on_closing(self):
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.client.close()
            self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    import threading
    client = FileTransferClient()
    client.run()