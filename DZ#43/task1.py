import threading
import random
import time

class NumberProcessor:
    def __init__(self, list_size=10):
        self.numbers = []
        self.list_size = list_size
        self.list_ready = threading.Event()
        self.sum_result = None
        self.avg_result = None
        self.lock = threading.Lock()

    def fill_list(self):
        """Поток заполняет список случайными числами"""
        print("Поток заполнения списка: начал работу")
        self.numbers = [random.randint(1, 100) for _ in range(self.list_size)]
        print(f"Поток заполнения списка: список заполнен - {self.numbers}")
        self.list_ready.set()  # Сигнализируем, что список готов

    def calculate_sum(self):
        """Поток вычисляет сумму элементов списка"""
        print("Поток суммы: ожидает заполнения списка...")
        self.list_ready.wait()  # Ожидаем сигнала о готовности списка
        
        with self.lock:
            print("Поток суммы: начал вычисления")
            self.sum_result = sum(self.numbers)
            print(f"Поток суммы: вычисления завершены, сумма = {self.sum_result}")

    def calculate_average(self):
        """Поток вычисляет среднее арифметическое списка"""
        print("Поток среднего: ожидает заполнения списка...")
        self.list_ready.wait()  # Ожидаем сигнала о готовности списка
        
        with self.lock:
            print("Поток среднего: начал вычисления")
            self.avg_result = sum(self.numbers) / len(self.numbers)
            print(f"Поток среднего: вычисления завершены, среднее = {self.avg_result:.2f}")

    def run(self):
        # Создаем потоки
        fill_thread = threading.Thread(target=self.fill_list)
        sum_thread = threading.Thread(target=self.calculate_sum)
        avg_thread = threading.Thread(target=self.calculate_average)

        # Запускаем потоки
        fill_thread.start()
        sum_thread.start()
        avg_thread.start()

        # Ожидаем завершения всех потоков
        fill_thread.join()
        sum_thread.join()
        avg_thread.join()

        # Выводим результаты
        print("\nРезультаты:")
        print(f"Список чисел: {self.numbers}")
        print(f"Сумма элементов: {self.sum_result}")
        print(f"Среднее арифметическое: {self.avg_result:.2f}")

if __name__ == "__main__":
    print("Программа запущена")
    processor = NumberProcessor(list_size=10)
    processor.run()
    print("Программа завершена")