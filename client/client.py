import requests
from map.graphics import *
from map.map import Map


class Client:
    def __init__(self, ip: str, port: str, player_name: str):
        self._url = f'http://{ip}:{port}'
        self._name = player_name
        self._map = None
        self._font_size = 13
        self._entities = {}
        self.connect()
        self._window = GraphWin('GAY', self._map.length, self._map.height)
        self._pressed = {}

    def post(self, request_type: str, request_body: Map = {}):
        request_body['player_name'] = self._name
        return requests.post(self._url, json={
            'request_type': request_type,
            'request_body': request_body
        }).json()

    def connect(self):
        # Try until the connection is up
        connected = False
        while not connected:
            try:
                requests.get(self._url)
                connected = True
            except:
                pass

        print(f'Connected to {self._url}')

        # Kick all other players
        #self.post('kick_all')
        response_json = self.post('add_player')

        # return {'rez': 'success', 'map_name': self._map.map_name, 'new_name': player_name}
        self._name = response_json['new_name']
        self._map = Map(response_json['map_name'])
        print(f'Name is {self._name}')
        print(f'Playing on map {self._map.map_name}')

    def draw(self):
        self._map.draw_stage(self._window)
        print('done drawing stage')
        while True:
            entity_info = None
            try:
                entity_info = requests.get(self._url).json()
            except:
                print('Problem with the server, shutting down')
            for player, player_info in entity_info.items():

                x, y = player_info['x_coord'], player_info['y_coord']
                height, width = player_info['height'], player_info['width']
                color = player_info['color']

                name_tag_x = x + width / 2
                name_tag_y = y - height - self._font_size
                if f'{player}_name' in self._entities:
                    item = self._entities[f'{player}_name']
                    item.move(name_tag_x - item.getAnchor().getX(),
                              name_tag_y - item.getAnchor().getY())
                else:
                    text = Text(Point(name_tag_x, name_tag_y), player)
                    text.setSize(self._font_size)
                    text.draw(self._window)
                    self._entities[f'{player}_name'] = text

                if player in self._entities:
                    item = self._entities[player]
                    item.move(x - item.getP1().getX(), y - item.getP1().getY())
                else:
                    rect = Rectangle(Point(x, y), Point(x + width, y - height))
                    rect.setFill(color)
                    rect.draw(self._window)
                    self._entities[player] = rect

            k = self._window.checkKey()
            if k == 'Left' or k == 'Right':
                self._pressed[k] = True
            elif k == '':
                self._pressed = {}
            if 'Left' in self._pressed:
                self.post('move_left')
            if 'Right' in self._pressed:
                self.post('move_right')
        self._window.getMouse()
        self._window.close()

ip = input('Enter ip to connect to\n')
if not ip:
    ip = '192.168.0.26'
port = input('Enter port to connect to\n')
if not port:
    port = '5216'
player_name = input('What do you want your player name to be?\n')
if not player_name:
    player_name = 'fishlicker'
client = Client(ip, port, player_name)
client.draw()
