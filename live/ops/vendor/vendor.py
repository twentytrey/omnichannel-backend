from .db_con import createcon
# from db_con import createcon
import psycopg2
con,cursor=createcon('retail','pronov','localhost','5432')
import pandas as pd
import numpy as np
import os,re
from ops import CurrencyHelper,humanize_date,timestamp_forever,timestamp_now

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Vendor:
    def __init__(self,vendor_id,buyer_id=None,lastupdate=None,markfordelete=0,vendorname=None):
        self.vendor_id=vendor_id
        self.buyer_id=buyer_id
        self.lastupdate=timestamp_now()
        self.markfordelete=markfordelete
        self.vendorname=vendorname
    
    def save(self):
        try:
            cursor.execute("""insert into vendor(vendor_id,buyer_id,lastupdate,markfordelete,vendorname)
            values(%s,%s,%s,%s,%s)on conflict(vendor_id)do update set vendor_id=%s,buyer_id=%s,lastupdate=%s,
            markfordelete=%s,vendorname=%s returning vendor_id""",(self.vendor_id,self.buyer_id,self.lastupdate,
            self.markfordelete,self.vendorname,self.vendor_id,self.buyer_id,self.lastupdate,self.markfordelete,
            self.vendorname,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Vendordesc:
    def __init__(self,vendor_id,language_id,description,lastupdate):
        self.vendor_id=vendor_id
        self.language_id=language_id
        self.description=description
        self.lastupdate=timestamp_now()
    
    def save(self):
        try:
            cursor.execute("""insert into vendordesc(vendor_id,language_id,description,lastupdate)
            values(%s,%s,%s,%s)on conflict(vendor_id,language_id)do update set vendor_id=%s,language_id=%s,
            description=%s,lastupdate=%s returning vendor_id""",(self.vendor_id,self.language_id,self.description,
            self.lastupdate,self.vendor_id,self.language_id,self.description,self.lastupdate,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
