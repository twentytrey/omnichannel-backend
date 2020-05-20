from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","jmso","localhost","5432")
import  importlib
import pandas as pd
import numpy as np
from ops import textualize_datetime,CurrencyHelper

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class CreditAccountEntryMethod:
    def __init__(self,member_id,faccountname,amount,setccurr,typecode,timecreated,memo,op='C'):
        self.member_id=member_id
        self.faccountname=faccountname
        self.amount=amount
        self.setccurr=setccurr
        self.typecode=typecode
        self.timecreated=timecreated
        self.memo=memo
        self.op=op
    
    def _execute(self):
        pass