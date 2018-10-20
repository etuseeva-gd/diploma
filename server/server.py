from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

import predict
import train
import config

def handlePredict(body):
    print('predict')

    # Нужно подумать что передать 
    predict.init()

def handleTrain(body):
    print('train')

    # Нужно подумать что передать 
    train.init()

def handleSaveSettings(body):
    print('save settings')


def handlePost(self):
    path = self.path

    # Переданные параметры 
    content_len = int(self.headers.getheader('content-length'))
    post_body = self.rfile.read(content_len)
    body = json.loads(post_body)

    if path == '/save_settings':
        handleSaveSettings(body)
    elif path == '/train':
        handleTrain(body)
    elif path == '/predict':
        handlePredict(body)
    return {}


def handleGet():
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
