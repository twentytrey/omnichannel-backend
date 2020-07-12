from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","pronov","localhost","5432")

class calculationcodecalculate:
    def __init__(self,catentry_id,calcode_id,price,quantity,store_id,rulecombine):
        print("""calculationcodecalculate""")
        self.catentry_id=catentry_id
        self.calcode_id=calcode_id
        self.price=price
        self.quantity=quantity
        self.store_id=store_id
        self.rulecombine=rulecombine
    
    def _execute(self):
        return self.rulecombine(self.calcode_id,self.catentry_id,self.price,self.quantity,self.store_id).returns

