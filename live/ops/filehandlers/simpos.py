import pandas as pd
import numpy as np
import os
from .db_con import createcon
# from db_con import createcon
import psycopg2
con,cursor=createcon('retail','pronov','localhost','5432')
from random import normalvariate

def getcatentries():
    cursor.execute("select catentry_id from catentry")
    return [x for (x,) in cursor.fetchall()]

def vendors():
    cursor.execute("select vendor_id from vendor")
    return [x for (x,) in cursor.fetchall()]

def raids():
    cursor.execute("select ra_id from ra")
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

def getcatalog(cat_id):
    cursor.execute("""select catalog.identifier from catalog inner join catgpenrel on catalog.catalog_id=
    catgpenrel.catalog_id where catgpenrel.catentry_id=%s""",(cat_id,))
    return cursor.fetchone()[0]

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

items=getcatentries()
juta_id=89
pronov_id=82
pronovstore_id=28
