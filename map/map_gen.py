import json

AIR = 0
SOLID = 1
DEATH = 2

length = 600
height = 600
map = {
    'map_name': 'basic',
    'length': length,
    'height': height,
    'spawn_x': 300,
    'spawn_y': 500,
    'stage':
        [[AIR] * length] * 500 +
        [[SOLID] * length] * 100

}

with open(f'map/data/{map["map_name"]}', 'w') as write:
    json.dump(map, write, indent=4)
