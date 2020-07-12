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

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

orderstatuses=[dict(value=1,text="Ordered"),dict(value=2,text="Invoiced"),dict(value=3,text="Shipped"),
dict(value=4,text="Backordered"),dict(value=5,text="Canceled"),dict(value=6,text="Refunded"),dict(value=7,text="Returned")]
ffmstatuses=[dict(value="INT",text="Not Yet Released"),dict(value="OUT",text="Released for Fulfillment"),
dict(value="SHIP",text="Shipment Confirmed"),dict(value="HOLD",text="Held, Waiting for Release")]
