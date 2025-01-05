# utils
# P2PKH Script
import os
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress, P2SHBitcoinAddress
from bitcoin import SelectParams
from bitcoin.core import lx, COutPoint
from bitcoin.core import CMutableTxOut, CMutableTxIn, CMutableTransaction
from bitcoin.core.script import CScript, SignatureHash, SIGHASH_ALL,OP_2,OP_CHECKMULTISIG
from bitcoin.core.scripteval import VerifyScript

def create_testnet_address(secret = None):
  SelectParams('testnet')
  if secret == None: secret = os.urandom(32)
  # Generate a random private key
  private_key = CBitcoinSecret.from_secret_bytes(secret)
  # Derive the public key and Bitcoin address
  public_key = private_key.pub
  address = P2PKHBitcoinAddress.from_pubkey(public_key)
  print("Private Key:", private_key)
  print("Public Key:", public_key.hex())
  print("Bitcoin Address:", address)
  return private_key, public_key, address

def create_txin(txid, output_index):
    return CMutableTxIn(prevout=COutPoint(lx(txid), output_index))

def create_txout(amount_to_send, recipient_address):
    recipient_scriptPubKey = recipient_address.to_redeemScript()
    return CMutableTxOut(amount_to_send, recipient_scriptPubKey)

def create_signed_transaction(inputs, outputs, my_private_key):
    my_address = P2PKHBitcoinAddress.from_pubkey(my_private_key.pub)
    print(my_address)
    tx = CMutableTransaction(inputs, outputs)

    sighash = SignatureHash(script=my_address.to_scriptPubKey(), txTo=tx, inIdx=0, hashtype=SIGHASH_ALL)
    signature = my_private_key.sign(sighash) + bytes([SIGHASH_ALL])

    # Add the signature and public key to the scriptSig of txin
    tx.vin[0].scriptSig = CScript([signature, my_private_key.pub])

    VerifyScript(tx.vin[0].scriptSig, my_address.to_scriptPubKey(), tx, 0)
    return tx

#============================================= P2SH ===========================================
def createMultisigAddress():
    # 2-of-2 Multisig Script
    # Generate two random private keys
    private_key1 = CBitcoinSecret.from_secret_bytes(os.urandom(32))
    private_key2 = CBitcoinSecret.from_secret_bytes(os.urandom(32))
    # Derive the public keys
    public_key1 = private_key1.pub
    public_key2 = private_key2.pub
    # Create a 2-of-2 multisig redeem script
    redeem_script = CScript([OP_2, public_key1, public_key2, OP_2, OP_CHECKMULTISIG])
    # Create a P2SH address from the redeem script
    address = P2SHBitcoinAddress.from_redeemScript(redeem_script)
    print("Private Key 1:", private_key1)
    print("Private Key 2:", private_key2)
    print("Redeem Script:", redeem_script.hex())
    print("Multisig Address:", address)

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