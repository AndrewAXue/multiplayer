from basic_vars import Player
from map.map import Map



class PlayerProcessor:
    '''
        Contains a list of PlayerInfo and has all the logic with dealing with movement
    '''

    MISSING_PLAYER_ERROR = 2

    def __init__(self, map_name):
        # Local copy of Player
        self._players = {}
        self._map = Map(map_name)
        self._player_height = 20
        self._player_width = 10
        self._player_color = 'red'

    def check_req(self, req_body):
        if 'player_name' not in req_body:
            return self.MISSING_PLAYER_ERROR

    def process_post(self, req_type, req_body):
        error = self.check_req(req_body)
        if error:
            return {'rez': 'error', 'error_code': error}

        if req_type == 'add_player':
            dup_num = 0
            player_name = req_body['player_name']
            while player_name in self._players:
                dup_num += 1
                if dup_num == 1:
                    player_name += ' (1)'
                else:
                    player_name = player_name[:-4] + f' ({dup_num})'
            print(f'{self._map.spawn_point.x} {self._map.spawn_point.y}')
            self._players[player_name] = Player(self._map.spawn_point.clone(),
                                                self._player_height,
                                                self._player_width,
                                                self._player_color
                                                )
            self._map.spawn_player(self._players[player_name])
            return {'rez': 'success', 'map_name': self._map.map_name, 'new_name': player_name}
        if req_type == 'move_left':
            player_name = req_body['player_name']
            self._players[player_name].coord.x -= 1
        if req_type == 'move_right':
            player_name = req_body['player_name']
            self._players[player_name].coord.x += 1
        if req_type == 'kick_all':
            self._players = {}
        return {'rez': 'success'}

    def settle_players(self):
        # Physics (gravity) based changes to player pos
        pass

    def player_to_json(self):
        # Convert PlayerInfos to whatever info needs to be transmitted
        return {
            name: {'color': player_info.color,
                   'x_coord': player_info.coord.x,
                   'y_coord': player_info.coord.y,
                   'height': player_info.height,
                   'width': player_info.width
                   } for name, player_info in self._players.items()
        }
