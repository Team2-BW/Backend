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
# room_exits = data['exits']
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

# Get stats
res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/status/", headers=headers)
stats = res.json()
print(stats)
inventory = stats['inventory']
time.sleep(data['cooldown'])

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

    # Sell items at Shop
    if (data['title'] == 'Shop'):
        while len(inventory) > 0:
            res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", json={'name':'treasure'}, headers=headers)
            time.sleep(data['cooldown'])
            print("Do you want to sell your treasure?")
            
            # Confirm to sell
            confirm_data = {
                "name":"tiny treasure", 
                "confirm": input("Confirm 'yes' to sell: ")
            }
            
            res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", json=confirm_data, headers=headers)
            print(res)
            time.sleep(data['cooldown'])

    # Pray at shrine
    if (data['title'] == "The Peak of Mt. Holloway" and data['name'] == "LeeTann"):

        res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/", headers=headers)
        print(res.json())
        time.sleep(data['cooldown'])


    # Change name when pirate is found
    if (data['title'] == "Pirate Ry's"):

        change_name_data ={
            "name": input("change your name: "),
            "confirm": input("Confirm 'aye' to change name: ")
        }

        res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/", json=change_name_data, headers=headers)
        nameChange = res.json()
        print(nameChange)
        time.sleep(data['cooldown'])
    

    # enter next direction
    post_data = {
        "direction": input("Enter your direction: ")
    }
    
    res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move/", json=post_data, headers=headers)
    data = res.json()
    roomID = data['room_id']

    print(data)
    time.sleep(data['cooldown'])

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

