from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","pronov","localhost","5432")

class summarizecalculationusage:
    def __init__(self,amount,quantity):
        print("""summarizecalculationusage""")
        self.amount=amount
        self.quantity=quantity
    
    def _execute(self):
        return self.amount*self.quantity


