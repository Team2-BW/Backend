import config
import requests
import time
import random
import json
from utils import Stack, Queue
from room import Room

# token = config.TOKEN

# headers = {
#     'Authorization': f"Token {token}",
#     'Content-Type': 'application/json'
# }

# init_response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)
# data = init_response.json()
# print(data)

# time.sleep(data['cooldown'])
# room_exits = data['exits']
# roomID = data['room_id']

# roomInfo = f'room_id: {data["room_id"]}, title: {data["title"]}, coords: {data["coordinates"]}'
# print(roomInfo)

# traversalPath = []
# reversePath = []
# visitedRoom = {}
# MapRoom = []

# # Start with current room 0 and get it's exits
# # visitedRoom[roomID] = room_exits

# # Get stats
# res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/status/", headers=headers)
# stats = res.json()
# print(stats)
# inventory = stats['inventory']
# time.sleep(data['cooldown'])

# # Traverse entire graph while the rooms visited is less than 500
# while len(visitedRoom) < 500:
#     unvisited = []
#     room_exits = data['exits']
#     items = data['items']
    
#     # take the items in room
#     if len(items) > 0:
#         for item in items:
#             res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/take/", json={'name': f'{item}'}, headers=headers)
#             print(res)
#             time.sleep(data['cooldown'])
    
#         # check stats
#         res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/status/", headers=headers)
#         stats = res.json()
#         print(stats)
#         time.sleep(data['cooldown'])
    
#     visitedRoom[data["room_id"]] = data["coordinates"]
#     print("visited room", visitedRoom)

#     # Sell items at Shop
#     if (data['title'] == 'Shop'):
#         while len(inventory) > 0:
#             res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", json={'name':'treasure'}, headers=headers)
#             time.sleep(data['cooldown'])
#             print("Do you want to sell your treasure?")
            
#             # Confirm to sell
#             confirm_data = {
#                 "name":"tiny treasure", 
#                 "confirm": input("Confirm 'yes' to sell: ")
#             }
            
#             res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", json=confirm_data, headers=headers)
#             print(res)
#             time.sleep(data['cooldown'])

#     # enter next direction
#     post_data = {
#         "direction": input("Enter your direction: ")
#     }
    
#     res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv//move", json=post_data, headers=headers)
#     data = res.json()
#     roomID = data['room_id']

#     print(data)
#     time.sleep(data['cooldown'])

#     # Collect all rooms stored in the DB
#     def get_room_dict():
#         room_dict = {}
#         room_list = requests.get('https://team2-bw.herokuapp.com/api/rooms/').json()
#         for room in room_list:
#             room_dict[room['id']] = room
#         return room_dict

#     # Variable for get_room_dict()
#     rooms_we_have = get_room_dict()

#     # Compares the current room to the list of visited rooms in the DB. If the ID doesn't exist, post current ID data.  
#     if data['room_id'] not in rooms_we_have:
#         db_send = {
#             "id": data["room_id"],
#             "coordinates": data["coordinates"],
#             "name": data["title"],
#             "description": data["description"],
#         }
#         requests.post("https://team2-bw.herokuapp.com/api/rooms/", json=db_send).json()

traversalGraph = {}

def writeCurrentRoom(data):
    with open('currentRoom.json', 'w') as currentRoom:
        currentRoom.write(json.dumps(data))

def readCurrentRoom():
    with open('currentRoom.json', 'r') as currentRoom:
        data=currentRoom.read()
        return json.loads(data)

def getItemsFromRoom():
    current_room = readCurrentRoom()
    
    for item in current_room['items']:
        print("Taking item")
        tmpData = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/take/", json={'name': f'{item}'}, headers=headers).json()
        print(f"waiting {tmpData['cooldown']} secs")
        time.sleep(tmpData['cooldown'])

def movePlayerAndWait(direction):
    current_room = readCurrentRoom()
    print(f"moving in direction: {direction}")
    
    post_data = {
        "direction": direction
    }
    
    res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv//move", json=post_data, headers=headers)
    writeCurrentRoom(res.json())
    current_room = res.json()

    print(f"waiting {current_room['cooldown']} secs")

    time.sleep(current_room['cooldown'])
    addCurrentRoomToGraph()
    getItemsFromRoom()

def addCurrentRoomToGraph():
    current_room = readCurrentRoom();
    tmp = {}
    if current_room['room_id'] not in traversalGraph:
        for i in current_room['exits']:
            tmp[i] = "?"
        traversalGraph[current_room['room_id']] = tmp
        # send current room to backend
        db_send = {
            "id": current_room["room_id"],
            "coordinates": current_room["coordinates"],
            "name": current_room["title"],
            "description": current_room["description"],
        }
        requests.post("https://team2-bw.herokuapp.com/api/rooms/", json=db_send).json()
        print("posted to db")

def findUnexploredRoom():
    current_room = readCurrentRoom();
    q = Queue()
    q.enqueue([current_room['room_id']])

    while q.size():
        path = q.dequeue()
        room = path[-1]
        
        for i in traversalGraph[room]:
            if traversalGraph[room][i] == "?":
                return path
            else:
                path_copy = path[:]
                path_copy.append(traversalGraph[room][i])
                q.enqueue(path_copy)

    return None
    

def movePlayerToDeadEnd():
    current_room = readCurrentRoom();
    addCurrentRoomToGraph()

    startRoom = current_room["room_id"]
    startExits = current_room['exits']

    nonExplored = []
    
    for i in startExits:
        if traversalGraph[startRoom][i] == "?":
            nonExplored.append(i)

    if len(nonExplored) < 1:
        return
    else:
        direction = nonExplored[int(random.uniform(0, len(nonExplored) - 1))]

        movePlayerAndWait(direction)
        addCurrentRoomToGraph()
        current_room = readCurrentRoom();

        traversalGraph[startRoom][direction] = current_room["room_id"]

        if direction == "n":
            traversalGraph[current_room["room_id"]]["s"] = startRoom
        elif direction == "e":
            traversalGraph[current_room["room_id"]]["w"] = startRoom
        elif direction == "s":
            traversalGraph[current_room["room_id"]]["n"] = startRoom
        elif direction == "w":
            traversalGraph[current_room["room_id"]]["e"] = startRoom

        movePlayerToDeadEnd()

def traverseThisMap():
    current_room = readCurrentRoom();
    movePlayerToDeadEnd()
    unexploredPath = findUnexploredRoom()
    if unexploredPath == None:
        return
    else:
        for i in range(len(unexploredPath)):
            if current_room['room_id'] == unexploredPath[-1]:
                break
            for j in traversalGraph[current_room['room_id']]:
                if traversalGraph[current_room['room_id']][j] == unexploredPath[i]:
                    movePlayerAndWait(j)
                    current_room = readCurrentRoom();
    traverseThisMap()
    
token = config.TOKEN

headers = {
    'Authorization': f"Token {token}",
    'Content-Type': 'application/json'
}
writeCurrentRoom(requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers).json())

time.sleep(readCurrentRoom()['cooldown'])

addCurrentRoomToGraph()
traverseThisMap()