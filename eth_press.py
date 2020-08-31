from web3 import Web3
from web3._utils.encoding import to_hex
from web3.middleware import geth_poa_middleware
from web3._utils.transactions import get_buffered_gas_estimate

import time

w3 = Web3(Web3.HTTPProvider('http://localhost:20636'))

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# new_account = w3.personal.newAccount("123")
# print('new account => {0}'.format(new_account))

accounts = w3.eth.accounts
print('accounts => {0}'.format(accounts))

balance = w3.eth.getBalance(accounts[0], 'latest')
print('balance before tx => {0}'.format(balance))

blockNumber = 0

while True:
    bn = w3.eth.blockNumber
    print('block number => {0}'.format(bn))

    transaction = {
        'from': accounts[0],
        'to': accounts[0],
        'value': 100
    }
    gas = get_buffered_gas_estimate(w3, transaction)
    gas_price = w3.eth.gasPrice
    # log_debug_print("use gas ", gas, "gasPrice", gas_price)
    transaction['gas'] = int(gas * 1)
    # transaction['gasPrice'] = int(gas_price * 1)

    tx_hash = w3.eth.sendTransaction(transaction)
    print('tx hash => {0}'.format(to_hex(tx_hash)))

    if bn > blockNumber:
        blockNumber = bn
        balance = w3.eth.getBalance(accounts[0], 'latest')
        print('balance after tx => {0}'.format(balance))

    time.sleep(0.2)

