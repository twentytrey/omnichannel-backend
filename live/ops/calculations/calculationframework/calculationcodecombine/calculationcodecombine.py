# from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
# con,cursor=createcon("retail","jmso","localhost","5432")
from ops.connector.connector import evcon
con,cursor=evcon()


class calculationcodecombine:
    def __init__(self,calcode_id,catentry_id,price,quantity):
        print( """calculationcodecombine""" )
        self.calcode_id=calcode_id
        self.catentry_id=catentry_id
        self.price=price
        self.quantity=quantity


