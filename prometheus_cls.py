# coding: utf-8
from prometheus_client import start_http_server
from prometheus_client import Counter
from threading import Thread
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

#需要统计的lable
c = Counter('my_failures_total', 'Description of counter')

#正常的业务逻辑
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        #累加计数
        c.inc()
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("Hello World!")

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass 

def serve_on_port(port):
    server = ThreadingHTTPServer(("localhost",port), Handler)
    server.serve_forever()

#启动一个现场用来做业务端口
Thread(target=serve_on_port, args=[8001]).start()

#启动监控端口
start_http_server(10092)
