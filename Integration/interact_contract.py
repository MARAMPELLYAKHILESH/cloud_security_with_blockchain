from web3 import Web3

# Connect to your local Ganache blockchain
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

if w3.is_connected():
    print("Connected to Ganache")
else:
    print("Connection failed!")

# Replace with your deployed contract's address
contract_address = "0xD2a4e9B1965B0992197dE17e3dC765B00E36bA5E"

# Define the contract ABI as a Python literal with proper booleans
abi = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "string",
                "name": "fileId",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "masterHash",
                "type": "string"
            }
        ],
        "name": "MasterHashStored",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "fileId",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "masterHash",
                "type": "string"
            }
        ],
        "name": "storeMasterHash",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "fileId",
                "type": "string"
            }
        ],
        "name": "getMasterHash",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "name": "masterHashes",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)

# Function to store a master hash on-chain
def store_master_hash(file_id, master_hash, account, private_key):
    txn = contract.functions.storeMasterHash(file_id, master_hash).build_transaction({
        'from': account,
        'nonce': w3.eth.get_transaction_count(account),
        'gas': 3000000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    # Use 'raw_transaction' instead of 'rawTransaction'
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print("Transaction sent. Hash:", tx_hash.hex())
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transaction receipt:", receipt)
    return receipt

# Function to get a stored master hash
def get_stored_master_hash(file_id):
    stored_hash = contract.functions.getMasterHash(file_id).call()
    print(f"Stored master hash for '{file_id}' is: {stored_hash}")
    return stored_hash

if __name__ == "__main__":
    # Example usage:
    file_id = "sample_file.txt"
    master_hash = "c5a37e7b230ddb14402c3ed7a06b474fc683c733"  # Replace with your actual hash
    account = w3.eth.accounts[0]  # First account from Ganache
    private_key = "0x9e0015ef8b4a615e43169fb40d2be49d48c6a36d9b42df2674c78d70ebbd745e"  # Replace with the correct private key

    # Store the master hash on-chain
    store_master_hash(file_id, master_hash, account, private_key)
    # Retrieve it to verify
    get_stored_master_hash(file_id)
