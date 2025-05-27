from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети
BASE_DIR = Path(__file__).resolve().parent.parent
HTML_DIR = BASE_DIR / "html"
contact_file_path = HTML_DIR / "contacts.html"


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """Метод для обработки входящих GET-запросов"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(contact_file_path, "r", encoding="utf-8") as file_html:
            data = file_html.read()
        self.wfile.write(bytes(data, "utf-8"))

    def do_OPTIONS(self):
        """Обработка метода OPTIONS"""
        self.send_response(200)  # Статус OK
        self.send_header('Access-Control-Allow-Origin', '*')  # Разрешение на CORS
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')  # Разрешенные методы
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # Разрешенные заголовки
        self.end_headers()

    def do_POST(self):
        """Метод для обработки входящих POST-запросов"""
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(body)
        self.send_response(200)
        self.end_headers()



if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")


