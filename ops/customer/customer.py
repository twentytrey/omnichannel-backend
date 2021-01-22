# from .db_con import createcon
# from db_con import createcon
import psycopg2
# con,cursor=createcon('retail','jmso','localhost','5432')
from ops.connector.connector import evcon
con,cursor=evcon()

import pandas as pd
import numpy as np
import os,re
from ops import CurrencyHelper,humanize_date,timestamp_forever,timestamp_now

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class CC:
    def __init__(self):
        pass
    
    def get(self):
        cursor.execute("select users_id from userreg where logonid='Cash Customer';")
        res=cursor.fetchone()
        if res==None:return dict(customer_id=None,customer_name=None)
        elif res!=None:return dict(customer_id=res[0],customer_name="Cash Customer")
