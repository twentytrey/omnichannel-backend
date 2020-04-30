# from .db_con import createcon
from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","jmso","localhost","5432")

class calculationcodecombine:
    def __init__(self,calusage_id,catentry_id,calcode_id,store_id,trading_id):
        print( """calculationcodecombine""" )
        self.calusage_id=calusage_id
        self.catentry_id=catentry_id


