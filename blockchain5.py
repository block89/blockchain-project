# initializing blockchain list
from functools import reduce
import hashlib as hl
import json
from collections import OrderedDict
from hash_util import hash_string_256, hash_block

MINING_REWARD = 10
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}

blockchain = [genesis_block]
open_transactions = []
owner = 'M'
participants = {'M'}

def valid_proof(transactions, last_hash, proof):
    guess = str(transactions) + str(last_hash) + str(proof).encode()
    guess_hash = hl.sha256(guess).hexdigest()
    print(guess_hash)
    return guess_hash[0:2] == '00'

def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof

#def hash_block(block):
   # return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
    #'-'.join([str(block[key]) for key in block])

def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']for tx in open_transactions if tx['sender'] == participant]
    
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + tx_amt[0] if len(tx_amt) > 0 else 0, tx_sender, 0)
    
    
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = reduce(lambda tx_sum, tx_amt: tx_sum + tx_amt[0] if len(tx_amt) > 0 else 0, tx_recipient, 0)

    return amount_recieved - amount_sent

def get_last_blockchain_value():
    """ returns the last value of the current blockchain."""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']
    
def add_transaction(recipient, sender=owner, amount=1.0):
    """append a new value as well as the last blockchain value to the blockchain
    Argument :
        :sender: the sender of Coins 
        :recipient: recipient of the Coins 
        :amount: the amount of coins sent in transaction

    """  
 #   transaction = {
 #       'sender': sender, 
 #       'recipient': recipient,
 #       'amount': amount
 #   }
    transaction = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)])
    
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False

    #blockchain.append([last_transaction, transaction_amount])

def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
#    reward_transaction = {
#        'sender': 'MINING',
#        'recipient': owner,
#        'amount': MINING_REWARD
#    }
    reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
   
   
    copied_transaction = open_transactions[:]
    copied_transaction.append(reward_transaction)
    
    #for key in last_block:
    #    value = last_block[key]
    #    hashed_block = hashed_block + str(value)
    
    block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': copied_transaction,
        'proof': proof
    }
    blockchain.append(block)
    return True

def get_transaction_value():
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return tx_recipient, tx_amount

def get_user_choice():
    user_input = input('Your choice: ')
    return user_input

def print_blockchain_elements():
    #Outout the blockchain to console
    for block in blockchain:
        print('Outputting Block') 
        print(block)
    else:
        print('-' *20)

def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
           continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work is invalid!')
            return False
    return True  
  
waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output blockchain blocks')
    print('4: Output participants')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == 1:
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print(open_transactions)
    elif user_choice == 2:
        if mine_block():
            open_transactions = []
    elif user_choice == 3:
        print_blockchain_elements() 
    elif user_choice == 4:
        print(participants)
    
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Chris', 'recipient': 'Max', 'amount': 100.0}]
            }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Input was invalid')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
    print('Balance of {}: {:6.2f}'.format('M',get_balance('M')))
else:
    print('User left!')

print('Done!')