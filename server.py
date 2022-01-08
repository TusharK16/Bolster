import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import traceback
import launch


class ThreadedHTTPServer(HTTPServer):
    def process_request(self, request, client_address):
        thread = Thread(target=self.__new_request, args=(self.RequestHandlerClass, request, client_address, self))
        thread.start()
    def __new_request(self, handlerClass, request, address, server):
        handlerClass(request, address, server)
        self.shutdown_request(request)


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/favicon.ico':
            return
        self._set_headers()
        self.wfile.write("hello")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        request_headers = self.headers
        self._set_headers()
        if self.headers['Content-Type'] == 'application/json':
            content_length = request_headers.get('content-length')
            length = int(content_length) if content_length else 0
            data_str = self.rfile.read(length)
            data = json.loads(data_str)
            resp_json = None
            resp_json = launch.call_me(data)
            resp_json_str = json.dumps(resp_json)
            return self.wfile.write(resp_json_str.encode())
        else:
            return self.wfile.write("Unsupported Media Type".encode())

def run(server_class=ThreadedHTTPServer, handler_class=S, port=32002):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
