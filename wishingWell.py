import config
import requests
import time

token = config.TOKEN

headers = {
    'Authorization': f"Token {token}",
    'Content-Type': 'application/json'
}

init_response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)
data = init_response.json()
print(data)
time.sleep(data['cooldown'])

# Examine Wishing Well
if (data['title']== "Wishing Well"):

    examine_data = {
        "name": "Wishing Well"
    }

    res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/", json=examine_data, headers=headers)
    examineWell = res.json()
    print(examineWell)
    wishing_well = examineWell['description']
    
    time.sleep(data['cooldown'])
    
    # Decode the binary message
    # Removes \n before code store in bit_code array
    bit_code = wishing_well.split("\n")[2:] 

    # Convert binary to decimal number with int()
    int_array = []
    for byte in bit_code:
        int_array.append(int(byte, 2)) 

    print(int_array)
    
    # Convert to character 
    convert = []
    for num in int_array[2::5]:
        convert.append(chr(num))
    print("".join(convert))

    # Mine your coin in room 346