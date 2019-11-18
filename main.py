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
room_exits = data['exits']
roomID = data['room_id']

roomInfo = f'room_id: {data["room_id"]}, title: {data["title"]}, coords: {data["coordinates"]}'
print(roomInfo)

reverseDirections = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
traversalPath = []
reversePath = []
visitedRoom = {}
MapRoom = []

# Start with current room 0 and get it's exits
# visitedRoom[roomID] = room_exits

# Traverse entire graph while the rooms visited is less than 500
while len(visitedRoom) < 500:
    unvisited = []
    room_exits = data['exits']
    items = data['items']
    
    # take the items in room
    if len(items) > 0:
        for item in items:
            res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/take/", json={'name': f'{item}'}, headers=headers)
            print(res)
            time.sleep(data['cooldown'])
    
    # check stats
    res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/status/", headers=headers)
    stats = res.json()
    print(stats)
    time.sleep(data['cooldown'])
    
    visitedRoom[data["room_id"]] = data["coordinates"]
    print("visited room", visitedRoom)

    # enter next direction
    post_data = {
        "direction": input("Enter your direction: ")
    }
    
    res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv//move", json=post_data, headers=headers)
    data = res.json()
    roomID = data['room_id']

    print(data)
    time.sleep(data['cooldown'])