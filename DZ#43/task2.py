import threading
import random
import math
import time
import os

class FileNumberProcessor:
    def __init__(self):
        self.file_path = ""
        self.numbers = []
        self.file_ready = threading.Event()
        self.prime_numbers = []
        self.factorials = {}
        self.lock = threading.Lock()
        self.primes_file = "primes.txt"
        self.factorials_file = "factorials.txt"

    def get_file_path(self):
        """Получение пути к файлу от пользователя"""
        while True:
            self.file_path = input("Введите путь к файлу для обработки: ")
            if os.path.isdir(os.path.dirname(self.file_path)) or not os.path.dirname(self.file_path):
                return self.file_path
            print("Ошибка: указан неверный путь к директории. Попробуйте еще раз.")

    def fill_file(self):
        """Заполнение файла случайными числами"""
        print("\nПоток заполнения файла: начал работу")
        self.numbers = [random.randint(1, 20) for _ in range(20)]
        
        with open(self.file_path, 'w') as f:
            f.write('\n'.join(map(str, self.numbers)))
        
        print(f"Поток заполнения файла: файл {self.file_path} заполнен {len(self.numbers)} числами")
        self.file_ready.set()

    def find_primes(self):
        """Поиск простых чисел в файле"""
        print("Поток поиска простых чисел: ожидает заполнения файла...")
        self.file_ready.wait()
        
        with self.lock:
            print("Поток поиска простых чисел: начал обработку файла")
            
            def is_prime(n):
                if n < 2:
                    return False
                for i in range(2, int(math.sqrt(n)) + 1):
                    if n % i == 0:
                        return False
                return True
            
            self.prime_numbers = [n for n in self.numbers if is_prime(n)]
            
            with open(self.primes_file, 'w') as f:
                f.write('\n'.join(map(str, self.prime_numbers)))
            
            print(f"Поток поиска простых чисел: найдено {len(self.prime_numbers)} простых чисел")

    def calculate_factorials(self):
        """Вычисление факториалов чисел из файла"""
        print("Поток вычисления факториалов: ожидает заполнения файла...")
        self.file_ready.wait()
        
        with self.lock:
            print("Поток вычисления факториалов: начал обработку файла")
            
            self.factorials = {n: math.factorial(n) for n in self.numbers}
            
            with open(self.factorials_file, 'w') as f:
                for num, fact in self.factorials.items():
                    f.write(f"{num}! = {fact}\n")
            
            print(f"Поток вычисления факториалов: вычислено {len(self.factorials)} факториалов")

    def run(self):
        # Получаем путь к файлу
        self.get_file_path()
        
        # Создаем потоки
        fill_thread = threading.Thread(target=self.fill_file)
        primes_thread = threading.Thread(target=self.find_primes)
        factorials_thread = threading.Thread(target=self.calculate_factorials)

        # Запускаем потоки
        fill_thread.start()
        primes_thread.start()
        factorials_thread.start()

        # Ожидаем завершения всех потоков
        fill_thread.join()
        primes_thread.join()
        factorials_thread.join()

        # Выводим статистику
        print("\nСтатистика выполнения:")
        print(f"1. Файл '{self.file_path}' содержит {len(self.numbers)} чисел")
        print(f"2. Найдено {len(self.prime_numbers)} простых чисел (сохранено в {self.primes_file})")
        print(f"3. Вычислено {len(self.factorials)} факториалов (сохранено в {self.factorials_file})")
        
        print("\nСодержимое файлов:")
        print(f"\nПростые числа ({self.primes_file}):")
        with open(self.primes_file, 'r') as f:
            print(f.read())
        
        print(f"\nФакториалы ({self.factorials_file}):")
        with open(self.factorials_file, 'r') as f:
            print(f.read())

if __name__ == "__main__":
    print("Программа для обработки чисел в файле")
    processor = FileNumberProcessor()
    processor.run()