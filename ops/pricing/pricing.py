from .db_con import createcon
# from db_con import createcon
import psycopg2
con,cursor=createcon('retail','jmso','localhost','5432')
import pandas as pd
import numpy as np
import os,re
from ops import CurrencyHelper,humanize_date,timestamp_forever,timestamp_now

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Storetpc:
    def __init__(self,storeent_id,tradeposcn_id,sttpcusg_id=None):
        self.storeent_id=storeent_id
        self.tradeposcn_id=tradeposcn_id
        self.sttpcusg_id=sttpcusg_id
    
    def save(self):
        try:
            cursor.execute("""insert into storetpc(storeent_id,tradeposcn_id,sttpcusg_id)values(%s,%s,%s)
            on conflict(storeent_id,tradeposcn_id)do update set storeent_id=%s,tradeposcn_id=%s,sttpcusg_id=%s
            returning tradeposcn_id""",(self.storeent_id,self.tradeposcn_id,self.sttpcusg_id,
            self.storeent_id,self.tradeposcn_id,self.sttpcusg_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Sttpcusg:
    def __init__(self,sttpcusg_id,identifier,description=None):
        self.sttpcusg_id=sttpcusg_id
        self.identifier=identifier
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into sttpcusg(sttpcusg_id,identifier,description)values(%s,%s,%s)
            on conflict(sttpcusg_id)do update set sttpcusg_id=%s,identifier=%s,description=%s
            returning sttpcusg_id""",(self.sttpcusg_id,self.identifier,self.description,
            self.sttpcusg_id,self.identifier,self.description,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

