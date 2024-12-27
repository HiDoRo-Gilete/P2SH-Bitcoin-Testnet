import hashlib

from bitcoin import SelectParams
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_0, OP_2, OP_HASH160, OP_EQUALVERIFY, OP_CHECKMULTISIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret


SelectParams('testnet')

# first key
seckey1 = CBitcoinSecret('cN1XQx8o4efyix7h48RcQkEhPurSJd1sFrhv3NhzRZpbzAUXfnk2')

# second key
seckey2 = CBitcoinSecret('cVisGjUQRcPHoSrb3MPNPSRCTLn62Wo9oCqZXjtpe34h11BgWS6M')

# Create a redeemScript. Similar to a scriptPubKey the redeemScript must be
# satisfied for the funds to be spent.
redeem_script = CScript([OP_2, seckey1.pub, seckey2.pub, OP_2, OP_CHECKMULTISIG])

# Create the magic P2SH scriptPubKey format from that redeemScript. You should
# look at the CScript.to_p2sh_scriptPubKey() function in bitcoin.core.script to
# understand what's happening, as well as read BIP16:
# https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki
script_pubkey = redeem_script.to_p2sh_scriptPubKey()

# Convert the P2SH scriptPubKey to a base58 Bitcoin address and print it.
# You'll need to send some funds to it to create a txout to spend.
address = CBitcoinAddress.from_scriptPubKey(script_pubkey)

print('Address:',str(address))


txid = lx("2bc9d15610ddc3d71861f7cc9ce281093c7d5680cffd00ac1197b5a944b421e7")
vout = 0

# Specify the amount send to your P2WSH address.
amount = 1000

# Calculate an amount for the upcoming new UTXO. Set a high fee (5%) to bypass bitcoind minfee
# setting on regtest.

# Create the txin structure, which includes the outpoint. The scriptSig defaults to being empty as
# is necessary for spending a P2WSH output.
txin = CMutableTxIn(COutPoint(txid, vout))

# Specify a destination address and create the txout.
destination = CBitcoinAddress("2N4rB5gabVodvewzAbZXAcEJd2SFZWPpDfA").to_scriptPubKey() 
address_change = CBitcoinAddress("2N64Gjq151UBNkBoceMJ1EmxWmsqzeFFaeN").to_scriptPubKey()
txout = CMutableTxOut(amount, destination)
total = 44000
fee=4000
txout_change = CMutableTxOut(total-fee-amount,address_change)


# Create the unsigned transaction.
tx = CMutableTransaction([txin], [txout,txout_change])

# Calculate the signature hash for that transaction.
sighash = SignatureHash(
    script=redeem_script,
    txTo=tx,
    inIdx=0,
    hashtype=SIGHASH_ALL
)

# Now sign it. We have to append the type of signature we want to the end, in this case the usual
# SIGHASH_ALL.
sig1 = seckey1.sign(sighash) + bytes([SIGHASH_ALL])
sig2 = seckey2.sign(sighash) + bytes([SIGHASH_ALL])

# Construct a witness for this P2WSH transaction and add to tx.
txin.scriptSig = CScript([OP_0, sig1, sig2, redeem_script])
VerifyScript(txin.scriptSig, script_pubkey, tx, 0, (SCRIPT_VERIFY_P2SH,))
# Done! Print the transaction
tx_hex = b2x(tx.serialize())
print(b2x(tx.serialize()))


# import requests

# url = 'https://bitcoin-testnet.drpc.org'

# data = {
#     "method": "sendrawtransaction",
#     "params": [tx_hex]
# }

# response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
# res = response.json()

# print(res)

import requests
def broadcast_testnet_transaction_blockstream(raw_transaction):
    """Broadcasts a raw transaction to the Bitcoin testnet using Blockstream.info API.

    Args:
        raw_transaction: The hex-encoded string representing the raw transaction.

    Returns:
        The transaction ID (txid) as a string if successful, or None if an error occurs.
    """
    url = "https://blockstream.info/testnet/api/tx"
    headers = {'Content-Type': 'text/plain'}  # Important for Blockstream API

    try:
        response = requests.post(url, headers=headers, data=raw_transaction)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        txid = response.text  # Blockstream returns the txid directly in the response body
        return txid
    except requests.exceptions.RequestException as e:
        print(f"Error broadcasting transaction: {e}")
        if hasattr(e.response, 'text'):  # Print response text if available
            print(f"Server response: {e.response.text}")
        return None

txid=broadcast_testnet_transaction_blockstream(tx_hex)
if txid !=None:
    print(f"Public transaction success! id={txid}")
