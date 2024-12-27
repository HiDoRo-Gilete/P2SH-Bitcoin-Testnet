# utils
# P2PKH Script
import os
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin import SelectParams
from bitcoin.core import lx, COutPoint
from bitcoin.core import CMutableTxOut, CMutableTxIn, CMutableTransaction
from bitcoin.core.script import CScript, SignatureHash, SIGHASH_ALL
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
