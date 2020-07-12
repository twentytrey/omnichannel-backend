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

class PrepareOrder:
    def __init__(self,creator_id,store_id,ra_id,vendor_id):
        self.creator_id=creator_id
        self.store_id=store_id
        self.ra_id=ra_id
        self.vendor_id=vendor_id
        self.supplyingstore_id=self.vendorstore(vendor_id)
    
    def vendorstore(self,vendor_id):
        cursor.execute("select storeent_id from storeent where member_id=%s",(vendor_id,))
        return cursor.fetchone()[0]
