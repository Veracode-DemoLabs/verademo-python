from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = "127.0.0.1"
PORT = 3306

class NeuralHTTP(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(bytes("Hello World","utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content_type", "application/json")
        self.end_headers()


server = HTTPServer((HOST, PORT), NeuralHTTP)
print("Server running on port ", PORT)
server.serve_forever()
server.server_close()