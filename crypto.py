import os
import hashlib
import hmac

# Keypair Generation (simulate Kyber)
def generate_keypair():
    private_key = os.urandom(32)  # 256-bit private key
    public_key = hashlib.sha3_256(private_key).hexdigest()  # Simulate public key with SHA3-256 (Post-Quantum safe)
    return public_key, private_key

# Signing a message (simulate Dilithium)
def sign_message(private_key, message):
    signature = hmac.new(private_key, message.encode(), hashlib.sha3_256).hexdigest()
    return signature

# Verifying signature
def verify_signature(public_key, message, signature, ledger):
    for user, (stored_pub, stored_priv) in ledger.items():
        if stored_pub == public_key:
            expected_signature = hmac.new(stored_priv, message.encode(), hashlib.sha3_256).hexdigest()
            return expected_signature == signature
    return False
