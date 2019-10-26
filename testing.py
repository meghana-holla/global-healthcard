from web3 import Web3

rpc = "http://127.0.0.1:8545"

web3 = Web3(Web3.HTTPProvider(rpc))

abi = '[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"cp","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"cd","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"allpatients","outputs":[{"name":"name","type":"string"},{"name":"age","type":"uint256"},{"name":"bloodgroup","type":"string"},{"name":"ndoc","type":"uint256"},{"name":"npres","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"alldoctors","outputs":[{"name":"name","type":"string"},{"name":"hospital","type":"string"},{"name":"npat","type":"uint256"},{"name":"specialization","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"pid","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"name","type":"string"},{"name":"hospital","type":"string"},{"name":"specialization","type":"string"}],"name":"initdoc","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"name","type":"string"},{"name":"age","type":"uint256"},{"name":"bloodgroup","type":"string"}],"name":"initpat","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"pattt","type":"uint256"},{"name":"n","type":"string"},{"name":"c","type":"string"},{"name":"dos","type":"uint256"},{"name":"u","type":"string"},{"name":"pe","type":"string"},{"name":"dur","type":"uint256"}],"name":"addPrescriptions","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
admin_acc = '0xB0BE5EFDe83490f0d8fC64120461660098AE7599'
pat = 0xe0e577218063fc8648A4b04fDcFe2fD02990f734

pat_key = "01519292e7b9fb0d98149b7b202cbd2b99d92857804140fe927855cc26026a9d"
pat_acc = "0xe0e577218063fc8648A4b04fDcFe2fD02990f734"

admin_pvtkey = '25d9479cd21fb800522f8e0c74513f0730f7afac9f3ac7a23d8ad69b7103be52'

contract_addr = "0xe0641afa5d665cA2c737bCA48AD7d5f1dba822CD"

contract = web3.eth.contract(address=contract_addr, abi=abi)

print(contract.caller().allpatients(pat_acc))

'''
transaction  = contract.functions.initdoc("xyz","dajdan","sa").buildTransaction()
transaction['nonce'] = web3.eth.getTransactionCount(admin_acc)

signed_tx = web3.eth.account.signTransaction(transaction, admin_pvtkey)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

print(tx_hash)
'''

'''
transaction  = contract.functions.initpat("xyz",1,"sa").buildTransaction()
transaction['nonce'] = web3.eth.getTransactionCount(pat_acc)

signed_tx = web3.eth.account.signTransaction(transaction, pat_key)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

print(tx_hash)
'''

'''
transaction  = contract.functions.addPrescriptions(pat,"xyz","rwe",325,"1-1-1","fsfs",4).buildTransaction()
transaction['nonce'] = web3.eth.getTransactionCount(admin_acc)

signed_tx = web3.eth.account.signTransaction(transaction, admin_pvtkey)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

print(tx_hash)
'''


