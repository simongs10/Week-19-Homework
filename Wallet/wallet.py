import subprocess
import json
import os
from dotenv import load_dotenv
from constants import *
from web3 import Web3
from eth_account import Account
from bit.network import NetworkAPI
from bit import PrivateKeyTestnet

load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3

mnemonic = "cactus exotic mango damage universe sniff history cheese image such surface hard"
# Create a function called `derive_wallets`
def derive_wallets(coin=BTC, mnemonic=mnemonic, numderive=3):
    command = f'php ./derive -g --mnemonic="{mnemonic}" --cols=all --coin={coin} --numderive={numderive} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

coin = {
    ETH:derive_wallets(coin=ETH),
    BTCTEST:derive_wallets(coin=BTCTEST)
}

def priv_key_to_account(coin, priv_key):
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    elif coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    else:
        print("Not a valid crypto")
        

def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": amount}
        )
        return {
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            "chainID": chainid,
        }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address,     [(to, amount, BTC)])
    
    
def send_tx(coin, account, to, amount):
    if coin == ETH:
        tx = create_raw_tx(account, to, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return result
    elif coin == BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed)


