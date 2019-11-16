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

roomID = data['room_id']
room_exits = data['exits']

reverseDirections = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
traversalPath = []
reversePath = []
visitedDict = {}
MapRoom = []

# Start with current room 0 and get it's exits
visitedDict[roomID] = room_exits

# Traverse entire graph while the rooms visited is less than 500
while len(MapRoom) < 500:

    post_data = {
        "direction": input("Enter your direction: ")
    }
    
    # Request to move
    res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv//move", json=post_data, headers=headers)
    data = res.json()
    roomID = data['room_id']

    print(data)
    MapRoom.append(roomID)
    print(MapRoom)

    time.sleep(data['cooldown'])