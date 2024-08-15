from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import NBow
from urllib.parse import parse_qs

HOST = "127.0.0.1"
PORT = 3306

class NeuralHTTP(BaseHTTPRequestHandler):

    model = NBow.create_model()

    def do_GET(self):
        print("Get Recognized")
        try:
            content_len = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_len).decode('utf8')
            parsed_text = parse_qs(body)['Text'][0]
            print("received data: ", parsed_text)
            response = self.model.predict_sentiment(parsed_text)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            responseStr = json.dumps({'Result':response[0],'Certainty':response[1]})
            self.wfile.write(bytes(responseStr,"utf-8"))
        except Exception as e:
            print(e)
            self.send_response(400)

    def do_POST(self):
        print("Post recognized")
        try:
            content_len = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_len).decode('utf8')
            parsed_text = parse_qs(body)['Text'][0]
            print("received data: ", parsed_text)
            response = self.model.predict_sentiment(parsed_text)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            responseStr = json.dumps({'Result':response[0],'Certainty':response[1]})
            self.wfile.write(bytes(responseStr,"utf-8"))
        except Exception as e:
            print(e)
            self.send_response(400)
            
        

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), NeuralHTTP)
    print("Server running on port ", PORT)
    server.serve_forever()
    server.server_close()

