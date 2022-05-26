from flask import Flask, jsonify, request
from uuid import uuid4
import hashlib
import json
from time import time

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        
        # Create the genesis block
        self.new_block(previous_hash = '1', proof = 100)

    def new_block(self, proof, previous_hash = None):
        # Create a new Block nd adds it to the chain
        """
        Create a new Block in the blockchain
        :param proof:            <int> The proof given by the Proof of Work algorithm
        :param previous_hash:    <str> Hash of the previous block (Optional)
        :return:                 <dict> New block
        """
        block = {
            'index'         : len(self.chain) + 1,
            'timestamp'     : time(),
            'transaction'   : self.pending_transactions,
            'proof'         : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1])
        }
        
        # Reset the current list of transactions
        self.pending_transaction = []
        
        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of transactions
        """
        Creates a new transaction to go into the next mined block
        :param sender:       <str> Address of the Sender
        :param receipient:   <str> Address of the Receipient
        :param amount:       <int> Amount
        :return:             <int> The index of the Block that will hold this transaction
        """
        self.pending_transaction.append({
            "sender"    : sender,
            "recipient" : recipient,
            "amount"    : amount
        })
        
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # Hashes a block
        """
        Creates a Sha256 hash of a Block
        :param block:   <dict> Block
        :return:        <str>        
        """
        
        # We must make sure that the Dictionary is ordered, or we will have inconsistent hashes
        block_string = json.dumps(block, sort_keys= True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @staticmethod
    def proof_of_work(block):
        """
        Proof_of_Work algorithm.
        Iterate the "proof" field until the conditions are satisfied
        :param block:  <dict>
        """
        while not Blockchain.valid_proof(block):
            block["proof"] += 1
            
    @staticmethod
    def valid_proof(block):
        """
        The Proof_of_Work conditions.
        Check if the hash of the block starts with 4 zeros.
        Higher difficulty == more zeros, lower difficulty == less.
        :param block:   <dict>
        """
        return Blockchain.hash(block)[:4] == "0000"

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]


if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.proof_of_work(blockchain.last_block)
    print(blockchain.hash(blockchain.last_block))
