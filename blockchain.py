import datetime
import json
import hashlib
import random
from flask import Flask , jsonify
class Blockchain:
    def __init__(self):
        #เก็บกลุ่มของ block
        self.chain = [] #list ที่เก็บ block
        #genesis block
        self.create_block(nonce=1,previous_hash="0",id="B64xxxxx",name="suranaree",booktitle="eng5")
        
    #สร้าง block ขึ้นมาในระบบ blockchain
    def create_block(self,nonce,previous_hash,id,name,booktitle):
        #เก็บส่วนประกอบของ block แต่ละ block
        block={
            "index":len(self.chain)+1,
            "timestamp":str(datetime.datetime.now()),
            "nonce":nonce,
            "data": {
                "รหัสนักศึกษา": id,
                "ชื่อผู้ยืม": name,
                "ชื่อหนังสือ": booktitle,
                "วันที่คืน": str(datetime.datetime.now())
            },
            "previous_hash":previous_hash
        }
        block["hash"] = self.hash(block)
        self.chain.append(block)
        return block
    
    #ให้บริการเกี่ยวกับ Block ก่อนหน้า
    def get_previous_block(self):
        return self.chain[-1]
    
    #เข้ารหัส block
    def hash(self,block):
        #แปลง python object (dict) => json object
        encode_block = json.dumps(block,sort_keys=True).encode()
        #sha-256
        return hashlib.sha256(encode_block).hexdigest()
        
    def proof_of_work(self,previous_nonce):
        #อยากได้ค่า nonce = ??? ที่ส่งผลให้ได้ target hash => 4 หลักแรก => 0000xxxxxxxxx
        new_nonce = 1 #ค่า nonce ที่ต้องการ
        check_proof = False #ตัวแปรที่เช็คค่า nonce ให้ได้ตาม target ที่กำหนด
        
        #แก้โจทย์ทางคณิตศาสตร์
        while check_proof is False:
            #เลขฐาน 16 มา 1 ชุด
            hashopreration = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashopreration[:4] == "0000":
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce
    #ตรวจสอบ Block
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index<len(chain):
            block = chain[block_index] # block ที่ตรวจสอบ
            
            if block["previous_hash"] != self.hash(previous_block):
                return False
            
            previous_nonce = previous_block["nonce"] #nonce block ก่อนหน้า
            nonce = block["nonce"] #nonce ของ block ที่ตรวจสอบ
            hashopreration = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            
            if hashopreration[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True
    
    def make_chain_invalid(self):
    # Modify the hash of the last block to make it invalid
        modified_block = self.chain[3]
        modified_block["hash"] = "InvalidHash123"

        return "Chain modified successfully to make it invalid"
            
#web server
app = Flask(__name__)
#ใช้งาน blockchain
blockchain = Blockchain()

#routing
@app.route('/')
def hello():
    return "<h1>Hello Blockchain<h1>"

@app.route('/get_chain',methods=["GET"])
def get_chain():
    response={
        "chain":blockchain.chain,
        "length":len(blockchain.chain)
    }
    return jsonify(response),200
   
@app.route('/mining',methods=["GET"])
def mining_block():
    # Random values for demonstration purposes
    random_id = "B" + str(random.randint(100000, 999999))  # Example: B123456
    random_name = "User" + str(random.randint(1, 100))  # Example: User42
    random_booktitle = "Book" + str(random.randint(1, 50))  # Example: Book23

    #pow
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]
    #nonce
    nonce = blockchain.proof_of_work(previous_nonce)
    #hash block ก่อนหน้า
    previous_hash = blockchain.hash(previous_block)
    #update block ใหม่
    block = blockchain.create_block(nonce, previous_hash, id=random_id, name=random_name, booktitle=random_booktitle)
    response={
        "message": "Mining_Block เรียบร้อย",
        "index":block["index"],
        "timestamp":str(datetime.datetime.now()),
        "nonce":block["nonce"],
        "previous_hash":block["previous_hash"],
        "data": block["data"]  
    }
    return jsonify(response),200

@app.route('/check',methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response={"message":"Blockchain Valid"}
    else :
        response={"message":"Blockchain Is Not Valid"}
    return jsonify(response),200  

@app.route('/modified', methods=["GET"])
def make_invalid():
    result = blockchain.make_chain_invalid()

    if result.startswith("Chain modified"):
        response = {"message": result}
    else:
        response = {"error": result}

    return jsonify(response), 200 if result.startswith("Chain modified") else 400


if __name__ == "__main__":
    app.run()
