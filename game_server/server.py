import json

from game_server.player_processor import PlayerProcessor
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 5216
player_processor = PlayerProcessor('basic')


# Technically a request handler but whatever
class Server(BaseHTTPRequestHandler):

    def post_success(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        postvars = self.rfile.read(content_length)
        postvars = json.loads(postvars.decode('utf-8'))
        print(f'Received {postvars} post request')
        if set(postvars.keys()) != set(['request_type', 'request_body']):
            print('Improper postvars format')
            self.send_response(1)
        post_rez = player_processor.process_post(postvars['request_type'], postvars['request_body'])
        if post_rez['rez'] == 'error':
            self.send_response(post_rez['error_code'])
        if post_rez['rez'] in {'name_change', 'success'}:
            self.post_success()
            self.wfile.write(json.dumps(post_rez)
                             .encode('utf-8'))

    # Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        json_string = json.dumps(player_processor.player_to_json())
        self.wfile.write(bytes(json_string, 'utf-8'))
        return

    def do_HEALTH(self):
        self.send_response(200)
        self.wfile.write(json.dumps({'health': 'good'}).encode('utf-8'))
        return


try:
    # Create a web game_server and define the handler to manage the
    print(f'Server started at {PORT_NUMBER}')
    server = HTTPServer(('', PORT_NUMBER), Server)
    server.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down the web game_server')
    server.socket.close()
