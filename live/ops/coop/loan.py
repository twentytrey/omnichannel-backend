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

class CooperativeRules:
    def __init__(self,member_id,language_id):
        self.language_id=language_id
        self.member_id=member_id
        self.group=self.getcoop()
        self.symbol=CurrencyHelper(language_id).getcurrsymbol()
    
    def getcoop(self):
        cursor.execute("""select mbrgrp.mbrgrpname,mbrgrpmbr.mbrgrp_id from mbrgrp inner join mbrgrpmbr
        on mbrgrp.mbrgrp_id=mbrgrpmbr.mbrgrp_id where mbrgrpmbr.member_id=%s""",(self.member_id,))
        res=cursor.fetchone()
        if res==None:return dict()
        elif res!= None:return dict(name=res[0],group_id=res[1])
    
    def read(self):
        cursor.execute("select field1,field2 from mbrgrpcond where mbrgrp_id=%s",(self.group["group_id"],))
        res=cursor.fetchall()
        if len(res) <=0: return dict()
        if len(res) > 0:return dict(res)

class TransactionHistory:
    def __init__(self,member_id,language_id):
        self.member_id=member_id
        self.language_id=language_id
        self.symbol=CurrencyHelper(language_id).getcurrsymbol()
    
    def read(self):
        cursor.execute("""select confirmtransaction.holder_id,confirmtransaction.payee_id,confirmtransaction.
        referencenumber,confirmtransaction.transaction_id,confirmtransaction.status,transaction.typecode,
        transaction.holder_id,transaction.amount::float::float,transaction.payee_id,transaction.timecreated,transaction.memo,
        facctransaction.faccount_id,facctransaction.crdr from confirmtransaction inner join transaction on 
        confirmtransaction.transaction_id=transaction.transaction_id inner join facctransaction on transaction.
        transaction_id=facctransaction.transaction_id where confirmtransaction.payee_id=%s and facctransaction.
        crdr='D'""",(self.member_id,));res=cursor.fetchall()
        if len(res) > 0:return [dict(holder_id=r[0],payee_id=r[1],reference=r[2],transaction_id=r[3],
        status=r[4],typecode=r[5],amount=r[7],timecreated=humanize_date(r[9]),memo=r[10],
        faccount_id=r[11],crdr=r[12],symbol=self.symbol)for r in res]
        elif len(res)<=0:return [dict(holder_id=None,payee_id=None,reference=None,transaction_id=None,
        status=None,typecode=None,amount=None,timecreated=None,memo=None,faccount_id=None,crdr=None,
        symbol=None)]

class LoanHistory:
    def __init__(self,member_id,language_id):
        self.member_id=member_id
        self.language_id=language_id
        self.symbol=CurrencyHelper(language_id).getcurrsymbol()
    
    def read(self):
        cursor.execute("""select credit.setccurr,credit.member_id,orgentity.orgentityname,credit.mbrgrp_id,
        mbrgrp.mbrgrpname,credit.timecreated,credit.timeupdated,credit.nextduedate,credit.tenure,credit.rate::float,
        credit.creditlimit,credit.decimalfield1::float,credit.decimalfield2::float,creditstatus.status,credit.credit_id 
        from credit inner join mbrgrp on credit.mbrgrp_id=mbrgrp.mbrgrp_id inner join orgentity on credit.member_id=
        orgentity.orgentity_id inner join creditstatus on credit.credit_id=creditstatus.credit_id where credit.member_id=%s""",
        (self.member_id,));res=cursor.fetchall()
        if len(res) > 0:return [dict(setccurr=r[0],member_id=r[1],name=r[2],group_id=r[3],groupname=r[4],
        timecreated=humanize_date(r[5]),timeupdated=humanize_date(r[6]),nextduedate=humanize_date(r[7]),
        tenure=r[8],rate=r[9],creditlimit=r[10],decimalfield1=r[11],decimalfield2=r[12],status=r[13],credit_id=r[14],
        symbol=self.symbol) for r in res]
        elif len(res) <=0:return [dict(setccurr=None,member_id=None,name=None,group_id=None,groupname=None,
        timecreated=None,timeupdated=None,nextduedate=None,tenure=None,rate=None,creditlimit=None,decimalfield=None,
        decimalfield2=None,status=None,credit_id=None,symbol=None)]

class GuarantorView:
    def __init__(self,member_id):
        self.member_id=member_id

    def get(self):
        cursor.execute("""select orgentity.orgentity_id,orgentity.orgentityname,users.profiletype,
        address.address1,address.phone1,userprof.photo from orgentity inner join users on orgentity.
        orgentity_id=users.users_id inner join address on users.users_id=address.member_id left join 
        userprof on users.users_id=userprof.users_id where users.profiletype='C' and orgentity.orgentity_id !=%s""",
        (self.member_id,));res=cursor.fetchall()
        if len(res)>0:return [dict(orgentity_id=r[0],orgentityname=r[1],profiletype=r[2],
        address1=r[3],phone1=r[4],photo=r[5]) for r in res]
        elif len(res)<=0:return [dict(orgentity_id=None,orgentityname=None,profiletype=None,
        address1=None,phone1=None,photo=None)]

class GuarantorBalance:
    def __init__(self,guarantor_id,language_id):
        self.guarantor_id=guarantor_id
        self.language_id=language_id
        cc=CurrencyHelper(language_id)
        self.symbol=cc.getcurrsymbol()
        self.balanceval=self.balance()
        self.balanceval_fmt=cc.formatamount(self.balanceval)
    
    def cashbalance(self):
        cursor.execute("""select faccount.faccount_id,faccount.identifier,faccount.member_id,facctransaction.
        transaction_id,facctransaction.crdr,transaction.amount::float from faccount inner join facctransaction on 
        faccount.faccount_id=facctransaction.faccount_id inner join transaction on facctransaction.transaction_id=
        transaction.transaction_id where faccount.member_id=%s and faccount.identifier='Investments'""",(self.guarantor_id,))
        res=cursor.fetchall()
        if len(res) > 0:
            credits=[x[5] for x in res if x[4]=='C']
            debits=[x[5] for x in res if x[4]=='D']
            return round(sum(debits)-sum(credits),2)
        elif len(res)<=0:return 0
    
    def acpbalance(self):
        cursor.execute("""select faccount.faccount_id,faccount.identifier,faccount.member_id,facctransaction.
        transaction_id,facctransaction.crdr,transaction.amount::float from faccount inner join facctransaction on 
        faccount.faccount_id=facctransaction.faccount_id inner join transaction on facctransaction.transaction_id=
        transaction.transaction_id where faccount.member_id=%s and faccount.identifier='Accounts Payable'""",(self.guarantor_id,))
        res=cursor.fetchall()
        if len(res) > 0:
            credits=[x[5] for x in res if x[4]=='C']
            debits=[x[5] for x in res if x[4]=='D']
            return round(sum(debits)-sum(credits),2)
        elif len(res)<=0:return 0
        
    def escrowbalance(self):
        cursor.execute("""select faccount.faccount_id,faccount.identifier,faccount.member_id,facctransaction.
        transaction_id,facctransaction.crdr,transaction.amount::float from faccount inner join facctransaction on 
        faccount.faccount_id=facctransaction.faccount_id inner join transaction on facctransaction.transaction_id=
        transaction.transaction_id where faccount.member_id=%s and faccount.identifier='Escrow'""",(self.guarantor_id,))
        res=cursor.fetchall()
        if len(res) > 0:
            credits=[x[5] for x in res if x[4]=='C']
            debits=[x[5] for x in res if x[4]=='D']
            return round(sum(debits)-sum(credits),2)
        elif len(res)<=0:return 0

    def balance(self):
        return self.cashbalance()-self.escrowbalance()-self.acpbalance()

class Guarantees:
    def __init__(self,guarantor_id,language_id):
        self.guarantor_id=guarantor_id
        self.language_id=language_id
        self.cc=CurrencyHelper(language_id)

    def read(self):
        cursor.execute("""select orgentity.orgentityname as guarantorname,guarantor.credit_id,
        orgentity.orgentityname as borrowername,guarantor.status,guarantor.transaction_id,credit.
        decimalfield1::float,credit.decimalfield2::float,credit.rate::float,credit.tenure from orgentity 
        inner join guarantor on orgentity.orgentity_id=guarantor.guarantor_id inner join credit on 
        credit.credit_id=guarantor.credit_id where guarantor.guarantor_id=%s""",
        (self.guarantor_id,));res=cursor.fetchall()
        if len(res) > 0:return [dict(guarantor_name=r[0],credit_id=r[1],borrower_name=r[2],
        guarantor_status=r[3],transaction_id=r[4],principal=r[5],principal_fmt=self.cc.formatamount(r[5]),
        repayment=r[6],repayment_fmt=self.cc.formatamount(r[6]),symbol=self.cc.getcurrsymbol(),
        rate=r[7],tenure=r[8]) for r in res]
        elif len(res) <=0:return None
