# Quantum-Safe Distributed Authentication System

This project develops a Quantum-Safe Distributed Authentication System (QSDAS) designed to protect against future quantum attacks. It ensures secure and reliable authentication in distributed networks by integrating quantum-resistant algorithms and leveraging blockchain technology for a transparent and immutable ledger of authentication events.

## Features

  * **Quantum-Safe Cryptography**: Utilizes simulated post-quantum cryptography algorithms (Kyber for key generation, Dilithium for signing) to resist quantum computer attacks.
  * **Distributed Architecture**: Implemented as a multi-node Flask application, simulating a distributed network where authentication requests are processed across different nodes.
  * **Blockchain Integration**: A simple blockchain is used as a distributed, immutable ledger to record registration, authentication, and zero-knowledge authentication events.
  * **User Registration**: Allows new users to register, generating a unique public/private key pair.
  * **Message Signing and Verification**: Users can sign messages, and their signatures can be verified using their public keys.
  * **Authentication**: Supports traditional username/password-based authentication (though password handling is simplified in this simulation).
  * **Zero-Knowledge Authentication**: Implements a challenge-response mechanism for zero-knowledge proof of identity, where users can verify their identity without revealing their private key.
  * **Consensus Mechanism**: Nodes can synchronize their blockchain ledgers, ensuring consistency across the distributed network.

## Project Structure

The project consists of several Python files, each serving a specific purpose:

  * **`README.md`**: This file, providing an overview of the project, its features, and how to set it up and run.
  * **`a.py`**: Represents the primary authentication node (AuthNode) running on port 5000. It handles user registration, signing, authentication, challenge generation, and zero-knowledge verification. It also maintains its own blockchain instance.
  * **`b.py`**: Another authentication node (AuthNode) running on port 5002. Similar to `a.py`, it handles authentication requests but also includes peer-to-peer communication for block synchronization and consensus.
  * **`c.py`**: A third authentication node (AuthNode) running on port 5003. It functions similarly to `b.py`, participating in the distributed network for authentication, block synchronization, and consensus.
  * **`blockchain.py`**: Defines the `Block` and `Blockchain` classes.
      * `Block`: Represents a single block in the blockchain, containing an index, timestamp, data (action details), previous hash, and its own hash.
      * `Blockchain`: Manages the chain of blocks, including creating the genesis block, adding new blocks, and retrieving the latest block.
  * **`crypto.py`**: Implements the cryptographic functionalities for the system.
      * `generate_keypair()`: Simulates Kyber for generating a public and private key pair.
      * `sign_message()`: Simulates Dilithium for signing a message using a private key.
      * `verify_signature()`: Verifies a signature against a message and a public key.

## How it Works

The system operates as a network of distributed authentication nodes (`a.py`, `b.py`, `c.py`). Each node maintains its own copy of a blockchain-based ledger.

1.  **Key Generation and Registration**: When a user registers, a quantum-safe public/private key pair is generated using `crypto.py`. The public key and registration action are recorded on the blockchain.
2.  **Authentication**: Users can authenticate by signing a message with their private key. The node verifies the signature using the stored public key from its ledger.
3.  **Zero-Knowledge Proof (ZKP)**: For enhanced security, the system supports ZKP. A node generates a random challenge, and the user signs this challenge with their private key. The node then verifies the signature without needing to know the user's private key, proving identity without revealing sensitive information.
4.  **Blockchain as Ledger**: All significant events (registration, authentication, ZKP) are added as new blocks to the node's blockchain.
5.  **Distributed Consensus**: Nodes communicate with each other (`sync_block` and `consensus` routes in `b.py` and `c.py`) to synchronize their blockchains, ensuring data consistency and integrity across the distributed network. The longest chain rule is applied for consensus.

## Setup and Running the Project

To run this distributed system, you need to have Python and Flask installed.

1.  **Clone the Repository (if not already done)**:

    ```bash
    git clone [repository_url]
    cd Distributed-system
    ```

2.  **Install Dependencies**:

    ```bash
    pip install Flask requests
    ```

3.  **Run the Nodes**:
    Open three separate terminal windows or command prompts.

    **Terminal 1 (Node A - Port 5000):**

    ```bash
    python a.py
    ```

    **Terminal 2 (Node B - Port 5002):**

    ```bash
    python b.py
    ```

    **Terminal 3 (Node C - Port 5003):**

    ```bash
    python c.py
    ```

    *Note: Ensure that the `PEERS` list in `b.py` and `c.py` correctly points to the addresses of other running nodes.*

## API Endpoints

Once the nodes are running, you can interact with the system using these API endpoints:

### Common Endpoints (available on all nodes)

  * **GET `/`**:

      * **Description**: Welcome message for the node.
      * **Example**: `http://127.0.0.1:5000/`

  * **POST `/register`**:

      * **Description**: Registers a new user and generates a quantum-safe keypair.
      * **Request Body**:
        ```json
        {
            "username": "your_username"
        }
        ```
      * **Example**: `http://127.0.0.1:5000/register`

  * **POST `/sign`**:

      * **Description**: Signs a message with the user's private key.
      * **Request Body**:
        ```json
        {
            "username": "your_username",
            "message": "message_to_sign"
        }
        ```
      * **Example**: `http://127.0.0.1:5000/sign`

  * **POST `/authenticate`**:

      * **Description**: Authenticates a user by verifying a signed message.
      * **Request Body**:
        ```json
        {
            "username": "your_username",
            "message": "original_message",
            "signature": "signature_string"
        }
        ```
      * **Example**: `http://127.0.0.1:5000/authenticate`

  * **POST `/challenge`**:

      * **Description**: Generates a challenge for Zero-Knowledge Authentication.
      * **Request Body**:
        ```json
        {
            "username": "your_username"
        }
        ```
      * **Example**: `http://127.0.0.1:5000/challenge`

  * **POST `/verify`**:

      * **Description**: Verifies the signature of a challenge for Zero-Knowledge Authentication.
      * **Request Body**:
        ```json
        {
            "username": "your_username",
            "signature": "signed_challenge"
        }
        ```
      * **Example**: `http://127.0.0.1:5000/verify`

  * **GET `/chain`**:

      * **Description**: Retrieves the full blockchain of the current node.
      * **Example**: `http://127.0.0.1:5000/chain`

### Node-Specific Endpoints (for `b.py` and `c.py`)

  * **POST `/sync_block`**:

      * **Description**: Allows peers to synchronize new blocks.
      * **Request Body**:
        ```json
        {
            "block": {
                "index": 1,
                "timestamp": 1678886400,
                "data": {"action": "registration", "username": "testuser"},
                "previous_hash": "..."
            }
        }
        ```
      * **Example**: (Internal peer communication)

  * **GET `/consensus`**:

      * **Description**: Initiates the consensus mechanism to synchronize the node's blockchain with the longest chain among its peers.
      * **Example**: `http://127.0.0.1:5002/consensus`

## Conclusion

This project demonstrates a foundational Quantum-Safe Distributed Authentication System. While the cryptographic implementations are simulated for simplicity, the architecture showcases how blockchain can be integrated into distributed systems for secure and verifiable authentication processes, with an eye towards future quantum security challenges.
