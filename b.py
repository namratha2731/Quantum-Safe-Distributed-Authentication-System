from flask import Flask, request, jsonify
from blockchain import Blockchain
from crypto import generate_keypair, sign_message, verify_signature
import requests
import random
import string
import time

app = Flask(__name__)
ledger = {}
challenges = {}
blockchain = Blockchain()

# Modify these per node
PORT = 5002
PEERS = ["http://127.0.0.1:5001", "http://127.0.0.1:5003"]

@app.route('/')
def home():
    return f"Welcome to AuthNode on port {PORT}!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')

    if username in ledger:
        return jsonify({"message": "User already registered."}), 400

    public_key, private_key = generate_keypair()
    ledger[username] = (public_key, private_key)

    block_data = {
        "action": "register",
        "username": username,
        "public_key": public_key
    }
    blockchain.add_block(block_data)

    # Broadcast new block to peers
    for peer in PEERS:
        try:
            requests.post(f"{peer}/sync_block", json={"block": blockchain.get_latest_block().__dict__})
        except:
            pass

    return jsonify({
        "message": "Registration successful.",
        "username": username,
        "public_key": public_key
    }), 200

@app.route('/sign', methods=['POST'])
def sign():
    data = request.get_json()
    username = data.get('username')
    message = data.get('message')

    if username not in ledger:
        return jsonify({"message": "User not found."}), 404

    public_key, private_key = ledger[username]
    signature = sign_message(private_key, message)
    return jsonify({
        "message": "Signature generated.",
        "username": username,
        "signature": signature
    }), 200

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    username = data.get('username')
    message = data.get('message')
    signature = data.get('signature')

    if username not in ledger:
        return jsonify({"message": "User not found."}), 404

    public_key, _ = ledger[username]
    if verify_signature(public_key, message, signature, ledger):
        blockchain.add_block({
            "action": "authentication",
            "username": username,
            "message": message,
            "signature": signature
        })
        return jsonify({"message": "Authentication successful."}), 200
    return jsonify({"message": "Authentication failed."}), 401

@app.route('/challenge', methods=['POST'])
def generate_challenge():
    data = request.get_json()
    username = data.get('username')

    if username not in ledger:
        return jsonify({"message": "User not found."}), 404

    challenge = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    challenges[username] = challenge
    return jsonify({
        "message": "Challenge generated.",
        "challenge": challenge
    }), 200

@app.route('/verify', methods=['POST'])
def verify_challenge():
    data = request.get_json()
    username = data.get('username')
    signature = data.get('signature')

    if username not in ledger or username not in challenges:
        return jsonify({"message": "User or challenge not found."}), 404

    challenge = challenges.pop(username)
    public_key, _ = ledger[username]

    if verify_signature(public_key, challenge, signature, ledger):
        blockchain.add_block({
            "action": "zk_authentication",
            "username": username,
            "challenge": challenge,
            "signature": signature
        })
        return jsonify({"message": "Zero-Knowledge Authentication successful."}), 200
    return jsonify({"message": "Zero-Knowledge Authentication failed."}), 401

@app.route('/sync_block', methods=['POST'])
def sync_block():
    data = request.get_json()
    incoming_block = data['block']
    last_block = blockchain.get_latest_block()

    if incoming_block['previous_hash'] == last_block.hash:
        blockchain.chain.append(Block(
            index=incoming_block['index'],
            timestamp=incoming_block['timestamp'],
            data=incoming_block['data'],
            previous_hash=incoming_block['previous_hash']
        ))
        return jsonify({"message": "Block synced"}), 200
    return jsonify({"message": "Block rejected (hash mismatch)"}), 400

@app.route('/consensus', methods=['GET'])
def consensus():
    longest_chain = blockchain.chain
    for peer in PEERS:
        try:
            res = requests.get(f"{peer}/chain")
            peer_chain = res.json()['chain']
            if len(peer_chain) > len(longest_chain):
                longest_chain = [Block(**b) for b in peer_chain]
        except:
            continue

    blockchain.chain = longest_chain
    return jsonify({"message": "Consensus complete.", "length": len(blockchain.chain)}), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({
        "length": len(blockchain.chain),
        "chain": [block.__dict__ for block in blockchain.chain]
    }), 200

if __name__ == '__main__':
    print("b.py is loaded!")

if __name__ == '__main__':
    print("Starting Flask app on port 5002...")
    app.run(debug=True, port=5002)


