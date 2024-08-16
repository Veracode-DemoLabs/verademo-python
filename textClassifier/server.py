from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
import NBow
from urllib.parse import parse_qs, urlparse

HOST = "127.0.0.1"
PORT = 3306

class NeuralHTTP(BaseHTTPRequestHandler):

    model = NBow.create_model()

    def do_GET(self):
        print("Get Recognized")
        f = open('responses.json')
        responses = json.load(f)
        try:
            
            url = urlparse(self.path)
            print(url)
            body = parse_qs(url.query)['Sentiment']
            if (body[0] == '1'):
                text = random.choice(responses['negative'])
            elif body[0] == '2':
                text = random.choice(responses['positive'])
            else:
                text = "No sentiment found"

            print(body)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            responseStr = json.dumps({'Text': text})
            self.wfile.write(bytes(responseStr,"utf-8"))
        except Exception as e:
            print(e)
            self.send_error(500, e)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            responseStr = json.dumps({'Text': "Sample Comment Here"})
            self.wfile.write(bytes(responseStr,"utf-8"))

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

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(NeuralHTTP, self).end_headers()
         
    def do_OPTIONS(self):
        print("Options recognized")
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), NeuralHTTP)
    print("Server running on port ", PORT)
    server.serve_forever()
    server.server_close()

