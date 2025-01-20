import socket
import threading

class EchoServer:
    def __init__(self, host='localhost', port=9090):
        """
        Инициализация сервера
        host - адрес сервера (по умолчанию localhost)
        port - порт сервера (по умолчанию 9090)
        """
        self.host = host
        self.port = port
        # Создаем TCP сокет
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Привязываем сокет к адресу и порту
        self.server_socket.bind((self.host, self.port))
        # Начинаем прослушивание (очередь на 5 подключений)
        self.server_socket.listen(5)
        print(f"Сервер запущен на {self.host}:{self.port}")

    def handle_client(self, client_socket, addr):
        """
        Обработка подключения клиента в отдельном потоке
        client_socket - сокет клиента
        addr - адрес клиента
        """
        print(f"Новое подключение от {addr}")
        while True:
            try:
                # Получаем данные от клиента
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Получено от {addr}: {data.decode()}")
                # Отправляем данные обратно клиенту (эхо)
                client_socket.send(data)
            except:
                break
        print(f"Соединение с {addr} закрыто")
        client_socket.close()

    def start(self):
        """Запуск сервера и прием подключений"""
        while True:
            # Принимаем новое подключение
            client_socket, addr = self.server_socket.accept()
            # Создаем новый поток для обработки клиента
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, addr)
            )
            client_thread.start()

    def close(self):
        """Закрытие сервера"""
        self.server_socket.close()
