from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

# Лайфхак с импортом модулей
import sys
import os
sys.path.append(os.path.abspath('../recognizer'))

import predict
import train

from utility.jsonfile import read_json, write_json
from utility.file import read
from utility.constants import nn_params_path, base_params_path, train_params_path, report_path, end_flag

# recognizer_path = '../recognizer/'
recognizer_path = ''

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
        # Обрабатываем запрос на обучение
        # Сохраняем праметры тренировки и нейронной сети
        write_json(recognizer_path + train_params_path, body['train_params'])
        write_json(recognizer_path + nn_params_path, body['nn_params'])

        train.console_train() #!!!исправить!!! работа остановится из-за этого

    def handlePOSTSaveBaseParams(self, body):
        # Обрабатывает запрос на сохранение базовых настроек
        write_json(recognizer_path + base_params_path, body)

    def handleGetParams(self, path):
        data = read_json(path)
        self.wfile.write(json.dumps(data).encode())
        return

    def handleGetReport(self):
        is_train_ended = False
        report = []
        lines = read(recognizer_path + report_path)
        for line in lines:
            if line == end_flag:
                is_train_ended = True
                break

            p = line.split()
            report.append({
                'epoch': p[0],
                'train_accuracy': p[1],
                'test_accuracy': p[2],
                'test_loss': p[3]
            })

        self.wfile.write(json.dumps({
            'is_train_ended': is_train_ended,
            'statistics': report
        }).encode())

    def do_GET(self):
        self.do_OPTIONS()

        path = self.path
        if path == '/get_base_params':
            self.handleGetParams(recognizer_path + base_params_path)
        elif path == '/get_nn_params':
            self.handleGetParams(recognizer_path + nn_params_path)
        elif path == '/get_train_params':
            self.handleGetParams(recognizer_path + train_params_path)
        elif path == '/get_report':
            self.handleGetReport()

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
