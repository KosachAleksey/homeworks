import os
import threading
import time

class ContentProcessor:
    def __init__(self):
        self.search_dir = ""
        self.search_word = ""
        self.banned_words = []
        self.output_file = "combined_content.txt"
        self.filtered_file = "filtered_content.txt"
        self.found_files = []
        self.combined_size = 0
        self.removed_words_count = 0
        self.lock = threading.Lock()
        self.combine_done = threading.Event()

    def get_user_input(self):
        """Получение входных данных от пользователя"""
        while True:
            self.search_dir = input("Введите путь к директории для поиска: ")
            if os.path.isdir(self.search_dir):
                break
            print("Ошибка: указанная директория не существует. Попробуйте еще раз.")

        self.search_word = input("Введите слово для поиска: ").lower()
        
        # Загрузка запрещенных слов из файла
        banned_words_file = "banned_words.txt"
        if os.path.exists(banned_words_file):
            with open(banned_words_file, 'r', encoding='utf-8') as f:
                self.banned_words = [word.strip().lower() for word in f.readlines()]
        else:
            print(f"Файл с запрещенными словами '{banned_words_file}' не найден. Будет создан пустой список.")
            self.banned_words = []

    def find_and_combine_files(self):
        """Поиск файлов и объединение содержимого"""
        print("\nПоток поиска: начал работу")
        
        try:
            # Поиск файлов, содержащих искомое слово
            for root, _, files in os.walk(self.search_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read().lower()
                            if self.search_word in content:
                                self.found_files.append(file_path)
                    except (UnicodeDecodeError, PermissionError):
                        continue
            
            print(f"Найдено {len(self.found_files)} файлов, содержащих слово '{self.search_word}'")
            
            # Объединение содержимого найденных файлов
            with open(self.output_file, 'w', encoding='utf-8') as out_file:
                for file_path in self.found_files:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as in_file:
                            content = in_file.read()
                            out_file.write(f"\n\n--- Файл: {file_path} ---\n\n")
                            out_file.write(content)
                            self.combined_size += len(content)
                    except (UnicodeDecodeError, PermissionError):
                        continue
            
            print(f"Содержимое объединено в файл '{self.output_file}'")
            self.combine_done.set()  # Сигнализируем о завершении
        
        except Exception as e:
            print(f"Ошибка в потоке поиска: {e}")

    def filter_banned_words(self):
        """Фильтрация запрещенных слов из объединенного файла"""
        print("Поток фильтрации: ожидает завершения поиска...")
        self.combine_done.wait()  # Ожидаем завершения первого потока
        
        if not os.path.exists(self.output_file):
            print("Нет файла для фильтрации")
            return
        
        print("Поток фильтрации: начал работу")
        
        try:
            # Чтение объединенного файла
            with open(self.output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Замена запрещенных слов
            original_content = content
            for word in self.banned_words:
                content = content.replace(word, '[цензура]')
                content = content.replace(word.capitalize(), '[Цензура]')
            
            # Подсчет количества замен
            self.removed_words_count = sum(
                original_content.lower().count(word.lower()) 
                for word in self.banned_words
            )
            
            # Сохранение отфильтрованного файла
            with open(self.filtered_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Отфильтрованное содержимое сохранено в '{self.filtered_file}'")
        
        except Exception as e:
            print(f"Ошибка в потоке фильтрации: {e}")

    def run(self):
        # Получаем входные данные
        self.get_user_input()
        
        # Создаем и запускаем потоки
        search_thread = threading.Thread(target=self.find_and_combine_files)
        filter_thread = threading.Thread(target=self.filter_banned_words)
        
        start_time = time.time()
        search_thread.start()
        filter_thread.start()
        
        # Ожидаем завершения потоков
        search_thread.join()
        filter_thread.join()
        end_time = time.time()
        
        # Выводим статистику
        print("\nСтатистика выполнения:")
        print(f"Директория для поиска: {self.search_dir}")
        print(f"Искомое слово: '{self.search_word}'")
        print(f"Найдено файлов: {len(self.found_files)}")
        print(f"Размер объединенного файла: {self.combined_size} байт")
        print(f"Количество запрещенных слов: {len(self.banned_words)}")
        print(f"Удалено запрещенных слов: {self.removed_words_count}")
        print(f"Время выполнения: {end_time - start_time:.2f} секунд")
        
        # Показываем список найденных файлов
        if self.found_files:
            print("\nНайденные файлы:")
            for file in self.found_files:
                print(f"- {file}")

if __name__ == "__main__":
    print("Программа для поиска файлов и фильтрации содержимого")
    processor = ContentProcessor()
    processor.run()
    