from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

# import predict
# import train

from constants import nn_params_path, base_params_path, train_params_path
# from myutils import read_json


class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def handlePOSTPredict(self, body):
        # Обрабатываем запрос на обучение некоторого изображения
        print('handlePOSTPredict')
        # predict.web_prediction('some_url')

    def handlePOSTTrain(self, body):
        # Обрабатываем запрос на обучение некоторого изображения
        # Подумать над web_train
        # Сохраняем праметры тренировки и нейронной сети

        # @todo change to write file
        with open(train_params_path, 'w') as outfile:
            json.dump(body['train_params'], outfile)

        with open(nn_params_path, 'w') as outfile:
            json.dump(body['nn_params'], outfile)
        # end todo

        # train.console_train()

    def handlePOSTSaveBaseParams(self, body):
        # Обрабатывает запрос на сохранение базовых настроек
        print('save settings')

    def handleGetParams(self, path):
        # @todo chage on read_json
        file = open(path)
        data = json.load(file)
        file.close()
        # end toto

        self.wfile.write(json.dumps(data).encode())
        return

    def handleGetTrainStatus(self):
        print('get train status')

    def do_GET(self):
        self.do_OPTIONS()

        path = self.path
        if path == '/get_base_params':
            self.handleGetParams(base_params_path)
        elif path == '/get_nn_params':
            self.handleGetParams(nn_params_path)
        elif path == '/get_train_params':
            self.handleGetParams(train_params_path)
        elif path == '/get_train_status':
            self.handleGetTrainStatus()

    def do_POST(self):
        self.do_OPTIONS()

        path = self.path
        # Переданные параметры
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len)
        body = json.loads(post_body)

        if path == '/save_base_params':
            self.handlePOSTSaveBaseParams(body)
        elif path == '/train':            
            self.handlePOSTTrain(body)
        elif path == '/predict':
            self.handlePOSTPredict(body)


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print('Сервер запущен на - http://localhost:8000')
    server.serve_forever()
