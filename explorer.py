# explorer
import json, io
import requests

# Testnet block explorer API endpoint
BLOCKSTREAM_API = "https://blockstream.info/testnet/api/address/"

# Get transactions for an address
def get_wallet_info(address):
    # Query the block explorer API for transactions related to the address
    url = f"{BLOCKSTREAM_API}{address}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"Address: {address}")
        print(f"Total Transactions: {data.get('chain_stats', {}).get('tx_count', 0)}")
        print(f"Total Received: {data.get('chain_stats', {}).get('funded_txo_sum', 0) / 1e8} BTC")
        print(f"Total Sent: {data.get('chain_stats', {}).get('spent_txo_sum', 0) / 1e8} BTC")

        txs = data.get("transactions", [])
        # Print all transaction IDs
        for tx in txs:
            print(f"Transaction ID: {tx.get('txid')}")
    else:
        print(f"Error fetching data for address {address}. HTTP Status: {response.status_code}")
          

# get utxos of an address
def get_utxos(address):
    url = f"{BLOCKSTREAM_API}{address}/utxo"
    response = requests.get(url)

    if response.status_code == 200:
        utxos = response.json()
        if not utxos:
            print("No UTXOs found for this address.")
        else:
            print(f"UTXOs for address {address}:")
            for utxo in utxos:
                print(f"  Transaction ID: {utxo['txid']}")
                print(f"  Output Index: {utxo['vout']}")
                print(f"  Value: {utxo['value'] / 1e8} BTC")
                print()
    else:
        print(f"Error fetching UTXOs for address {address}. HTTP Status: {response.status_code}")
    
def beautify(jsonobj):
  return json.dumps(jsonobj, sort_keys=False, indent=2)   
  
def get_transaction_detail(txid):
  try:
    TRANSACTION_API = "https://blockstream.info/testnet/api/tx/"
    response = requests.get(f"{TRANSACTION_API}{txid}")
    details = response.json()
    print(beautify(details))
    return details
  except:
    pass

