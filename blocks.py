import csv

class Transaction:
    def __init__(self, tx_id, fee, weight, parentTxIds):
        self.tx_id = tx_id
        self.fee = fee
        self.weight = weight
        self.parentTxIds = parentTxIds

class Block:
    def __init__(self):
        self.transactions = []
        self.tx_ids = []
    
    def totalWeightOfBlock(self):
        weight = 0
        for tx in self.transactions:
            weight = weight + tx.weight
        return weight

    def areParentTxAvailable(self,parentTxIds):
        if(self.tx_ids.__len__() == 0):
            return True
        else:
            areAvailable = True
            for id in parentTxIds:
                if(self.tx_ids.__contains__(id)):
                    continue
                else:
                    areAvailable = False
                    break
            return areAvailable

    
    def addToBlock(self, tx):
        temp_weight = self.totalWeightOfBlock() + tx.weight
        if(temp_weight >= 4000000):
            return
        elif(tx.parentTxIds == ['']):
            self.tx_ids.append(tx.tx_id)
            self.transactions.append(tx)
        else:
            parentsAvailable = self.areParentTxAvailable(tx.parentTxIds)
            if(parentsAvailable):
                self.tx_ids.append(tx.tx_id)
                self.transactions.append(tx)
            else:
                return

extractedTransactions = []

with open('mempool.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue
        tx = Transaction(row["tx_id"],int(row["fee"]),int(row["weight"]),row['parents '].split(';'))
        extractedTransactions.append(tx)
        line_count += 1

extractedTransactions.sort(key=lambda x:x.fee,reverse=True)
block = Block()

for tx in extractedTransactions:
    block.addToBlock(tx)

with open('block.txt', mode='w') as out_file:
    for id in block.tx_ids:
        out_file.write(id)
        out_file.write('\n')