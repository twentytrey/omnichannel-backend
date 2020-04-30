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

class Offer:
    def __init__(self,tradeposcn_id,catentry_id,enddate=None,precedence=0,published=0,lastupdate=None,
    minimumquantity=None,qtyunit_id=None,maximumquantity=None,field1=None,field2=None,flags=1,
    identifier=None,startdate=None):
        self.tradeposcn_id=tradeposcn_id
        self.catentry_id=catentry_id
        self.enddate=enddate
        self.precedence=precedence
        self.published=published
        self.lastupdate=lastupdate
        self.minimumquantity=minimumquantity
        self.qtyunit_id=qtyunit_id
        self.maximumquantity=maximumquantity
        self.field1=field1
        self.field2=field2
        self.flags=flags
        self.identifier=identifier
        self.startdate=startdate
    
    @staticmethod
    def offerforitem(catentry_id,tradeposcn_id):
        cursor.execute("""with offer as (select tradeposcn.type,offer.offer_id from offer inner join tradeposcn
        on tradeposcn.tradeposcn_id=offer.tradeposcn_id where offer.catentry_id=%s and offer.tradeposcn_id=%s)
        select offer.type,offer.offer_id,offerprice.price::float,offerprice.currency from offer inner join offerprice on
        offer.offer_id=offerprice.offer_id""",(catentry_id,tradeposcn_id,));res=cursor.fetchone()
        if res==None:return dict(offer_id=None,offer=None,offercurrency=None,custom_offer_id=None,custom=None,customcurrency=None)
        elif res != None:
            if res[0]=='S':return dict(offer_id=res[1],offer=res[2],offercurrency=res[3])
            elif res[0]=='C':return dict(custom_offer_id=res[1],custom=res[2],customcurrency=res[3])
    
    def save(self):
        try:
            cursor.execute("""insert into offer(startdate,tradeposcn_id,catentry_id,enddate,precedence,published,
            lastupdate,minimumquantity,qtyunit_id,maximumquantity,field1,field2,flags,identifier)values(%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(catentry_id,tradeposcn_id)do update set
            startdate=%s,tradeposcn_id=%s,catentry_id=%s,enddate=%s,precedence=%s,published=%s,lastupdate=%s,
            minimumquantity=%s,qtyunit_id=%s,maximumquantity=%s,field1=%s,field2=%s,flags=%s,identifier=%s
            returning offer_id""",(self.startdate,self.tradeposcn_id,self.catentry_id,self.enddate,self.precedence,
            self.published,self.lastupdate,self.minimumquantity,self.qtyunit_id,self.maximumquantity,self.field1,
            self.field2,self.flags,self.identifier,self.startdate,self.tradeposcn_id,self.catentry_id,self.enddate,
            self.precedence,self.published,self.lastupdate,self.minimumquantity,self.qtyunit_id,self.maximumquantity,
            self.field1,self.field2,self.flags,self.identifier,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

print(Offer.offerforitem(9,13))

class Offerdesc:
    def __init__(self,offer_id,language_id,description=None):
        self.offer_id=offer_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into offerdesc(offer_id,language_id,description)values(%s,%s,%s)
            on conflict(offer_id,language_id)do update set offer_id=%s,language_id=%s,description=%s
            returning offer_id""",(self.offer_id,self.language_id,self.description,self.offer_id,
            self.language_id,self.description,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Offerprice:
    def __init__(self,offer_id,currency,price,compareprice=None):
        self.offer_id=offer_id
        self.currency=currency
        self.price=price
        self.compareprice=compareprice
    
    def save(self):
        try:
            cursor.execute("""insert into offerprice(offer_id,currency,price,compareprice)values(%s,%s,%s,%s)
            on conflict(offer_id,currency)do update set offer_id=%s,currency=%s,price=%s,compareprice=%s
            returning offer_id""",(self.offer_id,self.currency,self.price,self.compareprice,self.offer_id,
            self.currency,self.price,self.compareprice,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Mgptrdpscn:
    def __init__(self,mbrgrp_id,tradeposcn_id):
        self.mbrgrp_id=mbrgrp_id
        self.tradeposcn_id=tradeposcn_id
    
    def save(self):
        try:
            cursor.execute("""insert into mgptrdpscn(mbrgrp_id,tradeposcn_id)values(%s,%s)
            on conflict(mbrgrp_id,tradeposcn_id)do update set mbrgrp_id=%s,tradeposcn_id=%s
            returning mbrgrp_id""",(self.mbrgrp_id,self.tradeposcn_id,self.mbrgrp_id,self.tradeposcn_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordioffer:
    def __init__(self,offer_id,orderitems_id):
        self.offer_id=offer_id
        self.orderitems_id=orderitems_id
    
    def save(self):
        try:
            cursor.execute("""insert into ordioffer(offer_id,orderitems_id)values(%s,%s)
            on conflict(orderitems_id,offer_id)do update set offer_id=%s,orderitems_id=%s returning
            orderitems_id""",(self.offer_id,self.orderitems_id,self.offer_id,self.orderitems_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

