# Ethereum-Transactions-Using-Web3
This repository shows how you can make transactions on Ethereum blockchain using web3. 

# How to use
Install web3   
`pip install web3`

Install ethtoken  
`pip install ethtoken`   

Add make_transactions.py to your working directory and import it   
`import make_transactions`   

Methods:   
1. approve: Call this method to approve your sender to make transaction (Approve only trusted APPs). It will make transaction on blockchain for the same.    
2. send_token: Call this method to send ERC20 token from one address to another address. A transaction on Ethereum blockchain will be made for it.   
3. send_eth: Call this method to send ETH to destination address. A transaction on Ethereum blockchain will be mmade to send ETH to destination address
4. send_custom_data: This method will allow you to send custom data with your transaction. 
5. get_all_balances: This function can be used to get balance of all tokens on address passed as parameter

# Example
An example usage of *make_transactions* is given in Example folder.   
In example, an address will be taken from telegram account and tokens are sent on that address. To use it, you need to configure telegram details and your account details in ***settings.ini***
