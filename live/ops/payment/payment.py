from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","pronov","localhost","5432")
import  importlib
from ops import CurrencyHelper,humanize_date,timestamp_forever,timestamp_now,textualize_datetime

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class PaymentPolicy:
    def __init__(self,language_id,policytype_id):
        self.language_id=language_id
        self.policytype_id=policytype_id
    
    def read(self):
        cursor.execute("""select policy.policy_id,policy.policyname,policy.policytype_id::text,
        policy.storeent_id,storeent.identifier,policy.properties,policy.starttime,policy.endtime,
        policydesc.description,policydesc.timecreated,policydesc.timeupdated from policy inner join 
        storeent on policy.storeent_id=storeent.storeent_id inner join
        policydesc on policy.policy_id=policydesc.policy_id where policy.policytype_id=%s and 
        policydesc.language_id=%s""",(self.policytype_id,self.language_id,))
        res=cursor.fetchall()
        if len(res) <=0:return [dict()]
        elif len(res)>0:return[dict(policy_id=r[0],name=r[1],type=r[2],storeent_id=r[3],store=r[4],
        properties=r[5],starttime=textualize_datetime(r[6]),endtime=textualize_datetime(r[7]),
        description=r[8],created=humanize_date(r[9]),updated=humanize_date(r[10])) for r in res]

class ReadPolicyTc:
    def __init__(self,trading_id,tcsubtype_id,language_id):
        self.trading_id=trading_id
        self.tcsubtype_id=tcsubtype_id
        self.language_id=language_id
        self.termcond_id=self.gettcid()
    
    def gettcid(self):
        cursor.execute("select termcond_id from termcond where trading_id=%s and tcsubtype_id=%s",
        (self.trading_id,self.tcsubtype_id,));res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def get(self):
        cursor.execute("""select policy.policy_id,policy.policyname,policy.policytype_id::text,
        policy.storeent_id,storeent.identifier,policy.properties,policy.starttime,policy.endtime,
        policydesc.description,policydesc.timecreated,policydesc.timeupdated from policy inner join 
        storeent on policy.storeent_id=storeent.storeent_id inner join policydesc on policy.policy_id=
        policydesc.policy_id inner join policytc on policy.policy_id=policytc.policy_id where policy.
        policytype_id=%s and policydesc.language_id=%s and policytc.termcond_id=%s""",(self.tcsubtype_id,
        self.language_id,self.termcond_id,));res=cursor.fetchall()
        if len(res) <=0:return None
        elif len(res)>0:return[dict(policy_id=r[0],name=r[1],type=r[2],storeent_id=r[3],store=r[4],
        properties=r[5],starttime=textualize_datetime(r[6]),endtime=textualize_datetime(r[7]),
        description=r[8],created=humanize_date(r[9]),updated=humanize_date(r[10])) for r in res]
