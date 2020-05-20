from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","pronov","localhost","5432")
import  importlib
import pandas as pd
import numpy as np
import datetime
from ops.helpers.functions import timestamp_now,timestamp_forever,datetimestamp_now,datetimestamp_forever,defaultlanguage,CurrencyHelper
from ops.calculations.discountcalculations import DiscountCalculations

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

orderstatuses=[dict(value=1,text="Ordered"),dict(value=2,text="Invoiced"),dict(value=3,text="Shipped"),
dict(value=4,text="Backordered"),dict(value=5,text="Canceled"),dict(value=6,text="Refunded"),dict(value=7,text="Returned")]
ffmstatuses=[dict(value="INT",text="Not Yet Released"),dict(value="OUT",text="Released for Fulfillment"),
dict(value="SHIP",text="Shipment Confirmed"),dict(value="HOLD",text="Held, Waiting for Release")]

class CartItem:
    def __init__(self,catentry_id,store_id,customer_id,quantity,employer=None):
        self.catentry_id=catentry_id
        self.quantity=quantity
        self.storeent_id=store_id
        self.member_id=customer_id
        self.orgentity_id=employer
        now=datetime.datetime.now()
        self.trading_id=None;self.default_trading_id=None

        if self.orgentity_id!=None:self.trading_id=self.member_has_trading(self.orgentity_id)
        elif self.orgentity_id==None:self.trading_id=self.member_has_trading(self.member_id)

        self.default_trading_id=self.get_default_trading()
        self.defaulttrading_starttime,self.defaulttrading_endtime=self.trading_span(self.trading_id)
        self.activedefaulttrade=self.defaulttrading_starttime < now and self.defaulttrading_endtime > now
        self.inactivedefaulttrade=self.defaulttrading_starttime > now or self.defaulttrading_endtime < now
        self.tdpos=None
        if self.activedefaulttrade:
            self.tdpos=self.selectpos(self.tradingpositions(self.default_trading_id,self.catentry_id))

        if self.trading_id != None:
            self.trading_starttime,self.trading_endtime=self.trading_span(self.trading_id)
            self.activetrade=self.trading_starttime < now and self.trading_endtime > now
            self.inactivetrade=self.trading_starttime > now or self.trading_endtime < now
            if self.activetrade:
                self.tdpos=self.selectpos(self.tradingpositions(self.trading_id,self.catentry_id))
        
        self.ffmcenter=self.getffmcenter(self.catentry_id)
        self.address_id=self.getaddress()
        self.price=self.tdpos["price"]
        self.orderstatus=1
        allocable=self.qtyallocable()
        if allocable != None and allocable > 0:self.inventorystatus='ALLC'
        self.lastcreate=datetimestamp_now()
        self.lastupdate=datetimestamp_now()
        self.fulfillmentstatus="INT"
        self.lastallocupdate=datetimestamp_now()
        self.currency=self.tdpos["currency"]
        self.totalproduct=self.price*self.quantity
        self.catgroup_id=self.getcatgroup()
        self.trading=None
        
        self.trading_item_discount=None
        if self.default_trading_id!=None:
            self.trading=self.default_trading_id
            trading_item_discount=self.getcatentrydiscount(self.default_trading_id)
            category_discount=self.getcategorydiscount()
            if trading_item_discount!=None and category_discount!=None:self.trading_item_discount=trading_item_discount
            elif trading_item_discount!=None and category_discount==None:self.trading_item_discount=trading_item_discount
            elif trading_item_discount==None and category_discount!=None:self.trading_item_discount=category_discount

        if self.trading_id!=None:
            self.trading=self.trading_id
            trading_item_discount=self.getcatentrydiscount(self.trading_id)
            category_discount=self.getcategorydiscount()
            if trading_item_discount!=None and category_discount!=None:self.trading_item_discount=trading_item_discount
            elif trading_item_discount!=None and category_discount==None:self.trading_item_discount=trading_item_discount
            elif trading_item_discount==None and category_discount!=None:self.trading_item_discount=category_discount
        
        d=DiscountCalculations(self.trading_item_discount,self.catentry_id,self.price,self.quantity,self.storeent_id)
        self.totaladjustment=d._execute()
    
    def member_has_trading(self,mid):
        cursor.execute("select trading_id from participnt where member_id=%s",(mid,))
        res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def trading_span(self,trading_id):
        cursor.execute("select starttime,endtime from trading where trading_id=%s;",
        (trading_id,));res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res
    
    def get_default_trading(self):
        cursor.execute("select contract_id from contract where usage=0")
        res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def tradingpositions(self,contract_id,catentry_id):
        cursor.execute("""select offerprice.currency,offerprice.price::float,tradeposcn.name,
        contract.name from offerprice inner join offer on offerprice.offer_id=offer.offer_id 
        inner join tradeposcn on offer.tradeposcn_id=tradeposcn.tradeposcn_id inner join tdpscncntr 
        on tradeposcn.tradeposcn_id=tdpscncntr.tradeposcn_id inner join contract on tdpscncntr.
        contract_id=contract.contract_id where tdpscncntr.contract_id=%s and offer.catentry_id=%s;""",
        (contract_id,catentry_id,));res=cursor.fetchall()
        if len(res) <= 0:return None
        elif len(res) > 0:return [dict(currency=r[0],price=r[1],offername=r[2],basis=r[3])for r in res]
    
    def selectpos(self,data):
        for pos in data:
            if pos["offername"]=="Custom Price":return pos
            else:return pos
    
    def getffmcenter(self,catentry_id):
        cursor.execute("select ffmcenter_id from inventory where catentry_id=%s",
        (catentry_id,));res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]

    def getaddress(self):
        cursor.execute("select address_id from address where member_id=%s",
        (self.member_id,));res=cursor.fetchone()
        if res!=None:return res[0]
        elif res==None:return None
    
    def qtyallocable(self):
        cursor.execute("""select qtyonhand,qtyinprocess from receipt where versionspc_id=%s order by
        receipt_id desc limit 1""",(self.catentry_id,));res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res[0]-res[1]

    def getcatgroup(self):
        cursor.execute("select catgroup_id from catgpenrel where catentry_id=%s",
        (self.catentry_id,));res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res[0]

    def getcategorydiscount(self):
        cursor.execute("""select calcode_id from catgpcalcd where store_id=%s and trading_id=%s and 
        catgroup_id=%s""",(self.storeent_id,self.trading_id,self.catgroup_id,));res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def getcatentrydiscount(self,trading_id):
        cursor.execute("""select calcode_id from catencalcd where store_id=%s and trading_id=%s
        and catentry_id=%s""",(self.storeent_id,trading_id,self.catentry_id,))
        res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res[0]
