from flask import Flask, request, jsonify
import hashlib
import os
import hmac
import time
import random
import string
from crypto import generate_keypair, sign_message, verify_signature
from blockchain import Blockchain

app = Flask(__name__)

# Simulate a distributed ledger using in-memory dictionary
ledger = {}
blockchain = Blockchain()
challenges = {}

@app.route('/')
def home():
    return "Welcome to QSDAS!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    if username in ledger:
        return jsonify({"message": "Username already registered."}), 400

    public_key, private_key = generate_keypair()
    ledger[username] = (public_key, private_key)
    blockchain.add_block({
        "action": "registration",
        "username": username,
        "public_key": public_key
    })
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
    else:
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
            "action": "zero_knowledge_authentication",
            "username": username,
            "challenge": challenge,
            "signature": signature
        })
        return jsonify({"message": "Zero-Knowledge Authentication successful."}), 200
    else:
        return jsonify({"message": "Zero-Knowledge Authentication failed."}), 401

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
    return jsonify({"length": len(chain_data), "chain": chain_data}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)