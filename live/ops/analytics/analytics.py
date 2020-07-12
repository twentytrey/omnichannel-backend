from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","pronov","localhost","5432")
import  importlib
import pandas as pd
import numpy as np
import datetime
from ops.helpers.functions import humanize_date,textualize_datetime,month

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class SalesByMonth:
    def __init__(self,year):
        self.year=year

    def records(self):
        cursor.execute("select totalproduct::float,lastcreate from orderitems where date_part('year',lastcreate)=%s",
        (self.year,));res=cursor.fetchall();data=None
        if len(res) >=0:
            data=[(r[1],r[0]) for r in res]
            df=pd.DataFrame(data,columns=["Date","Sales"])
            df=df.sort_values(by="Date")
            df['Month']=df['Date'].apply(month)
            monthlysales=df[['Month','Sales']]
            months=df['Month'].unique()
            rows=[m for m in months]
            cols=[ monthlysales.loc[monthlysales["Month"]==m]["Sales"].sum() for m in months ]
            return dict(rows=rows,cols=cols,text="Monthly sales for the year {}".format(self.year))
            
class SalesByJurisdiction:

    def getjurst(self,mid):
        cursor.execute("select city,state,country from address where member_id=%s",(mid,))
        city,state,country=cursor.fetchone()
        cursor.execute("select jurst_id from jurst where state=%s and country=%s",(state,country,))
        res=cursor.fetchall();jurstids=None;jurstgroupids=None
        if len(res) > 0:jurstids=[x for (x,) in res]
        elif len(res)<=0:jurstids=None
        cursor.execute("""select jurstgroup.description from jurstgroup inner join 
        jurstgprel on jurstgroup.jurstgroup_id=jurstgprel.jurstgroup_id where jurstgprel.jurst_id in %s and
        jurstgroup.subclass=1""",(tuple(jurstids),));res=cursor.fetchone()[0].split('Shipping Jurisdiction')[0]
        return res

    def records(self):
        cursor.execute("select member_id,totalproduct::float from orderitems")
        res=cursor.fetchall();jurs=[(self.getjurst(x[0]),x[1]) for x in res]
        df=pd.DataFrame(jurs,columns=["Jurs","Sales"])
        areas=list(df["Jurs"].unique())
        values=[df.loc[df["Jurs"]==a]["Sales"].sum() for a in areas]
        def calculatepie(vals,v):
            s=sum(vals);return int(round((v/s)*360))
        angles=[calculatepie(values,v) for v in values]
        return dict(areas=areas,values=angles,text="Sales by Jurisdiction")
