import os
import shutil
import threading

class DirectoryCopier:
    def __init__(self):
        self.source_dir = ""
        self.target_dir = ""
        self.total_files = 0
        self.copied_files = 0
        self.total_size = 0
        self.lock = threading.Lock()

    def get_directory_paths(self):
        """Получение путей к директориям от пользователя"""
        while True:
            self.source_dir = input("Введите путь к исходной директории: ")
            if os.path.isdir(self.source_dir):
                break
            print("Ошибка: указанная директория не существует. Попробуйте еще раз.")

        while True:
            self.target_dir = input("Введите путь к целевой директории: ")
            if not os.path.exists(self.target_dir):
                os.makedirs(self.target_dir, exist_ok=True)
                break
            print("Ошибка: целевая директория уже существует. Укажите другой путь.")

    def count_files_and_size(self):
        """Подсчет общего количества файлов и их размера"""
        for root, dirs, files in os.walk(self.source_dir):
            self.total_files += len(files)
            for file in files:
                file_path = os.path.join(root, file)
                self.total_size += os.path.getsize(file_path)

    def copy_directory(self):
        """Копирование директории с сохранением структуры"""
        print(f"\nНачато копирование из '{self.source_dir}' в '{self.target_dir}'")
        
        try:
            # Создаем структуру директорий
            for root, dirs, files in os.walk(self.source_dir):
                # Создаем соответствующие директории в целевой папке
                relative_path = os.path.relpath(root, self.source_dir)
                target_path = os.path.join(self.target_dir, relative_path)
                
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                
                # Копируем файлы
                for file in files:
                    source_file = os.path.join(root, file)
                    dest_file = os.path.join(target_path, file)
                    
                    shutil.copy2(source_file, dest_file)
                    
                    with self.lock:
                        self.copied_files += 1
                        file_size = os.path.getsize(source_file)
                        print(f"Скопирован файл {self.copied_files}/{self.total_files}: {source_file} -> {dest_file} ({file_size} байт)")
            
            print("\nКопирование завершено успешно!")
        
        except Exception as e:
            print(f"\nОшибка при копировании: {e}")

    def run(self):
        # Получаем пути к директориям
        self.get_directory_paths()
        
        # Подсчитываем общее количество файлов и их размер
        self.count_files_and_size()
        
        print(f"\nНайдено файлов: {self.total_files}")
        print(f"Общий размер: {self.total_size} байт")
        
        # Создаем и запускаем поток копирования
        copy_thread = threading.Thread(target=self.copy_directory)
        copy_thread.start()
        
        # Ожидаем завершения потока
        copy_thread.join()
        
        # Выводим статистику
        print("\nСтатистика выполнения:")
        print(f"Исходная директория: {self.source_dir}")
        print(f"Целевая директория: {self.target_dir}")
        print(f"Всего файлов: {self.total_files}")
        print(f"Скопировано файлов: {self.copied_files}")
        print(f"Общий объем скопированных данных: {self.total_size} байт")
        
        if self.total_files > 0:
            print(f"Процент выполнения: {100 * self.copied_files / self.total_files:.2f}%")

if __name__ == "__main__":
    print("Программа для копирования директории с сохранением структуры")
    copier = DirectoryCopier()
    copier.run()