try:
    from web3 import Web3
    import secrets
    
    def create_eth_wallet():
        account = Web3().eth.account.create(secrets.token_hex(32))
        print("Connect to Your Wallet")
        return account.address, account.key.hex()
        
except ImportError:
    print("Warning: web3 not available, wallet creation disabled")
    
    def create_eth_wallet():
        print("Error: web3 not available")
        return None, None
