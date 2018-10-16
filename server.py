from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        request_path = self.path
        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")

    def do_POST(self):
        request_path = self.path
        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        self.send_response(200)

    do_PUT = do_POST
    do_DELETE = do_GET


def main():
    port = 8080
    print('Сервер запущен на - %s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    parser = OptionParser()
    (options, args) = parser.parse_args()

    main()
