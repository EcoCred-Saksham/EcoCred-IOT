from flask import Flask, jsonify, request
from web3 import Web3

app = Flask(__name__)
co2data=0
count=0


def receive_data():

    if request.is_json:
        global co2data, count
        data = request.get_json()
        data_value=int(data['value'])
        co2data+=data_value
        count+=1
        print(f"Received JSON data: {co2data}")
        #sys.stdout.flush()
        if(count>3):
            #execute_blockchain_code()
            count=0
        return jsonify({"message": "Data received", "data": data_value}), 200
    else:
        data = request.form['data']
        print(f"Received form data: {data}")
        return jsonify({"message": "Data received", "data": data_value}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




# Replace with your Infura or other RPC URL
rpc_url = "https://amoy.polygon.io"  # Example URL, replace with actual one
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Check if connected
if not web3.isConnected():
    raise Exception("Failed to connect to the Ethereum node")

# Replace with your contract address and ABI
contract_address = "0xYourContractAddress"
contract_abi = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "id", "type": "uint256"},
            {"internalType": "uint256", "name": "data", "type": "uint256"}
        ],
        "name": "addData",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "id", "type": "uint256"}],
        "name": "getData",
        "outputs": [
            {"internalType": "uint256[]", "name": "", "type": "uint256[]"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Your wallet address and private key
wallet_address ="0x7c26d596578bbDf17823efbE1F8c61a52b433898"
private_key = ""

# Function to execute addData
def add_data(id, data):
    # Build the transaction
    nonce = web3.eth.getTransactionCount(wallet_address)
    transaction = contract.functions.addData(id, data).buildTransaction({
        'chainId': web3.eth.chain_id,
        'gas': 2000000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': nonce,
    })
    
    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
    
    # Send the transaction
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    # Wait for the transaction to be mined
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt

# Example usage
id = 1
data = 100

receipt = add_data(id, data)
print(f"Transaction successful with hash: {receipt.transactionHash.hex()}")

