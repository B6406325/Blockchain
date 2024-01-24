import datetime
class Blockchain:
    def __init__(self):
        #เก็บกลุ่มของ block
        self.chain = [] #list ที่เก็บ block
        #genesis block
        self.create_block(nonce=1,previous_hash="0")
        
    #สร้าง block ขึ้นมาในระบบ blockchain
    def create_block(self,nonce,previous_hash):
        #เก็บส่วนประกอบของ block แต่ละ block
        block={
            "index":len(self.chain)+1,
            "timestamp":str(datetime.datetime.now()),
            "nonce":nonce,
            "previous_hash":previous_hash
        }
        self.chain.append(block)
        return block
    
#ใช้งาน blockchain
blockchain = Blockchain()
print(blockchain.chain)