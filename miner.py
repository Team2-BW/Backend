import config
import requests
import time
import hashlib
from timeit import default_timer as timer


token = config.TOKEN

# Start the game
headers = {
    'Authorization': f"Token {token}",
    'Content-Type': 'application/json'
}

init_response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)
data = init_response.json()
print(data)
time.sleep(data['cooldown'])

# Add difficulty to proof_of_work
def proof_of_work(last_proof, difficulty):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    - Note:  We are adding the hash of the last proof to a number/nonce for the new proof
    """

    start = timer()

    print("Searching for next proof")
    proof = 0
    #  TODO: Your code here

    while valid_proof(last_proof, proof, difficulty) is False:
        proof += 1

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof

# Add difficulty to valid_proof
def valid_proof(last_hash, proof, difficulty):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the proof?

    IE:  last_hash: ...AE9123456, new hash 123456888...
    """

    # TODO: Your code here!
    
    last_hash = str(last_hash)
    guess = f'{last_hash}{proof}'.encode()
    hashed_proof = hashlib.sha256(guess).hexdigest()

    # Update hash with difficulty
    if difficulty is not None:
        leading_zeros = "0" * difficulty
    else:
        leading_zeros = "0" * 6

    return hashed_proof[0:difficulty] == leading_zeros

# Get Proof
res = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/", headers=headers)
proof_data = res.json()
print(proof_data)

new_proof = proof_of_work(proof_data['proof'], proof_data['difficulty'])

# Mine the room
if new_proof != '':

    post_data = {
        "proof": new_proof
    }

    res = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/", json=post_data, headers=headers)
    mining_data = res.json()
    print(mining_data)
    time.sleep(data['cooldown'])