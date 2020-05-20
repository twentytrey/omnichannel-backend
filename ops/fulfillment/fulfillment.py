from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","jmso","localhost","5432")
import  importlib
import pandas as pd
import numpy as np
from ops import textualize_datetime,humanize_date,CurrencyHelper

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Ffmcenter:
    def __init__(self,member_id,name=None,defaultshipoffset=86400,markfordelete=0,extffmstorenum=None,
    inventoryopflags=0,maxnumpick=25,pickdelayinmin=5,dropship='N'):
        self.member_id=member_id
        self.name=name
        self.defaultshipoffset=defaultshipoffset
        self.markfordelete=markfordelete
        self.extffmstorenum=extffmstorenum
        self.inventoryopflags=inventoryopflags
        self.maxnumpick=maxnumpick
        self.pickdelayinmin=pickdelayinmin
        self.dropship=dropship

    def save(self):
        try:
            cursor.excute("""insert into ffmcenter(member_id,name,defaultshipoffset,markfordelete,
            extffmstorenum,inventoryopflags,maxnumpick,pickdelayinmin,dropship)values(%s,%s,%s,%s,
            %s,%s,%s,%s,%s)on conflict(member_id,name)do update set member_id=%s,name=%s,defaultshipoffset=%s,
            markfordelete=%s,extffmstorenum=%s,inventoryopflags=%s,maxnumpick=%s,pickdelayinmin=%s dropship=%s
            returning ffmcenter_id""",(self.member_id,self.name,self.defaultshipoffset,self.markfordelete,
            self.extffmstorenum,self.inventoryopflags,self.maxnumpick,self.pickdelayinmin,self.dropship,
            self.member_id,self.name,self.defaultshipoffset,self.markfordelete,self.extffmstorenum,
            self.inventoryopflags,self.maxnumpick,self.pickdelayinmin,self.dropship,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ffmcentds:
    def __init__(self,ffmcenter_id,language_id,staddress_id=None,description=None,displayname=None):
        self.ffmcenter_id=ffmcenter_id
        self.language_id=language_id
        self.staddress_id=staddress_id
        self.description=description
        self.displayname=displayname
    
    def save(self):
        try:
            cursor.execute("""insert into ffmcentds(ffmcenter_id,language_id,staddress_id,description,
            displayname)values(%s,%s,%s,%s,%s)on conflict(ffmcenter_id,language_id)do update set 
            ffmcenter_id=%s,language_id=%s,staddress_id=%s,description=%s,displayname=%s returning 
            ffmcenter_id""",(self.ffmcenter_id,self.language_id,self.staddress_id,self.description,
            self.displayname,self.ffmcenter_id,self.language_id,self.staddress_id,self.description,
            self.displayname,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Inventory:
    def __init__(self,catentry_id,ffmcenter_id,store_id,quantity=0,quantitymeasure='C62',inventoryflags=0):
        self.catentry_id=catentry_id
        self.ffmcenter_id=ffmcenter_id
        self.store_id=store_id
        self.quantity=quantity
        self.quantitymeasure=quantitymeasure
        self.inventoryflags=inventoryflags
    
    @staticmethod
    def getitemquantity(catentry_id,store_id):
        cursor.execute("select quantity from inventory where store_id=%s and catentry_id=%s",
        (store_id,catentry_id,));res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    @staticmethod
    def update(qtyreceived,catentry_id,ffmcenter_id,store_id):
        try:
            cursor.execute("""select quantity from inventory where catentry_id=%s and ffmcenter_id=%s and
            store_id=%s""",(catentry_id,ffmcenter_id,store_id,))
            quantity=cursor.fetchone()[0];qtyonhand=quantity+qtyreceived
            cursor.execute("""update inventory set quantity=%s where catentry_id=%s and ffmcenter_id=%s and 
            store_id=%s""",(qtyonhand,catentry_id,ffmcenter_id,store_id,));con.commit();return qtyonhand
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    @staticmethod
    def read(language_id):
        cursor.execute("""select catentry.catenttype_id::text,catentdesc.name,catentdesc.fullimage,
        catentry.endofservicedate,ffmcenter.name,storeent.identifier,inventory.quantity from
        catentry left join catentdesc on catentry.catentry_id=catentdesc.catentry_id left
        join inventory on catentry.catentry_id=inventory.catentry_id left join ffmcenter on
        inventory.ffmcenter_id=ffmcenter.ffmcenter_id left join storeent on inventory.store_id=
        storeent.storeent_id where catentdesc.language_id=%s""",(language_id,))
        res=cursor.fetchall()
        if len(res)<=0:return [dict(type=None,item=None,image=None,expires=None,warehouse=None,
        store=None,quantity=None,)]
        elif len(res)>0:return [dict(type=r[0],item=r[1],image=r[2],expires=humanize_date(r[3]),
        warehouse=r[4],store=r[5],quantity=r[6]) for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into inventory(catentry_id,quantity,ffmcenter_id,store_id,quantitymeasure,
            inventoryflags)values(%s,%s,%s,%s,%s,%s)on conflict(catentry_id,ffmcenter_id,store_id)do update set
            catentry_id=%s,quantity=%s,ffmcenter_id=%s,store_id=%s,quantitymeasure=%s,inventoryflags=%s
            returning catentry_id""",(self.catentry_id,self.quantity,self.ffmcenter_id,self.store_id,self.quantitymeasure,
            self.inventoryflags,self.catentry_id,self.quantity,self.ffmcenter_id,self.store_id,self.quantitymeasure,self.inventoryflags,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

