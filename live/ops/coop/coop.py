import psycopg2
from ops.connector.connector import evcon
con,cursor=evcon()

import pandas as pd
import numpy as np
import os,re,random,string,numbers
from ops import CurrencyHelper,humanize_date,timestamp_forever,timestamp_now,textualize_datetime

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class CheckMember:
    def __init__(self,member_id,mbrgrp_id):
        self.member_id=member_id
        self.mbrgrp_id=mbrgrp_id
    
    def check(self):
        cursor.execute("select mbrgrp_id from mbrgrpmbr where member_id=%s and mbrgrp_id=%s and exclude='0'",
        (self.member_id,self.mbrgrp_id,));res=cursor.fetchone()
        if res==None:return False
        elif res!=None:return True

class FetchMembers:
    def __init__(self,mbrgrp_id):
        self.mbrgrp_id=mbrgrp_id
    
    @staticmethod
    def mapexclusion(flag):
        if flag=='1':return "No"
        elif flag=='0':return 'Yes'
    
    def read(self):
        cursor.execute("""select mbrgrpmbr.member_id,orgentity.orgentityname,address.address1,address.email1,
        mbrgrpmbr.mbrgrp_id,mbrgrp.mbrgrpname,mbrgrpmbr.exclude from mbrgrp inner join mbrgrpmbr on mbrgrp.
        mbrgrp_id=mbrgrpmbr.mbrgrp_id inner join orgentity on mbrgrpmbr.member_id=orgentity.orgentity_id left 
        join address on mbrgrpmbr.member_id=address.member_id where mbrgrpmbr.mbrgrp_id=%s""",(self.mbrgrp_id,))
        res=cursor.fetchall()
        if len(res) > 0:
            pending=FetchPendingTransactions(res[0][0],self.mbrgrp_id).read()
            return [dict(member_id=r[0],member=r[1],address=r[2],email=r[3],mbrgrp_id=r[4],
        group=r[5],exclude=r[6],activated=self.mapexclusion(r[6]),_showDetails=False,
        pendingtransactions=pending) for r in res]
        elif len(res) <= 0:
            pending=FetchPendingTransactions(None,None).read()
            return [dict(member_id=None,member=None,address=None,email=None,mbrgrp_id=None,
        group=None,exclude=None,activated=None,_showDetails=None,pendingtransactions=pending)]

class FetchPendingTransactions:
    def __init__(self,member_id,mbrgrp_id):
        self.member_id=member_id
        self.mbrgrp_id=mbrgrp_id
    
    def read(self):
        cursor.execute("""select orgentity.orgentityname,confirmtransaction.holder_id,confirmtransaction.payee_id,
        confirmtransaction.referencenumber,confirmtransaction.status from orgentity inner join confirmtransaction 
        on orgentity.orgentity_id=confirmtransaction.payee_id where confirmtransaction.holder_id=%s and confirmtransaction
        .status='N'""",
        (self.mbrgrp_id,));res=cursor.fetchall()
        if len(res) <=0: return [dict(name=None,holder_id=None,payee_id=None,reference=None,status=None)]
        elif len(res) > 0:return [dict(name=r[0],holder_id=r[1],payee_id=r[2],reference=r[3],status=r[4])
        for r in res]

class ConfirmCTransaction:
    def __init__(self,holder_id,payee_id,referencenumber):
        self.holder_id=holder_id
        self.payee_id=payee_id
        self.referencenumber=referencenumber
    
    def confirm(self):
        try:
            cursor.execute("""update confirmtransaction set status='Y' where holder_id=%s and payee_id=%s
            and referencenumber=%s""",(self.holder_id,self.payee_id,self.referencenumber,));con.commit()
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def lock_unlock(self):
        cursor.execute("select count(status) from confirmtransaction where payee_id=%s and status='N'",(self.payee_id,))
        res=cursor.fetchone()[0]
        if res==0:
            cursor.execute("update mbrgrpmbr set exclude='0' where member_id=%s",(self.payee_id,))
            con.commit()
        elif res>0:
            cursor.execute("update mbrgrpmbr set exclude='1' where member_id=%s",(self.payee_id,))
            con.commit()

class Credit:
    def __init__(self,member_id,mbrgrp_id,tenure,rate,setccurr=None,timecreated=None,
    timeupdated=None,nextduedate=None,creditlimit=None,decimalfield1=None,
    decimalfield2=None,plan_integration=None,plan_code=None,plan_id=None,
    customer_code=None,subscription_code=None,email_token=None):
        self.member_id=member_id
        self.mbrgrp_id=mbrgrp_id
        self.tenure=tenure
        self.rate=rate
        self.setccurr=setccurr
        self.timecreated=timecreated
        self.timeupdated=timeupdated
        self.nextduedate=nextduedate
        self.creditlimit=creditlimit
        self.decimalfield1=decimalfield1
        self.decimalfield2=decimalfield2
        self.plan_integration=plan_integration
        self.plan_code=plan_code
        self.plan_id=plan_id
        self.customer_code=customer_code
        self.subscription_code=subscription_code
        self.email_token=email_token

    
    @staticmethod
    def outstanding(member_id):
        cursor.execute("""select credit.member_id from credit inner join creditstatus on credit.credit_id=
        creditstatus.credit_id where creditstatus.status='N' and credit.member_id=%s""",(member_id,))
        res=cursor.fetchone()
        if res==None:return False
        elif res!=None:return True
    
    def save(self):
        try:
            cursor.execute("""insert into credit(setccurr,member_id,mbrgrp_id,timecreated,timeupdated,
            nextduedate,tenure,rate,creditlimit,decimalfield1,decimalfield2,plan_integration,plan_code,
            plan_id,customer_code,email_token)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            returning credit_id""",(self.setccurr,self.member_id,self.mbrgrp_id,self.timecreated,
            self.timeupdated,self.nextduedate,self.tenure,self.rate,self.creditlimit,self.decimalfield1,
            self.decimalfield2,self.plan_integration,self.plan_code,self.plan_id,self.customer_code,
            self.email_token,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class CreditStatus:
    def __init__(self,credit_id,status='N'):
        self.credit_id=credit_id
        self.status=status
    
    def save(self):
        try:
            cursor.execute("""insert into creditstatus(credit_id,status)values(%s,%s)
            on conflict(credit_id,status)do update set credit_id=%s,status=%s returning
            credit_id""",(self.credit_id,self.status,self.credit_id,self.status,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Guarantor:
    def __init__(self,guarantor_id,borrower_id,credit_id,status='N'):
        self.guarantor_id=guarantor_id
        self.borrower_id=borrower_id
        self.credit_id=credit_id
        self.status=status
    
    def save(self):
        try:
            cursor.execute("""insert into guarantor(guarantor_id,borrower_id,credit_id,status)
            values(%s,%s,%s,%s)on conflict(guarantor_id,borrower_id,credit_id)do update set
            guarantor_id=%s,borrower_id=%s,credit_id=%s,status=%s returning guarantor_id""",
            (self.guarantor_id,self.borrower_id,self.credit_id,self.status,
            self.guarantor_id,self.borrower_id,self.credit_id,self.status,))
            con.commit();return cursor.fetchone()
        except (Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    def delete(self):
        try:
            cursor.execute("delete from guarantor where guarantor_id=%s and borrower_id=%s and credit_id=%s",
            (self.guarantor_id,self.borrower_id,self.credit_id,));con.commit()
        except (Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
