from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

import predict
import train
import config


def handlePOSTPredict(body):
    # Обрабатываем запрос на обучение некоторого изображения
    predict.web_prediction('some_url')


def handlePOSTTrain(body):
    # Обрабатываем запрос на обучение некоторого изображения    
    # Подумать над web_train
    train.console_train()


def handlePOSTSaveBaseSettings(body):
    # Обрабатывает запрос на сохранение базовых настроек
    print('save settings')


def handlePOSTSaveNNSettings(body):
    # Обрабатывает запрос на сохранение настроек нейронной сети
    print('save nn settings')


def handleGETBaseSettings():
    print('get base settings')


def handleGetNNSettings():
    print('get nn settings')


def handleGetTrainStatus():
    print('get train status')


def handlePost(self):
    path = self.path

    # Переданные параметры
    content_len = int(self.headers.getheader('content-length'))
    post_body = self.rfile.read(content_len)
    body = json.loads(post_body)

    if path == '/save_base_settings':
        handlePOSTSaveBaseSettings(body)
    elif path == '/save_nn_settings':
        handlePOSTSaveNNSettings(body)
    elif path == '/train':
        handlePOSTTrain(body)
    elif path == '/predict':
        handlePOSTPredict(body)
    return {}


def handleGet(self):
     path = self.path
    if path == '/get_base_settings':
        handleGETBaseSettings()
    elif path == '/get_nn_settings':
        handleGetNNSettings()
    elif path == '/get_train_status':
        handleGetTrainStatus()
    return {}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        handlePost(self)

        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version
        }).encode())

        return

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)

        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version,
            'body': data
        }).encode())
        return


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print('Сервер запущен на - http://localhost:8000')
    server.serve_forever()
