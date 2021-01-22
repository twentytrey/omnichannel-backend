# from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
# con,cursor=createcon("retail","jmso","localhost","5432")
from ops.connector.connector import evcon
con,cursor=evcon()

import  importlib
import pandas as pd
import numpy as np
from ops import textualize_datetime,CurrencyHelper,humanize_date

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Acclass:
    def __init__(self,name,member_id,rangestart=None,rangeend=None,timecreated=None):
        self.name=name
        self.member_id=member_id
        self.rangestart=rangestart
        self.rangeend=rangeend
        self.timecreated=timecreated
    
    @staticmethod
    def get_class_name(class_id):
        cursor.execute("select name from acclass where acclass_id=%s",(class_id,))
        res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res[0]
    
    @staticmethod
    def read(mid,lid):
        cursor.execute("""select acclass_id,name,rangestart,rangeend,timecreated from acclass where
        member_id=%s""",(mid,));res=cursor.fetchall()
        if len(res) <= 0:return [dict(acclass_id=None,name=None,ref_start=None,ref_end=None,created_on=None)]
        elif len(res) > 0:return [dict(acclass_id=r[0],name=r[1],ref_start=r[2],ref_end=r[3],created_on=r[4],
        description=Acclassdsc.read(r[0],lid))for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into acclass(name,member_id,rangestart,rangeend,timecreated)
            values(%s,%s,%s,%s,%s)on conflict(name,member_id)do update set name=%s,member_id=%s,
            rangestart=%s,rangeend=%s,timecreated=%s returning acclass_id""",(self.name,self.member_id,
            self.rangestart,self.rangeend,self.timecreated,self.name,self.member_id,self.rangestart,
            self.rangeend,self.timecreated,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acclassdsc:
    def __init__(self,acclass_id,language_id,description=None):
        self.acclass_id=acclass_id
        self.language_id=language_id
        self.description=description
    
    @staticmethod
    def read(acc_id,lid):
        cursor.execute("select description from acclassdsc where acclass_id=%s and language_id=%s",
        (acc_id,lid,));res=cursor.fetchone()
        if len(res) <= 0:return dict(description=None)
        elif len(res) > 0:return dict(description=res[0])

    def save(self):
        try:
            cursor.execute("""insert into acclassdsc(acclass_id,language_id,description)
            values(%s,%s,%s)on conflict(acclass_id,language_id)do update set acclass_id=%s,
            language_id=%s,description=%s returning acclass_id""",(self.acclass_id,
            self.language_id,self.description,self.acclass_id,self.language_id,self.description,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

# print( Acclass.read(1,1) )

class Acclassrel:
    def __init__(self,parent_id,child_id):
        self.parent_id=parent_id
        self.child_id=child_id

    def save(self):
        try:
            cursor.execute("""insert into acclassrel(parent_id,child_id)values(%s,%s)
            on conflict(parent_id,child_id)do update set parent_id=%s,child_id=%s
            returning parent_id""",(self.parent_id,self.child_id,self.parent_id,self.child_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Faccount:
    def __init__(self,accountnumber,identifier,member_id,routingnumber=None,setccurr=None):
        self.accountnumber=accountnumber
        self.identifier=identifier
        self.member_id=member_id
        self.routingnumber=routingnumber
        self.setccurr=setccurr
    
    @staticmethod
    def credit_debit_balance(faccount_id,holder_id,crdr):
        cursor.execute("""select sum(transaction.amount::float) from transaction inner join
        facctransaction on transaction.transaction_id=facctransaction.transaction_id 
        where transaction.holder_id=%s and facctransaction.crdr=%s and facctransaction.faccount_id=%s""",
        (holder_id,crdr,faccount_id,));res=cursor.fetchone()[0]
        if res==None:return 0
        elif res!=None:return res
    
    @staticmethod
    def get_balance(faccount_id):
        cursor.execute("""select sum(transaction.amount)::float from faccount inner join facctransaction 
        on faccount.faccount_id=facctransaction.faccount_id inner join transaction on facctransaction.
        transaction_id=transaction.transaction_id where faccount.faccount_id=%s""",(faccount_id,))
        res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res[0]
    
    @staticmethod
    def getid(name,member_id):
        cursor.execute("select faccount_id from faccount where identifier=%s and member_id=%s",(name,member_id,))
        res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res[0]
    
    @staticmethod
    def getclass(faccount_id):
        if faccount_id==None:return None
        elif faccount_id != None:
            cursor.execute("""select acclass.acclass_id,acclass.name from accountclassrel inner join faccount on 
            accountclassrel.faccount_id=faccount.faccount_id inner join acclass on accountclassrel.
            acclass_id=acclass.acclass_id where faccount.faccount_id=%s""",(faccount_id,))
            return cursor.fetchone()
        
    @staticmethod
    def readtransactions(faccount_id,member_id,language_id):
        cursor.execute("""select faccount.faccount_id,faccount.accountnumber,faccount.identifier,
        faccount.member_id,orgentity.orgentityname,faccount.setccurr,transaction.typecode,transaction.
        amount::float,transaction.timecreated,transaction.memo from faccount inner join orgentity on faccount.
        member_id=orgentity.orgentity_id inner join facctransaction on faccount.faccount_id=facctransaction.
        faccount_id inner join transaction on facctransaction.transaction_id=transaction.transaction_id 
        where faccount.faccount_id=%s and faccount.member_id=%s;""",
        (faccount_id,member_id,));res=cursor.fetchall()
        if len(res) <= 0:return [dict(faccount_id=None,reference=None,symbol=None,identifier=None,member_id=None,payee=None,
        currency=None,type=None,amount=None,created_on=None,timecreated=None)]
        elif len(res) > 0:return [dict(faccount_id=r[0],reference=r[1],identifier=r[2],member_id=r[3],payee=r[4],
        currency=r[5],symbol=CurrencyHelper(language_id).getcurrsymbol(),type=r[6],
        amount=CurrencyHelper(language_id).formatamount(r[7]),created_on=humanize_date(r[8]),
        timecreated=textualize_datetime(r[8]))for r in res]

    @staticmethod
    def readaccount(faccount_id,mid,lid):
        cursor.execute("""select faccount_id,accountnumber,identifier,routingnumber,setccurr from faccount
        where member_id=%s and faccount_id=%s""",(mid,faccount_id,));res=cursor.fetchone()
        if res==None:return dict(faccount_id=None,account_number=None,identifier=None,routing_number=None,
        currency=None,description=None,account_type=None,balance=CurrencyHelper(lid).formatamount(0.00))
        elif res != None:return dict(faccount_id=res[0],account_number=res[1],identifier=res[2],routing_number=res[3],
        currency=res[4],description=Faccountdsc.read(res[0],lid),balance=CurrencyHelper(lid).formatamount(0.00),
        account_class=Faccount.getclass(res[0])[1])

    @staticmethod
    def read(mid,lid):
        cursor.execute("""select faccount_id,accountnumber,identifier,routingnumber,setccurr from faccount
        where member_id=%s order by faccount_id asc""",(mid,));res=cursor.fetchall()

        if len(res) <= 0:return [dict(faccount_id=None,accountnumber=None,account_number=None,identifier=None,
        routingnumber=None,routing_number=None,setccurr=None,currency=None,symbol=None,description=None,acclass_id=None,
        account_type=None,balance=CurrencyHelper(lid).formatamount(0.00))]

        elif len(res) > 0:return [dict(faccount_id=r[0],accountnumber=r[1],account_number=r[1],identifier=r[2],
        routingnumber=r[3],routing_number=r[3],setccurr=r[4],currency=r[4],symbol=CurrencyHelper(lid).getcurrsymbol(),description=Faccountdsc.read(r[0],lid),
        credit=CurrencyHelper(lid).formatamount(round(Faccount.credit_debit_balance(r[0],mid,'C'),2)),debit=CurrencyHelper(lid).
        formatamount(round(Faccount.credit_debit_balance(r[0],mid,'D'),2)),acclass_id=Faccount.getclass(r[0])[0],
        account_class=Faccount.getclass(r[0])[1])for r in res]
    
    def update(self,faccount_id):
        try:
            cursor.execute("""update faccount set accountnumber=%s,identifier=%s,member_id=%s,routingnumber=%s,
            setccurr=%s where faccount_id=%s and member_id=%s""",(self.accountnumber,self.identifier,self.member_id,
            self.routingnumber,self.setccurr,faccount_id,self.member_id,));con.commit()
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    def save(self):
        try:
            cursor.execute("""insert into faccount(accountnumber,identifier,member_id,routingnumber,
            setccurr)values(%s,%s,%s,%s,%s)on conflict(accountnumber,identifier,member_id)do update 
            set accountnumber=%s,identifier=%s,member_id=%s,routingnumber=%s,setccurr=%s returning
            faccount_id""",(self.accountnumber,self.identifier,self.member_id,self.routingnumber,self.setccurr,
            self.accountnumber,self.identifier,self.member_id,self.routingnumber,self.setccurr,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Faccountdsc:
    def __init__(self,faccount_id,language_id,description=None):
        self.faccount_id=faccount_id
        self.language_id=language_id
        self.description=description
    
    @staticmethod
    def read(fid,lid):
        cursor.execute("""select description from faccountdsc where faccount_id=%s
        and language_id=%s""",(fid,lid,));res=cursor.fetchone()
        if res == None:return None
        elif res != None:return res[0]
    
    def update(self):
        try:
            cursor.execute("update faccountdsc set description=%s where faccount_id=%s and language_id=%s",
            (self.description,self.faccount_id,self.language_id,));con.commit()
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def save(self):
        try:
            cursor.execute("""insert into faccountdsc(faccount_id,language_id,description)
            values(%s,%s,%s)on conflict(faccount_id,language_id)do update set faccount_id=%s,
            language_id=%s,description=%s returning faccount_id""",(self.faccount_id,
            self.language_id,self.description,self.faccount_id,self.language_id,self.description,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

# print(Faccountdsc.read(1,1))
# print(Faccount.read(1,1))

class Accountclassrel:
    def __init__(self,acclass_id,faccount_id):
        self.acclass_id=acclass_id
        self.faccount_id=faccount_id
    
    def update(self):
        try:
            cursor.execute("update accountclassrel set acclass_id=%s,faccount_id=%s where faccount_id=%s and acclass_id=%s",
            (self.acclass_id,self.faccount_id,self.faccount_id,self.acclass_id,));con.commit()
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def save(self):
        try:
            cursor.execute("""insert into accountclassrel(acclass_id,faccount_id)values
            (%s,%s)on conflict(acclass_id,faccount_id)do update set acclass_id=%s,faccount_id=%s
            returning faccount_id""",(self.acclass_id,self.faccount_id,self.acclass_id,self.faccount_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Transactiontype:
    def __init__(self,code=None,description=None,longdescription=None):
        self.code=code
        self.description=description
        self.longdescription=longdescription
    
    def save(self):
        try:
            cursor.execute("""insert into transactiontype(code,description)values(%s,%s)
            on conflict(code)do update set code=%s,description=%s returning code""",
            (self.code,self.description,self.code,self.description,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Transaction:
    def __init__(self,typecode,holder_id,amount,payee_id=None,timecreated=None,timeupdated=None,memo=None):
        self.typecode=typecode
        self.holder_id=holder_id
        self.amount=amount
        self.payee_id=payee_id
        self.timecreated=timecreated
        self.timeupdated=timeupdated
        self.memo=memo
    
    def save(self):
        try:
            cursor.execute("""insert into transaction(typecode,holder_id,amount,payee_id,timecreated,
            timeupdated,memo)values(%s,%s,%s,%s,%s,%s,%s)returning transaction_id""",(self.typecode,
            self.holder_id,self.amount,self.payee_id,self.timecreated,self.timeupdated,self.memo,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Facctransaction:
    def __init__(self,transaction_id,faccount_id,crdr=None):
        self.transaction_id=transaction_id
        self.faccount_id=faccount_id
        self.crdr=crdr
    
    def save(self):
        try:
            cursor.execute("""insert into facctransaction(transaction_id,faccount_id,crdr)
            values(%s,%s,%s)on conflict(transaction_id,faccount_id)do update set transaction_id=%s,
            faccount_id=%s,crdr=%s returning transaction_id""",(self.transaction_id,self.faccount_id,
            self.crdr,self.transaction_id,self.faccount_id,self.crdr,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class InstallAccountClasses:
    def __init__(self,fname,language_id,member_id,timecreated=None):
        self.language_id=language_id
        self.member_id=member_id
        self.timecreated=timecreated
        self.fname=fname
    
    def isfilled(self):
        cursor.execute("select count(acclass_id)from acclass")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False
    
    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            df['language_id']=pd.Series([self.language_id]*df.shape[0])
            df['member_id']=pd.Series([self.member_id]*df.shape[0])
            df['timecreated']=pd.Series([self.timecreated]*df.shape[0])
            classvalues=df.values[:,[0,5,1,2,6]]
            classids=[Acclass(*x).save() for x in classvalues]
            df['acclass_id']=pd.Series(classids)
            descriptions=df.values[:,[7,4,3]]
            [Acclassdsc(*x).save() for x in descriptions]

class InstallAccounts:
    def __init__(self,fname,member_id,language_id):
        self.fname=fname
        self.member_id=member_id
        self.language_id=language_id
    
    def getclass(self,cname):
        cursor.execute("select acclass_id from acclass where name=%s",(cname,))
        res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res[0]
    
    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl);df['language_id']=pd.Series([self.language_id]*df.shape[0])
            df['member_id']=pd.Series([self.member_id]*df.shape[0])
            # accountnumber name currency description class language_id,member_id
            accounts=df.values
            faccount_ids=[Faccount(accounts[i][0],accounts[i][1],accounts[i][6],None,accounts[i][2]).save() for i in range(len(accounts))]
            [Faccountdsc(faccount_ids[i],accounts[i][5],accounts[i][3]).save() for i in range(len(accounts)) ]
            [Accountclassrel(self.getclass(accounts[i][4]),faccount_ids[i]).save() for i in range(len(accounts))]

transaction_types=[
    Transactiontype("PMT","Customer Payment","Customer payments"),
    Transactiontype("STMTCHG","Statement Charge","Statement charge billed to a customer"),
    Transactiontype("CREDMEM","Credit Memo","Credit memo issued by your business"),
    Transactiontype("RCPT","Sales Receipt","Generic code for sales receipts"),
    Transactiontype("ITMRCPT","Item Receipt","Specified an item receipt from a vendor without invoice"),
    Transactiontype("TAXPMT","Sales Tax Payment","Sales Tax Payment"),
    Transactiontype("BILL","Vendor Bill","Type represents a bill from a vendor that you're yet to play"),
    Transactiontype("BILLPMT","Paid Vendor Bill","Represents a bill from a vendor that you have paid"),
    Transactiontype("BILLCRED","Vendor Issued Credit","To show a credit given from a vendor"),
    Transactiontype("INV","Invoice","Stands for an invoice that you have issued to a customer or a vendor"),
    Transactiontype("PAYCHK","Paycheck","Identifies each paycheck issued to your employees"),
    Transactiontype("CCCHRG","Credit Card Charge","Represents a credit card charge"),
    Transactiontype("CCCRD","Credit Card Credit","Represents a credit card credit"),
    Transactiontype("LIABCHK","Liability Transaction","Shows payroll tax and other liability transactions"),
    Transactiontype("CHK","Check","Stands for checks"),
    Transactiontype("DEP","Deposit","Represents a deposit you've made to the bank"),
    Transactiontype("TRANSFR","Transfer","Represents a transfer you've made between two balance sheet registers"),
    Transactiontype("DISC","Discount","Identifies a discount given for early payment either to customers or vendors"),
    Transactiontype("GENJNRL","General Journal Entry","Stands for a general journal entry which you use when the other transaction types do not apply")]

class ConfirmTransaction:
    def __init__(self,holder_id,payee_id,referencenumber,transaction_id,status='N'):
        self.holder_id=holder_id
        self.payee_id=payee_id
        self.transaction_id=transaction_id
        self.referencenumber=referencenumber
        self.status=status
    
    def save(self):
        try:
            cursor.execute("""insert into confirmtransaction(holder_id,payee_id,referencenumber,
            status,transaction_id)values(%s,%s,%s,%s,%s)on conflict(holder_id,payee_id,referencenumber)
            do update set holder_id=%s,payee_id=%s,referencenumber=%s,status=%s,transaction_id=%s returning 
            payee_id""",(self.holder_id,self.payee_id,self.referencenumber,self.status,self.transaction_id,
            self.holder_id,self.payee_id,self.referencenumber,self.status,self.transaction_id,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
