import pandas as pd
import numpy as np
import os
# from .db_con import createcon
# from db_con import createcon
import psycopg2
# con,cursor=createcon('retail','jmso','localhost','5432')
from ops.connector.connector import evcon
con,cursor=evcon()

from random import normalvariate

def itemsoninventory(store_id):
    cursor.execute("select catentry_id from inventory where store_id=%s",(store_id,))
    res=cursor.fetchall();return [x for (x,) in res]

def getcatentries(mid):
    cursor.execute("select catentry_id from catentry where member_id=%s",(mid,))
    return [x for (x,) in cursor.fetchall()]

def vendors():
    cursor.execute("select vendor_id from vendor")
    return [x for (x,) in cursor.fetchall()]

def raids(store_id):
    cursor.execute("select ra_id from ra where store_id=%s",(store_id,))
    return [x for (x,) in cursor.fetchall()]

def getitemspc(cat_id):
    cursor.execute("select itemspc_id from catentry where catentry_id=%s",(cat_id,))
    return cursor.fetchone()[0]

def getffm(mid):
    cursor.execute("select ffmcenter_id from ffmcenter where member_id=%s",(mid,))
    return cursor.fetchone()[0]

def getname(cat_id):
    cursor.execute("select name from catentdesc where catentry_id=%s",(cat_id,))
    return cursor.fetchone()[0]

def getcatalog(cat_id,member_id):
    cursor.execute("""select catalog.identifier from catalog inner join catgpenrel on 
    catalog.catalog_id=catgpenrel.catalog_id where catgpenrel.catentry_id=%s and catalog.
    member_id=%s""",(cat_id,member_id,));return cursor.fetchone()[0]

def getprice(cat_id):
    cursor.execute("select listprice::float from listprice where catentry_id=%s",(cat_id,))
    return cursor.fetchone()[0]

def normal_choice(lst,mean=None,stddev=None):
    if mean==None:
        mean=(len(lst)-1)/2
    if stddev==None:
        stddev=len(lst)/6
    while True:
        index=int(normalvariate(mean,stddev)+0.5)
        if 0<=index < len(lst):
            return lst[index]

