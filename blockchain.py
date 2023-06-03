import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain :
    def __init__(self):
        self.chain = []
        self.transaction = 0
        self.create_block(nounce=1,prev_hash="0")

    def create_block(self,nounce,prev_hash):
        block={
            "index":len(self.chain) + 1,
            "timestamp":str(datetime.datetime.now()),
            "nounce":nounce,
            "data":self.transaction,
            "prev_hash":prev_hash,
        }
        self.chain.append(block)
        return block
    
    def get_prev_block(self):
        return self.chain[-1]
    
    def hash(self,block):
        encode_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()
    
    def proof_of_work(self,prev_nounce):
        new_nounce=1 
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_nounce**2 - prev_nounce**2).encode()).hexdigest()
            if hash_operation[:4] == "0000" :
                check_proof = True
            else : 
                new_nounce +=1
        return new_nounce
    
    def is_chain_valid(self,chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            prev_nounce = prev_block['nounce']
            nounce = block['nounce']
            hash_operation = hashlib.sha256(str(nounce**2 - prev_nounce**2).encode()).hexdigest()

            if hash_operation[:4] != "0000":
                return False
            prev_block = block
            block_index += 1
        return True

#web server
app = Flask(__name__)

blockchain = Blockchain()

#routing
@app.route('/')
def hello():
    return "<p>hello world</p>"

@app.route('/get_chain')
def get_chain():
    response={
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response),200

@app.route('/mining',methods=["GET"])
def mining_block():
    amount = 1000000
    blockchain.transaction = blockchain.transaction+amount
    #pow
    prev_block = blockchain.get_prev_block()
    prev_nounce = prev_block['nounce']
    #nounce
    nounce = blockchain.proof_of_work(prev_nounce)
    #prev hash block
    prev_hash = blockchain.hash(prev_block)
    #unpdate new block
    block = blockchain.create_block(nounce, prev_hash)
    response = {
        "message" : "mining complete",
        "index" : block["index"],
        "nounce": block['nounce'],
        "timestamp": block['timestamp'],
    }
    return jsonify(response),200

@app.route('/is_valid',methods=['GET'])
def is_valid():
    is_chain_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_chain_valid:
        response = {"message":"chain is valid."}
    else : response = {"message": "chain is not valid."}
    return jsonify(response),200

if __name__ == "__main__":
    app.run(debug=True)

