# from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
# con,cursor=createcon("retail","jmso","localhost","5432")
from ops.connector.connector import evcon
con,cursor=evcon()

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

class SaveReference:
    def __init__(self,orders_id,refid):
        self.orders_id=orders_id
        self.refid=refid
    
    def save(self):
        try:
            cursor.execute("update orders set field3=%s where orders_id=%s",
            (self.refid,self.orders_id,));con.commit()
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class CardAuth:
    def __init__(self,member_id,authorization_code,last4,expmonth,expyear,cardtype=None,bin=None,bank=None,channel=None,
    signature=None,reusable=None,country_code=None):
        self.member_id=member_id
        self.authorization_code=authorization_code
        self.last4=last4
        self.expmonth=expmonth
        self.expyear=expyear
        self.cardtype=cardtype
        self.bin=bin
        self.bank=bank
        self.channel=channel
        self.signature=signature
        self.reusable=reusable
        self.country_code=country_code
    
    def save(self):
        try:
            cursor.execute("""insert into cardauth(member_id,authorization_code,cardtype,last4,expmonth,expyear,
            bin,bank,channel,signature,reusable,country_code)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict
            (member_id)do update set authorization_code=%s,cardtype=%s,last4=%s,expmonth=%s,expyear=%s,
            bin=%s,bank=%s,channel=%s,signature=%s,reusable=%s,country_code=%s returning member_id""",
            (self.member_id,self.authorization_code,self.cardtype,self.last4,self.expmonth,self.expyear,
            self.bin,self.bank,self.channel,self.signature,self.reusable,self.country_code,self.authorization_code,
            self.cardtype,self.last4,self.expmonth,self.expyear,self.bin,self.bank,self.channel,self.signature,
            self.reusable,self.country_code,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
