import config
import requests
import time
from utils import Stack, Queue
from room import Room

token = config.TOKEN

headers = {
    'Authorization': f"Token {token}",
    'Content-Type': 'application/json'
}

init_response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)
data = init_response.json()
print(data)

time.sleep(data['cooldown'])

def get_room_dict():
    room_dict = {}
    room_list = requests.get('https://team2-bw.herokuapp.com/api/rooms/').json()
    for room in room_list:
        room_dict[room['id']] = room
        print(room['id'])
    return room_dict

get_room_dict()