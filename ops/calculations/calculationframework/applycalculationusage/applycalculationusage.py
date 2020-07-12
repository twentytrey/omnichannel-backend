# from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
# con,cursor=createcon("retail","jmso","localhost","5432")
from ops.connector.connector import evcon
con,cursor=evcon()


class applycalculationusage:
    def __init__(self,calcode_id,catentry_id,price,quantity,store_id,combineclass,calculateclass,rulecombine,codeapplyclass,
    summarizeclass,finalizeclass):
        print( """applycalculationusage""" )
        c=combineclass(calcode_id,catentry_id,price,quantity)
        self.catentry_id=c.catentry_id
        self.calcode_id=c.calcode_id
        self.price=price
        self.quantity=quantity
        self.store_id=store_id
        self.deductible=calculateclass(catentry_id,calcode_id,price,quantity,store_id,rulecombine)._execute()
        self.amount=codeapplyclass(self.deductible)._execute()
        summarizeclass(self.amount,self.quantity)._execute()
        finalizeclass()
