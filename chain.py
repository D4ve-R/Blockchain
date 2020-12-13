import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.new_block(prev_hash = 1, proof = 100)


    def new_block(self, proof, prev_hash = None):
        block = {
                'index': len(self.chain) + 1,
                'timestamp': time(),
                'transactions': self.transactions,
                'proof': proof,
                'previous_hash': prev_hash or self.hash(self.chain[-1]),
                }
        self.transactions = []
        self.chain.append(block)
        return block

    def new_trans(self, send, reci, amo):
        self.transactions.append({
            'sender': send,
            'recipient': reci,
            'amount': amo,
        })
        return self.last_block['index'] + 1

    def p_o_w(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @property 
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()
         
    @staticmethod
    def valid_proof(last_proof, proof):
        approx = f'{last_proof}{proof}'.encode()
        approx_hash = hashlib.sha256(approx).hexdigest()
        return approx_hash[:4] == "0000"




app = Flask(__name__)

node_ident = str(uuid4()).replace('-', '')

mychain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = mychain.last_block
    last_proof = last_block['proof']
    proof = mychain.p_o_w(last_proof)

    mychain.new_trans(send="0", reci=node_ident, amo=1)
    previos_hash = mychain.hash(last_block)
    block = mychain.new_block(proof)

    response = {
            'message': "Mined New Block...",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
            }
    return jsonify(response), 200

@app.route('/transaction/new', methods=['POST'])
def new_trans():
    values = request.get_json()
    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    index = mychain.new_trans(values['sender'], values ['recipient'], values['amount'])

    response = {'message':f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods= ['GET'])
def full_chain():
    response = {
            'chain': mychain.chain,
            'length': len(mychain.chain),
            }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=6969)
