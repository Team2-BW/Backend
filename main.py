import config
import requests

token = config.TOKEN

headers = {
    'Authorization': f"TOKEN {token}",
    'Content-Type': 'application/json'
}

init_response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)
data = init_response.json()
print(data)

print(data['room_id'], data['title'], data['coordinates'], data['exits'], data['cooldown'])