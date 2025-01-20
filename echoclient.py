class EchoClient:
    def __init__(self, host='localhost', port=9090):
        """
        Инициализация клиента
        host - адрес сервера
        port - порт сервера
        """
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Подключение к серверу"""
        self.client_socket.connect((self.host, self.port))
        print(f"Подключено к {self.host}:{self.port}")

    def send_message(self, message):
        """
        Отправка сообщения серверу и получение ответа
        message - текст сообщения
        """
        self.client_socket.send(message.encode())
        response = self.client_socket.recv(1024)
        return response.decode()

    def close(self):
        """Закрытие соединения"""
        self.client_socket.close()

if __name__ == "__main__":
    # Запуск в режиме сервера
    server = EchoServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.close()
