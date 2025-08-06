import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_PROVIDER")))

# Updated contract address after redeployment
contract_address = Web3.to_checksum_address("0x1012b75148f23848eb21a0a9b43e45d7f8ee07b8")
backend_wallet_address = Web3.to_checksum_address(os.getenv("BACKEND_WALLET_ADDRESS"))
backend_private_key = os.getenv("BACKEND_PRIVATE_KEY")

with open('DonorContractABI.json') as f:
    contract_abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=contract_abi)
