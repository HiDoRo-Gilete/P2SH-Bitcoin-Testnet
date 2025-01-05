# main
import utils, explorer
import hashlib
from bitcoin.wallet import P2WPKHBitcoinAddress, P2PKHBitcoinAddress

# Step 1: Create a testnet address to receive and send funds
# Use fixed 32 bytes secret to get the same address every time
secret = hashlib.sha256(b'feed nephew grain suggest law faint female coin emerge neck traffic midnight easily female atom').digest()
my_private_key, my_public_key, my_address = utils.create_testnet_address(secret)

# View your wallet info
# explorer.get_wallet_info(my_address)
explorer.get_utxos(my_address) # determine the txid and output index to spend

# Step 2: Create a transaction input (UTXO)
# TODO: Update txid
txid = "c557dec748afed1bfd0fcb10ff7adad7405737dec016a6360b818207ceca4385" #  Transaction ID of the UTXO you want to spend
output_index = 0 # Index of the output in the transaction
txin = utils.create_txin(txid, output_index)

# Step 3: Create a transaction output
# TODO: Update destination_address

destination_address = P2WPKHBitcoinAddress("tb1qg6m8u3shyrgf6xz0wtq92jvxqpzdc9dh9sc2l3") # A SegWit P2PSH address
# destination_address = P2PKHBitcoinAddress("mmECzbuXu2D5gxgP5zsBPZu6dwmu9QFu3x") # P2PKH address

# TODO: Update total, amount_to_send and fee
total = 29853
amount_to_send = 10000 # Amount to send in satoshis
fee = 5000
txout = utils.create_txout(amount_to_send, destination_address)

# the transaction output for repayment
change_amount = total - amount_to_send - fee # Amount of satoshis will send back to your address
change_txout = utils.create_txout(change_amount, my_address)

# Step 4: Create and Sign the transaction
tx = utils.create_signed_transaction([txin], [txout, change_txout], my_private_key)

# Step 5: Broadcast the transaction
txid = utils.broadcast_testnet_transaction_blockstream(tx)
if txid != None:
    print("Transaction detail")
    explorer.get_transaction_detail(txid)