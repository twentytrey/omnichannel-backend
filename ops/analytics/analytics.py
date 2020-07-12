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
import matplotlib.pyplot as plt
import squarify
from ops.helpers.functions import humanize_date,textualize_datetime,month,monthyear,getcatalog,CurrencyHelper,human_format,day

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

def min_max_dates(owner_id):
    cursor.execute("""select orderitems.lastcreate from orderitems inner join orders on orderitems.
    orders_id=orders.orders_id where orders.editor_id=%s""",(owner_id,));res=cursor.fetchall()
    if len(res)<=0:return None,None
    elif len(res)>0:
        res=[x for (x,) in res]
        oldest=min(res)
        youngest=max(dt for dt in res if dt<datetime.datetime.now())
        return [textualize_datetime(oldest),textualize_datetime(youngest)]

class RateStores:
    def __init__(self,owner_id,language_id):
        self.owner_id=owner_id
        self.cc=CurrencyHelper(language_id)
    
    def storename(self,storeid):
        cursor.execute("select identifier from storeent where storeent_id=%s",(storeid,))
        res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res[0]
    
    def prepare(self):
        rows,cols=SalesMatrix(self.owner_id).get()
        df=pd.DataFrame(rows,columns=cols)
        df['totalsales']=df['price']*df['quantity']
        df['storename']=df["storeid"].apply(self.storename)
        storegroups=df.groupby("storename");totals=list();stores=list()
        [(stores.append(i),totals.append( round(g['totalsales'].sum(),2))) for i,g in storegroups]
        def scaleitems(lower,upper,x,series):
            num=x-min(series)
            denum=max(series)-min(series)
            return round((upper-lower)*(num/denum)+lower,1)
        def storepc(x,series):return round(100*(x/sum(series)),2)
        pcs=[storepc(x,totals) for x in totals];scores=["{}{}".format(self.cc.getcurrsymbol(),self.cc.formatamount(round(x,2))) 
        for x in totals]
        data=[(scores[i],pcs[i],stores[i]) for i in range(len(stores))];return data
    
    def top(self):
        data=self.prepare()
        return [dict(score=x[0],percentage=x[1],storename=x[2]) for x in data]

class RateItems:
    def __init__(self,owner_id):
        self.owner_id=owner_id
    
    def itemname(self,catentry_id):
        cursor.execute("select name from catentdesc where catentry_id=%s",(catentry_id,))
        res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def itemimage(self,name):
        cursor.execute("select fullimage from catentdesc where name=%s",(name,))
        res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def prepare(self):
        rows,cols=SalesMatrix(self.owner_id).get()
        df=pd.DataFrame(rows,columns=cols)
        df['totalsales']=df['price']*df['quantity']
        df['productname']=df['catentryid'].apply(self.itemname)
        itemgroups=df.groupby("productname");totals=list();items=list()
        [(items.append(i),totals.append(round(g['totalsales'].sum(),2))) for i,g in itemgroups]
        def scaleitems(lower,upper,x,series):
            num=x-min(series)
            denum=max(series)-min(series)
            return round((upper-lower)*(num/denum)+lower,1)
        def itempc(x,series):return round(100*(x/sum(series)),2)
        pcs=[itempc(x,totals) for x in totals];scores=[scaleitems(1,5,x,totals) for x in totals]
        data=[(scores[i],pcs[i],items[i],self.itemimage(items[i])) for i in range(len(items))];return data
    
    def top10(self):
        data=self.prepare()
        sortedata=sorted(data,reverse=True)[:10]
        serialized=[dict(score=x[0],percentage=x[1],product=x[2],image=x[3]) for x in sortedata]
        return serialized

class RateCategories:
    def __init__(self,owner_id):
        self.owner_id=owner_id
    
    def catgroupname(self,catentry_id):
        cursor.execute("""select catgroup.identifier from catgroup inner join catgpenrel on
        catgpenrel.catgroup_id=catgroup.catgroup_id where catgpenrel.catentry_id=%s""",(catentry_id,))
        res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def prepare(self):
        rows,cols=SalesMatrix(self.owner_id).get()
        df=pd.DataFrame(rows,columns=cols)
        df['category']=df['catentryid'].apply(self.catgroupname)
        df['totalsales']=df['price']*df['quantity']
        catgroups=df.groupby("category");totals,categories=[],[]
        [(categories.append(i),totals.append(round(g["totalsales"].sum(),2))) for i,g in catgroups]
        def scalecategories(lower,upper,x,series):
            num=x-min(series)
            denum=max(series)-min(series)
            return round((upper-lower)*(num/denum)+lower,1)
        def categorypc(x,series):return round(100*(x/sum(series)),2)
        pcs=[categorypc(x,totals) for x in totals];scores=[scalecategories(1,5,x,totals) for x in totals]
        data=[(scores[i],pcs[i],categories[i]) for i in range(len(categories))];return data
    
    def top5(self):
        data=self.prepare()
        sortedata=sorted(data,reverse=True)[:5]
        serialized=[dict(score=x[0],percentage=x[1],category=x[2]) for x in sortedata]
        return serialized

class SalesSeries:
    def __init__(self,start,end,owner_id):
        self.start=start
        self.end=end
        self.owner_id=owner_id
    
    def defaultmatrix(self):
        rows,cols=SalesMatrix(self.owner_id).get()
        df=pd.DataFrame(rows,columns=cols)
        df['invoicedate']=df['invoicedate'].apply(lambda x:x.split(' ')[0])
        df['totalsales']=df['quantity']*df['price']
        dategroups=df.groupby('invoicedate');data=list();dates=list()
        [(dates.append(i),data.append(round(g["totalsales"].sum(),2))) for i,g in dategroups]
        return dict(data=data,dates=dates,title="Sales volume beginning to date.")

class DaysPerformance:
    def __init__(self,owner_id,language_id):
        self.owner_id=owner_id
        self.language_id=language_id
        self.cc=CurrencyHelper(language_id)
    
    def getmatrix(self):
        rows,cols=SalesMatrix(self.owner_id).get()
        df=pd.DataFrame(rows,columns=cols)
        df["invoicedate"]=pd.to_datetime(df["invoicedate"])
        df.dropna(inplace=True)
        df["totalsum"]=df["quantity"]*df["price"]
        df['day']=df['invoicedate'].apply(day)
        daygroups=df.groupby('day');days=[];values=[];pcs=list()
        [days.append(i) for i,g in daygroups]
        [values.append(round(g['totalsum'].sum(),2)) for i,g in daygroups]
        [pcs.append(round(100*(x/sum(values)),2)) for x in values]
        return days,pcs,values

class SalesByJurisdiction:
    def __init__(self,owner_id,language_id):
        self.owner_id=owner_id
        self.language_id=language_id
        self.cc=CurrencyHelper(language_id)

    def jurst(self,state):
        cursor.execute("""select jurstgroup.description from jurst inner join jurstgprel on 
        jurst.jurst_id=jurstgprel.jurst_id inner join jurstgroup on jurstgprel.jurstgroup_id=
        jurstgroup.jurstgroup_id where jurst.state=%s""",(state,));res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def records(self):
        cursor.execute("""select orderitems.member_id,orgentity.orgentityname,orderitems.totalproduct::float,
        address.state,address.country from orderitems inner join address on orderitems.member_id=address.member_id 
        inner join orgentity on orderitems.member_id=orgentity.orgentity_id inner join orders on orderitems.orders_id=
        orders.orders_id where orders.editor_id=%s""",(self.owner_id,));res=cursor.fetchall()
        cols=["customerid","customername","totalproduct","state","country"]
        if len(res)>0:
            rows=[[r[0],r[1],r[2],r[3],r[4]] for r in res]
            return rows,cols
    
    def getmatrix(self):
        data=self.records()
        if data!=None:
            rows,cols=data[0],data[1]
            df=pd.DataFrame(rows,columns=cols)
            stategroups=df.groupby("state");areas=list();values=list()
            [areas.append(i) for i,g in stategroups]
            [values.append(g["totalproduct"].sum()) for i,g in stategroups]
            sums=sum(values);angles=[round((v/sums)*360,2) for v in values]
            return dict(areas=areas,values=angles,text="Sales by Jurisdiction")

class SalesMatrix:
    def __init__(self,owner_id,):
        self.owner_id=owner_id
    
    def get(self):
        cursor.execute("""select orderitems.member_id,orderitems.catentry_id,orgentity.orgentityname,
        orderitems.quantity,orderitems.price::float,orderitems.lastcreate,orderitems.storeent_id from 
        orders inner join orderitems on orders.orders_id=orderitems.orders_id left join orgentity on 
        orders.editor_id=orgentity.orgentity_id where orders.editor_id=%s""",(self.owner_id,))
        res=cursor.fetchall();rows=None
        cols=["customerid","catentryid","customername","quantity","price","invoicedate","storeid"]
        if len(res)<=0:rows=None
        elif len(res) > 0:rows=[[r[0],r[1],r[2],r[3],r[4],textualize_datetime(r[5]),r[6]] for r in res]
        return rows,cols

class DashboardCounts:
    def __init__(self,owner_id,language_id):
        self.owner_id=owner_id
        self.language_id=language_id
        self.cc=CurrencyHelper(language_id)

    def _execute(self):
        d=self.getmatrix()
        data=[self.countorders(),self.counttotalsales(d),self.countcustomers(),
        self.countaveragetransactionvalue(d)];return data

    def countorders(self):
        cursor.execute("select count(orders_id)from orders")
        res=cursor.fetchone()
        if res==None:return{"val":0,"cformat":0,"text":"Total Orders","hformat":0}
        else:
            val=res[0];cformat=self.cc.formatamount(val)
            hformat=human_format(val)
            return {"val":val,"cformat":cformat,"text":"Total Orders","hformat":hformat}

    def counttotalsales(self,df):
        val=round(sum(df["quantity"]*df["price"]),2) or 0
        cformat="{}{}".format(self.cc.getcurrsymbol(),self.cc.formatamount(val))
        hformat="{}{}".format(self.cc.getcurrsymbol(),human_format(val))
        return {"cformat":cformat,"val":val,"hformat":hformat,"text":"Sales Revenue"}

    def countcustomers(self):
        cursor.execute("""select count(orgentity.orgentity_id) from orgentity 
        inner join users on orgentity.orgentity_id=users.users_id where users.
        profiletype='C'""");res=cursor.fetchone()
        if res==None:return{"val":0,"cformat":0,"hformat":0,"text":"Customers"}
        else:
            val=res[0];cformat=self.cc.formatamount(val);hformat=human_format(val)
            return {"val":val,"cformat":cformat,"hformat":hformat,"text":"Customers"}

    def countavgorderspercustomer(self):
        totalorders=self.countorders()["val"]
        totalcustomers=self.countcustomers()["val"]
        if totalorders > 0 and totalcustomers > 0:
            val=round((totalorders/totalcustomers),2)
            cformat=self.cc.formatamount(val);hformat=human_format(val)
            return {"val":val,"cformat":cformat,"hformat":hformat,"text":"Avg. Orders per Customer"}
        else:return {"val":0,"cformat":0,"hformat":0,"text":"Avg. Orders per Customer"}

    def countaveragetransactionvalue(self,df):
        ordersize=self.countorders()["val"]
        sales=sum(df["totalsales"])
        if ordersize > 0 and sales > 0:
            val=sales/ordersize
            cformat="{}{}".format(self.cc.getcurrsymbol(),self.cc.formatamount(val))
            hformat="{}{}".format(self.cc.getcurrsymbol(),human_format(val))
            return {"cformat":cformat,"val":val,"hformat":hformat,"text":"Average Transaction Value"}
        else:return {"cformat":0,"hformat":0,"text":"Average Transaction Value","val":0}
    
    def getmatrix(self):
        rows,cols=SalesMatrix(self.owner_id).get()
        df=pd.DataFrame(rows,columns=cols)
        df["invoicedate"]=pd.to_datetime(df["invoicedate"])
        df["totalsales"]=df["quantity"]*df["price"]
        df.dropna(inplace=True)
        return df

class RFM:
    def __init__(self,owner_id):
        self.owner_id=owner_id

    def chartdata(self,df):
        fx=lambda x:round(x,2)
        fx2=lambda x:round((x/24),2)
        df["monetary"]=df["monetary"].apply(fx)
        df["recency"]=df["recency"].apply(fx2)

        rows=[["Product","Recency","Frequency","Monetary"]]
        df=df[["storeid","recency","frequency","monetary"]]
        df["monetary"]-=df["monetary"].min();df["monetary"]/=df["monetary"].max()
        df["recency"]-=df["recency"].min();df["recency"]/=df["recency"].max()
        df["frequency"]-=df["frequency"].min();df["frequency"]/=df["frequency"].max()
        [rows.append(list(x)) for x in df.values]
        series=[dict(type='bar') for x in range(3)]
        return rows,series

    def vaporizetable(self,df):
        cc=CurrencyHelper(1)
        fx=lambda x:"{}{}".format(cc.getcurrsymbol(),cc.formatamount(round(x,2)))
        fx2=lambda x:"{} (days ago)".format(int(round(x/24)))
        fx3=lambda x:"{} visits".format(x)
        df["monetary"]=df["monetary"].apply(fx)
        df["recency"]=df["recency"].apply(fx2)
        df["frequency"]=df["frequency"].apply(fx3)
        columns=(list(df.columns));columns.remove('orgid');columns.remove("contractid");columns.append('_')
        rows=[dict(zip(['storeid', 'recency', 'frequency', 'monetary', 'R', 'F', 'M','orgid','OER','contractid','RFM'],x)) for x in df.values]
        return columns,rows

    def getmatrix(self):
        data=SalesMatrix(self.owner_id).get()
        if data[0]==None:return pd.DataFrame()
        else:
            rows,cols=data[0],data[1]
            df=pd.DataFrame(rows,columns=cols)
            df["invoicedate"]=pd.to_datetime(df["invoicedate"])
            df.dropna(inplace=True)
            df["totalsum"]=df["quantity"]*df["price"];df["invoiceno"]=None
            snapshotdate=df["invoicedate"].max()+datetime.timedelta(days=1)
            customergroups=df.groupby("customerid");rows2=[];cols2=["storeid","recency","frequency","monetary"]
            for i,g in customergroups:
                timediff=snapshotdate-g["invoicedate"].max()
                timediff=round(timediff.total_seconds()/(60*60),4)
                invoiceno=g["invoicedate"].count()
                totalsum=g["totalsum"].sum()
                rows2.append([i,timediff,invoiceno,totalsum])
            dataprocess=pd.DataFrame(rows2,columns=cols2)
            return dataprocess

    def getstoreorgid(self,storename):
        cursor.execute("select member_id from storeent where identifier=%s",(storename,))
        res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res[0]

    def getcontract(self,orgid):
        cursor.execute("""select contract.contract_id from contract inner join participnt on 
        contract.contract_id=participnt.trading_id inner join orgentity on orgentity.orgentity_id=
        participnt.member_id where participnt.member_id=%s and contract.usage=1;""",(orgid,))
        res=cursor.fetchone()
        if res==None:return 0
        elif res!=None:return res[0]

    def getoerscore(self,orgid):
        return OER(orgid).getbalance()

    def qcuts(self,dataprocess):
        r_labels=["5","4","3"];f_labels=["3","4","5"];m_labels=["3","4","5"]
        r_groups=pd.qcut(dataprocess["recency"],3,labels=r_labels)
        f_groups=pd.qcut(dataprocess["frequency"],3,labels=f_labels)
        m_groups=pd.qcut(dataprocess["monetary"],3,labels=m_labels)
        def storename(store_id):
            cursor.execute("select orgentityname from orgentity where orgentity_id=%s",(int(store_id),))
            return cursor.fetchone()[0]
        dataprocess=dataprocess.assign(R=r_groups.values,F=f_groups.values,M=m_groups.values)
        dataprocess["storeid"]=dataprocess["storeid"].apply(storename)
        dataprocess["orgid"]=dataprocess["storeid"].apply(self.getstoreorgid)
        dataprocess["OER"]=dataprocess["orgid"].apply(self.getoerscore)
        dataprocess["contractid"]=dataprocess["orgid"].apply(self.getcontract)
        def join_rfm(x):return int(x['R'])+int(x['F'])+int(x['M'])
        def label_r(x):
            mp=dict(zip(["5","4","3"],["latest","recent","stale"]))
            return mp[x]
        def label_f(x):
            mp=dict(zip(["3","4","5"],["bad","medium","good"]))
            return mp[x]
        def label_m(x):
            mp=dict(zip(["3","4","5"],["low","medium","high"]))
            return mp[x]
        dataprocess['RFM']=dataprocess.apply(join_rfm,axis=1)
        dataprocess["R"]=dataprocess["R"].apply(label_r)
        dataprocess["F"]=dataprocess["F"].apply(label_f)
        dataprocess["M"]=dataprocess["M"].apply(label_m)        
        return dataprocess

from ops.accounting.accounting import Faccount as fac
class OER:
    def __init__(self,owner_id):
        self.owner_id=owner_id
    
    def expense_accounts(self):
        cursor.execute("""select faccount.faccount_id from faccount inner join 
        accountclassrel on faccount.faccount_id=accountclassrel.faccount_id inner 
        join acclass on accountclassrel.acclass_id=acclass.acclass_id where faccount.
        member_id=%s and acclass.name in ('COGS','Expense');""",(self.owner_id,))
        res=cursor.fetchall()
        if len(res) > 0:return [x for (x,) in res]
        elif len(res)<=0:return None
    
    def revenue_accounts(self):
        cursor.execute("""select faccount.faccount_id from faccount inner join 
        accountclassrel on faccount.faccount_id=accountclassrel.faccount_id inner 
        join acclass on accountclassrel.acclass_id=acclass.acclass_id where faccount.
        member_id=%s and acclass.name in ('Revenue')""",(self.owner_id,))
        res=cursor.fetchall()
        if len(res)>0:return [x for (x,) in res]
        elif len(res) <=0:return None
    
    def getbalance(self):
        expenseaccounts=self.expense_accounts()
        revenueaccounts=self.revenue_accounts()
        c_expensebalances=[fac.credit_debit_balance(x,self.owner_id,'C') for x in expenseaccounts]
        d_expensebalances=[fac.credit_debit_balance(x,self.owner_id,'D') for x in expenseaccounts]
        c_expensebalances=[1*x for x in c_expensebalances];d_expensebalances=[-1*x for x in d_expensebalances]

        c_revenuebalances=[fac.credit_debit_balance(x,self.owner_id,'C') for x in revenueaccounts]
        d_revenuebalances=[fac.credit_debit_balance(x,self.owner_id,'D') for x in revenueaccounts]
        c_revenuebalances=[1*x for x in c_revenuebalances];d_revenuebalances=[-1*x for x in d_revenuebalances]

        s_expenses=abs(sum(c_expensebalances)+sum(d_expensebalances))
        s_revenues=abs(sum(c_revenuebalances)+sum(d_revenuebalances))
        if s_revenues>0:return int(round(100*(s_expenses/s_revenues)))
        elif s_revenues<=0:return 0

class OERScores:
    def __init__(self,holder_id):
        self.holder_id=holder_id

    def readmembers(self):
        cursor.execute("""select orgentity.orgentity_id,orgentity.orgentityname from storeent inner 
        join orgentity on storeent.member_id=orgentity.orgentity_id and orgentity.
        orgentity_id>%s""",(self.holder_id,));res=cursor.fetchall()
        if len(res)<=0:return None
        elif len(res)>0:return [list(x) for x in res]

    def getscores(self):
        members=self.readmembers()
        ids=[x[0] for x in members]
        names=[x[1] for x in members]
        scores=[OER(i).getbalance() for i in ids]
        return names,scores
