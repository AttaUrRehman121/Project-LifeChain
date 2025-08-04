from web3 import Web3
import secrets

def create_eth_wallet():
    account = Web3().eth.account.create(secrets.token_hex(32))
    print("Connect to YOur Wallet")
    return account.address, account.key.hex()
