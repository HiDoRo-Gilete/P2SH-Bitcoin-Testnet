import utils, explorer
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

# Create a redeemScript

redeem_script = CScript([OP_2, seckey1.pub, seckey2.pub, OP_2, OP_CHECKMULTISIG])

# Create the magic P2SH scriptPubKey format from that redeemScript

script_pubkey = redeem_script.to_p2sh_scriptPubKey()

# Convert the P2SH scriptPubKey to a base58 Bitcoin address and print it.
address = CBitcoinAddress.from_scriptPubKey(script_pubkey)

print('Address:',str(address))


txid = lx("234bb48a9eee1b95c25be883f1784f984c6973527950e1be5cb0821bacca148d")
vout = 1 

amount = 1000

txin = CMutableTxIn(COutPoint(txid, vout))

# Specify a destination address and create the txout.
destination = CBitcoinAddress("2N4rB5gabVodvewzAbZXAcEJd2SFZWPpDfA").to_scriptPubKey() 
address_change = CBitcoinAddress("2N64Gjq151UBNkBoceMJ1EmxWmsqzeFFaeN").to_scriptPubKey()
txout = CMutableTxOut(amount, destination)
total = 29534
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

# SIGHASH_ALL.
sig1 = seckey1.sign(sighash) + bytes([SIGHASH_ALL])
sig2 = seckey2.sign(sighash) + bytes([SIGHASH_ALL])

# Construct a witness for this P2WSH transaction and add to tx.
txin.scriptSig = CScript([OP_0, sig1, sig2, redeem_script])
VerifyScript(txin.scriptSig, script_pubkey, tx, 0, (SCRIPT_VERIFY_P2SH,))
# Done
#broadcast
tx_hex = b2x(tx.serialize())

txid=utils.broadcast_testnet_transaction_blockstream(tx_hex)
if txid !=None:
    print("Transaction detail")
    explorer.get_transaction_detail(txid)

    