# from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
# con,cursor=createcon("retail","jmso","localhost","5432")
from ops.connector.connector import evcon
con,cursor=evcon()

import  importlib
import pandas as pd
import numpy as np
import datetime
from ops.helpers.functions import timestamp_now,timestamp_forever,datetimestamp_now,datetimestamp_forever,defaultlanguage,CurrencyHelper
from ops.calculations.discountcalculations import DiscountCalculations
from ops.calculations.shippingmethods import ShippingMethods
from ops.inventory.inventory import InventoryItem

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class OrderItem:
    def __init__(self,catentry_id,language_id,store_id,customer_id,owner_id,timeplaced,costprice,quantity=1,buschn_id=7):
        self.catentry_id=catentry_id
        self.language_id=language_id
        self.store_id=store_id
        self.customer_id=customer_id
        self.owner_id=owner_id
        self.buschn_id=buschn_id
        self.quantity=quantity
        self.timeplaced=timeplaced
        self.costprice=costprice
        iitem=InventoryItem(catentry_id,language_id,store_id,customer_id,owner_id,quantity)
        contract_id=iitem.price["contract_id"]
        offer_id=iitem.price["offer_id"]
        price=iitem.price["price"]
        currency=iitem.price["currency"]
        
        totaladjustment=iitem.totaladjustment
        itemspc_id=iitem.itemspc_id
        partnumber=iitem.partnumber
        totalproduct=quantity*price
        self.logonid=self.identity()
        ffmcenter_id,address_id=None,None
        if self.logonid !=None and self.logonid !="Cash Customer":
            shippingmethod=ShippingMethods(store_id,customer_id,totalproduct)
            ffmcenter_id=shippingmethod.ffmcenter_id
            address_id=shippingmethod.address_id
        
        self.data=dict(storeent_id=self.store_id,orders_id=None,termcond_id=None,trading_id=contract_id,
        itemspc_id=itemspc_id,catentry_id=catentry_id,partnum=partnumber,ffmcenter_id=ffmcenter_id,
        member_id=customer_id,address_id=address_id,price=price,status="1",inventorystatus="ALLC",
        lastcreate=timeplaced,lastupdate=timeplaced,fulfillmentstatus="INT",identity=self.logonid,
        offer_id=offer_id,currency=currency,totalproduct=totalproduct,quantity=quantity,
        totaladjustment=totaladjustment,owner_id=owner_id,buschn_id=buschn_id,costprice=costprice)
    
    def identity(self):
        cursor.execute("select logonid from userreg where users_id=%s",(self.customer_id,))
        res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
