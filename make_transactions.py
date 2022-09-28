import time
import web3
from ethtoken.abi import EIP20_ABI # this ABI works for ERC20 tokens

#w = web3.Web3(web3.HTTPProvider('https://mainnet.infura.io/805o3JxUvzvpJOAGRl56'))
w = web3.Web3(web3.HTTPProvider('https://api.myetherwallet.com/eth'))

def approve(token_addr, spender_address, amount, from_addr, gas_gwei, gas_limit, key, nonce=None):
	token_addr = web3.Web3.toChecksumAddress(token_addr)
	from_addr = web3.Web3.toChecksumAddress(from_addr)
	# nonce = w.eth.getTransactionCount(from_addr)
	if nonce!= None:
		print ('Nonce (ALREADY SET): {0}'.format(nonce))
	else:
		nonce = w.eth.getTransactionCount(from_addr)
		print ('Nonce (OBTAINED LIVE): {0}'.format(nonce))
	contract = w.eth.contract(token_addr, abi=EIP20_ABI)
	# token_name = contract.functions.name().call()
	token_symbol = contract.functions.symbol().call()
	token_decimals = contract.functions.decimals().call()
	DECIMALS = 10**token_decimals
	print('Approving {0} to spend {1} {2} tokens'.format(spender_address, amount, token_symbol))
	amount = hex(amount*DECIMALS)
	# create data
	method_id = '0x095ea7b3' # method id for approve
	second_line = spender_address[2:].zfill(64)
	third_line = amount[2:].zfill(64)
	data = method_id + second_line + third_line
	
	transaction = {
		'to': token_addr,
		'from': from_addr,
		'value': 0,
		'gas': gas_limit,
		'gasPrice':int(gas_gwei*(10**9)),
		# 'gasPrice':int(gas_price, 16), # gas price comes as a hex value which was already multiplied by 10**9
		'chainId':1,
		'nonce': nonce,
		'data': data
	}
	# attempt to sign and send transaction
	while True:
		try:
			signed_transaction = w.eth.account.signTransaction(transaction, key)
			transaction_id = w.eth.sendRawTransaction(signed_transaction.rawTransaction)
			break
		except Exception as e:
			print ('['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] Error occured: {0}\t TRYING AGAIN...'.format(str(e)))
	print ('\n['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] Approve Transaction sent. ID = https://etherscan.io/tx/{0}'.format(transaction_id.hex()))

# send some tokens to 'receiver_addr'
def send_token(token_addr, token_amount, from_addr, receiver_addr, gas_limit, gas_gwei, key, nonce=None):
	token_addr = web3.Web3.toChecksumAddress(token_addr)
	from_addr = web3.Web3.toChecksumAddress(from_addr)
	if nonce!= None:
		print ('Nonce (ALREADY SET): {0}'.format(nonce))
	else:
		nonce = w.eth.getTransactionCount(from_addr)
		print ('Nonce (OBTAINED LIVE): {0}'.format(nonce))
	contract = w.eth.contract(token_addr, abi=EIP20_ABI)
	token_name = contract.functions.name().call()
	token_symbol = contract.functions.symbol().call()
	token_decimals = contract.functions.decimals().call()
	DECIMALS = 10**token_decimals
	# print(type(token_decimals), type(DECIMALS))
	token_balance = contract.functions.balanceOf(from_addr).call() // DECIMALS
	eth_balance = float(w.fromWei(w.eth.getBalance(from_addr), 'ether'))
	print ('========= SENDING {0} ========='.format(token_symbol))
	print ('ETH balance: {0}'.format(eth_balance))
	print ('{0} balance: {1}\n'.format(token_symbol, token_balance))
	print ('FROM: {0}'.format(from_addr))
	print ('TO: {0}'.format(receiver_addr))
	print ('Amount of {0} to send: {1:.6f}'.format(token_symbol, token_amount))	
	print ('Gas Limit (smart contracts need more): {0}'.format(gas_limit))
	print ('Gas Price (most important): {0} gwei'.format(gas_gwei))
	# nonce = w.eth.getTransactionCount(from_addr)
	print ()

	method_name = '0xa9059cbb'	# transfer method for ERC20 tokens
	receiver_addr = receiver_addr[2:].zfill(64)	# prepends 0's to get length 64
	amount = str(hex(int(token_amount * DECIMALS)))[2:].zfill(64)
	data = method_name + receiver_addr + amount 

	# transaction
	transaction = {
		'to':token_addr,
		'from':from_addr,
		'value':0, # ETH DECIMAL is 18
		'gas':gas_limit,
		'gasPrice':int(gas_gwei*(10**9)),
		'chainId':1,
		'nonce': nonce,
		'data': data
	}
	# attempt to sign and send transaction
	while True:
		try:
			signed_transaction = w.eth.account.signTransaction(transaction, key)
			transaction_id = w.eth.sendRawTransaction(signed_transaction.rawTransaction)
			break
		except Exception as e:
			print ('['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] Error occured: {0}\t TRYING AGAIN...'.format(str(e)))
	print ('\n['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] {0} sent. ID = https://etherscan.io/tx/{1}'.format(token_symbol, transaction_id.hex()))

# send ETH to some address
def send_eth(amount, from_addr, to_addr, gas_limit, gas_gwei, key, nonce=None):
	to_addr = web3.Web3.toChecksumAddress(to_addr)
	from_addr = web3.Web3.toChecksumAddress(from_addr)
	print('here')
	# nonce = w.eth.getTransactionCount(from_addr)
	if nonce!= None:
		print ('Nonce (ALREADY SET): {0}'.format(nonce))
	else:
		nonce = w.eth.getTransactionCount(from_addr)
		print ('Nonce (OBTAINED LIVE): {0}'.format(nonce))
	eth_balance = float(w.fromWei(w.eth.getBalance(from_addr), 'ether'))
	print ('========= SENDING ETH =========')
	print ('ETH balance: {0}\n'.format(eth_balance))
	print ('FROM: {0}'.format(from_addr))
	print ('TO: {0}'.format(to_addr))
	print ('Amount of ETH to send: {0:.6f}'.format(amount))	
	print ('Gas Limit (smart contracts need more): {0}'.format(gas_limit))
	print ('Gas Price (most important): {0} gwei'.format(gas_gwei))
	
	transaction = {
		'to':to_addr,
		'from':from_addr,
		'value':int(amount*(10**18)),
		'gas':gas_limit,
		'gasPrice':int(gas_gwei*(10**9)),
		'chainId':1,
		'nonce': nonce
	}

	# attempt to sign and send transaction
	while True:
		try:
			signed_transaction = w.eth.account.signTransaction(transaction, key)
			transaction_id = w.eth.sendRawTransaction(signed_transaction.rawTransaction)
			break
		except Exception as e:
			print ('['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] Error occured: {0}\t TRYING AGAIN...'.format(str(e)))
	print ('\n['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] ETH sent. ID = https://etherscan.io/tx/{0}'.format(transaction_id.hex()))

def send_custom_data(from_addr, to_addr, data, gas_limit, gas_gwei, key, nonce=None, eth_value=0):
	to_addr = web3.Web3.toChecksumAddress(to_addr)
	from_addr = web3.Web3.toChecksumAddress(from_addr)
	# nonce = w.eth.getTransactionCount(from_addr)
	if nonce!= None:
		print ('Nonce (ALREADY SET): {0}'.format(nonce))
	else:
		nonce = w.eth.getTransactionCount(from_addr)
		print ('Nonce (OBTAINED LIVE): {0}'.format(nonce))
	transaction = {
		'to': to_addr,
		'from': from_addr,
		'value': int(eth_value*(10**18)), # ETH DECIMAL is 18
		'gas': gas_limit,
		'gasPrice':int(gas_gwei*(10**9)),
		# 'gasPrice':int(gas_price, 16), # gas price comes as a hex value which was already multiplied by 10**9
		'chainId':1,
		'nonce': nonce,
		'data': data
	}
	# attempt to sign and send transaction
	while True:
		try:
			signed_transaction = w.eth.account.signTransaction(transaction, key)
			transaction_id = w.eth.sendRawTransaction(signed_transaction.rawTransaction)
			key = 'base64'
			break
		except Exception as e:
			print ('['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] Error occured: {0}\t TRYING AGAIN...'.format(str(e)))
	print ('\n['+ time.strftime("%Y-%m-%d %I:%M:%S %p") +'] ETH sent. ID = https://etherscan.io/tx/{0}'.format(transaction_id.hex()))
