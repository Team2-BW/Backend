import requests
import config
import time
from utils import Stack, Queue
from room import Room

#Ryan: token = 'f816a2a8dfba25cdd1a305a303681c2ccef582a1'

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
    res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move", json=post_data, headers=headers)
    data = res.json()
    roomID = data['room_id']

    # Collect all rooms stored in the DB
    def get_room_dict():
        room_dict = {}
        room_list = requests.get('https://team2-bw.herokuapp.com/api/rooms/').json()
        for room in room_list:
            room_dict[room['id']] = room
        return room_dict
    
    # Variable for get_room_dict()
    rooms_we_have = get_room_dict()
        
    # Compares the current room to the list of visited rooms in the DB. If the ID doesn't exist, post current ID data.  
    if data['room_id'] not in rooms_we_have:
        db_send = {
            "id": data["room_id"],
            "coordinates": data["coordinates"],
            "name": data["title"],
            "description": data["description"],
        }
        requests.post("https://team2-bw.herokuapp.com/api/rooms/", json=db_send).json()     


    print(data)
    MapRoom.append(roomID)
    print(MapRoom)

    time.sleep(data['cooldown'])
