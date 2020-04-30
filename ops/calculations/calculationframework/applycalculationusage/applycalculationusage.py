# from .db_con import createcon
from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","jmso","localhost","5432")

class applycalculationusage:
    def __init__(self,combinationclass,calusage_id,catentry_id,calcode_id,store_id,trading_id):
        print( """applycalculationusage""" )
        self.combinationclass=combinationclass
        self.calusage_id=calusage_id
        self.catentry_id=catentry_id
        self.calcode_id=calcode_id
        self.store_id=store_id
        self.trading_id=trading_id
        self._execute()
    
    def _execute(self):
        self.combinationclass(self.calusage_id,self.catentry_id,self.calcode_id,self.store_id,self.trading_id)
