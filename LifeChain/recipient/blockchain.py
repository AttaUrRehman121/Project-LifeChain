import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize variables with defaults
w3 = None
contract = None
contract_address = None
backend_wallet_address = None
backend_private_key = None

try:
    from web3 import Web3
    
    # Only initialize Web3 if blockchain provider is available
    blockchain_provider = os.getenv("BLOCKCHAIN_PROVIDER")
    if blockchain_provider:
        w3 = Web3(Web3.HTTPProvider(blockchain_provider))
        
        # Contract address
        contract_address = Web3.to_checksum_address("0x1012b75148f23848eb21a0a9b43e45d7f8ee07b8")
        
        # Backend wallet details
        backend_wallet_address = os.getenv("BACKEND_WALLET_ADDRESS")
        if backend_wallet_address:
            backend_wallet_address = Web3.to_checksum_address(backend_wallet_address)
        
        backend_private_key = os.getenv("BACKEND_PRIVATE_KEY")
        
        # Load contract ABI if file exists
        abi_file_path = os.path.join(os.path.dirname(__file__), '..', 'DonorContractABI.json')
        if os.path.exists(abi_file_path):
            with open(abi_file_path) as f:
                contract_abi = json.load(f)
            contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        else:
            print("Warning: DonorContractABI.json not found")
            
except ImportError:
    print("Warning: web3 not available, blockchain functionality disabled")
except Exception as e:
    print(f"Warning: Error initializing blockchain: {e}")
