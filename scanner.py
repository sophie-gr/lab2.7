import socket
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import tqdm
import sys

class PortScanner:
    def __init__(self, host, start_port=1, end_port=1024, num_threads=100):
        """
        Инициализация сканера портов
        host - адрес для сканирования
        start_port - начальный порт
        end_port - конечный порт
        num_threads - количество потоков для сканирования
        """
        self.host = host
        self.start_port = start_port
        self.end_port = end_port
        self.num_threads = num_threads
        self.queue = Queue()
        self.results = []
        self.lock = threading.Lock()

    def scan_port(self, port):
        """
        Проверка одного порта
        port - номер порта для проверки
        """
        try:
            # Создаем сокет для проверки порта
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)  # Таймаут в 1 секунду
                result = sock.connect_ex((self.host, port))
                if result == 0:  # Если порт открыт
                    with self.lock:
                        self.results.append(port)
                    return True
        except:
            pass
        return False

    def scan(self):
        """
        Запуск сканирования всех портов в указанном диапазоне
        """
        total_ports = self.end_port - self.start_port + 1
        open_ports = []

        # Используем пул потоков для параллельного сканирования
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            # Создаем прогресс-бар
            with tqdm.tqdm(total=total_ports, desc="Сканирование портов", unit="порт") as pbar:
                # Создаем список задач для выполнения
                futures = [
                    executor.submit(self.scan_port, port)
                    for port in range(self.start_port, self.end_port + 1)
                ]
                
                # Обрабатываем результаты по мере их появления
                for future in futures:
                    future.result()
                    pbar.update(1)

        # Сортируем результаты
        self.results.sort()
        return self.results

def main():
    # Получаем адрес хоста от пользователя
    host = input("Введите хост для сканирования (IP или имя хоста): ").strip()
    
    try:
        # Пробуем преобразовать имя хоста в IP-адрес
        ip = socket.gethostbyname(host)
        print(f"Сканирование хоста: {host} ({ip})")
    except socket.gaierror:
        print("Ошибка: Неверное имя хоста или IP-адрес")
        sys.exit(1)

    # Создаем и запускаем сканер
    scanner = PortScanner(ip)
    open_ports = scanner.scan()

    # Выводим результаты
    if open_ports:
        print("\nОткрытые порты:")
        for port in open_ports:
            print(f"Порт {port} открыт")
    else:
        print("\nОткрытых портов не найдено")

if __name__ == "__main__":
    main()
