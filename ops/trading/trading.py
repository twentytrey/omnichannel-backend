from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","jmso","localhost","5432")
import  importlib
import pandas as pd
import numpy as np
from ops import textualize_datetime,humanize_date,CurrencyHelper

# z=list(range(100))
# print( [z[i:i+10] for i in range(0,len(z),10)] )

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Trdtype:
    def __init__(self,trdtype_id,):
        self.trdtype_id=trdtype_id

    @staticmethod
    def read():
        cursor.execute("select trdtype_id,description from trdtypedsc");res=cursor.fetchall()
        if len(res) > 0:return [dict(value=x[0],text=x[1]) for x in res]
        elif len(res) <= 0:return [dict(value=None,text=None)]
    
    def save(self):
        try:
            cursor.execute("insert into trdtype(trdtype_id)values(%s)returning trdtype_id",(self.trdtype_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Trdtypedsc:
    def __init__(self,trdtype_id,language_id,description=None):
        self.trdtype_id=trdtype_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into trdtypedsc(trdtype_id,language_id,description)
            values(%s,%s,%s)on conflict(trdtype_id,language_id)do update set trdtype_id=%s,
            language_id=%s,description=%s returning trdtype_id""",(self.trdtype_id,self.language_id,
            self.description,self.trdtype_id,self.language_id,self.description,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

tradingstate=[dict(text="Inactive",value=0),dict(text="Active",value=1)]
creditallowed=[dict(text="No",value=0),dict(text="Yes",value=1)]
contractorigin=[dict(text="Manual",value=0),dict(text="Imported",value=1),dict(text="RFQ",value=2),
    dict(text="Exchange",value=3),dict(text="Auction",value=4),dict(text="2-Party Negotiation",value=5),
    dict(text="Deployment",value=6)]
contractstate=[dict(text="Draft",value=0),dict(text="Pending Approval",value=1),dict(text="Approved",value=2),
    dict(text="Active",value=3),dict(text="Rejected",value=4),dict(text="Canceled",value=5),
    dict(text="Closed",value=6),dict(text="Suspended",value=7)]
contractusage=[dict(text="Default",value=0),dict(text="Organizational Buyer",value=1),dict(text="Reseller",value=2),
    dict(text="Special Bid",value=3),dict(text="Referral",value=4),dict(text="Supplier",value=5)]
trdtypes=Trdtype.read()

class Participnt:
    def __init__(self,member_id,partrole_id,trading_id=None,termcond_id=None,information=None,
    timecreated=None,timeupdated=None):
        self.member_id=member_id
        self.partrole_id=partrole_id
        self.trading_id=trading_id
        self.termcond_id=termcond_id
        self.information=information
        self.timecreated=timecreated
        self.timeupdated=timeupdated

    @staticmethod
    def read(tid):
        cursor.execute("""select participnt.member_id,orgentity.orgentityname,participnt.partrole_id,
        partroleds.description,participnt.trading_id,participnt.termcond_id,participnt.information,
        participnt.timecreated,participnt.timeupdated from participnt inner join orgentity on 
        participnt.member_id=orgentity.orgentity_id inner join partroleds on participnt.partrole_id=
        partroleds.partrole_id where participnt.trading_id=%s""",(tid,));res=cursor.fetchone()
        if res != None:return dict(member_id=res[0],participant=res[1],partrole_id=res[2],
        role=res[3],trading_id=res[4],termcond_id=res[5],information=res[6],timecreated=textualize_datetime(res[7]),
        created_on=humanize_date(res[7]),timeupdated=textualize_datetime(res[8]),updated_on=humanize_date(res[8]))
    
    def save(self):
        try:
            cursor.execute("""insert into participnt(member_id,partrole_id,trading_id,termcond_id,information,timecreated,
            timeupdated)values(%s,%s,%s,%s,%s,%s,%s)on conflict(member_id,partrole_id,trading_id,termcond_id)do update 
            set member_id=%s,partrole_id=%s,trading_id=%s,termcond_id=%s,information=%s,timecreated=%s,timeupdated=%s 
            returning participnt_id""",(self.member_id,self.partrole_id,self.trading_id,self.termcond_id,self.information,self.timecreated,
            self.timeupdated,self.member_id,self.partrole_id,self.trading_id,self.termcond_id,self.information,self.timecreated,
            self.timeupdated,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Participnt.read(1))

class Trading:
    def __init__(self,trdtype_id,account_id=None,state=0,markfordelete=0,referencecount=0,
    starttime=None,endtime=None,creditallowed=0,reftrading_id=None):
        self.trdtype_id=trdtype_id
        self.account_id=account_id
        self.state=state
        self.markfordelete=markfordelete
        self.referencecount=referencecount
        self.starttime=starttime
        self.endtime=endtime
        self.creditallowed=creditallowed
        self.reftrading_id=reftrading_id
    
    @staticmethod
    def particpantname(mid):
        cursor.execute("select orgentityname from orgentity where orgentity_id=%s",(mid,))
        return cursor.fetchone()[0]
    
    @staticmethod
    def readaccounts(language_id):
        cursor.execute("""select trading.trading_id,trading.trdtype_id,trading.state,trading.starttime,
        trading.endtime,trading.creditallowed,trddesc.longdescription,trddesc.timecreated,trddesc.timeupdated,
        account.name,account.member_id,account.store_id,account.state,account.currency,account.comments,
        account.timecreated,account.timeupdated,account.timeapproved,account.timeactivated,
        orgentity.orgentityname,participnt.member_id from trading inner join 
        trddesc on trading.trading_id=trddesc.trading_id inner join account on trading.trading_id=account.account_id 
        inner join orgentity on account.member_id=orgentity.orgentity_id inner join participnt on trading.
        trading_id=participnt.trading_id where trddesc.language_id=%s and trading.trdtype_id=0""",(language_id,))
        res=cursor.fetchall()
        if len(res) <= 0:return [dict()]
        elif len(res) > 0:return [dict(trading_id=r[0],trdtype_id=r[1],tradingstate=r[2],
        tradingstarttime=textualize_datetime(r[3]),starting=humanize_date(r[3]),ending=humanize_date(r[4]),
        tradingendtime=textualize_datetime(r[4]),creditallowed=r[5],longdescription=r[6],
        tradingtimecreated=textualize_datetime(r[7]),created=humanize_date(r[7]),updated=humanize_date(r[8]),
        tradingtimeupdated=textualize_datetime(r[8]),
        type=[x['text'] for x in trdtypes if x['value']==r[1]][0],
        state=[x['text'] for x in tradingstate if x['value']==r[2]][0],
        credit=[x['text'] for x in creditallowed if x['value']==r[5]][0],
        stage=[x['text'] for x in contractstate if x['value']==r[12]][0],
        contract_title=r[9],contractmember_id=r[10],store_id=r[11],contractstate=r[12],
        currency=r[13],contractcomments=r[14],
        contracttimecreated=textualize_datetime(r[15]),contracttimeupdated=textualize_datetime(r[16]),
        contracttimeapproved=textualize_datetime(r[17]),contracttimeactivated=textualize_datetime(r[18]),
        created_by=r[19],participant=Trading.particpantname(r[20]))for r in res]

    @staticmethod
    def readdefaultcontracts(language_id):
        cursor.execute("""select trading.trading_id,trading.trdtype_id,trading.state,trading.starttime,
        trading.endtime,trading.creditallowed,trddesc.longdescription,trddesc.timecreated,trddesc.timeupdated,
        contract.name,contract.member_id,contract.origin,contract.state,contract.usage,contract.comments,
        contract.timecreated,contract.timeapproved,contract.timeactivated,contract.timedeployed,
        orgentity.orgentityname,participnt.member_id from trading inner join 
        trddesc on trading.trading_id=trddesc.trading_id inner join contract on trading.trading_id=contract.contract_id
        inner join orgentity on contract.member_id=orgentity.orgentity_id inner join participnt on trading.
        trading_id=participnt.trading_id where trddesc.language_id=%s and trading.trdtype_id=1 and contract.usage<=0""",
        (language_id,));res=cursor.fetchall()
        if len(res) <= 0: return [dict()]
        elif len(res) > 0:return [dict(trading_id=r[0],trdtype_id=r[1],tradingstate=r[2],
        tradingstarttime=textualize_datetime(r[3]),starting=humanize_date(r[3]),ending=humanize_date(r[4]),
        tradingendtime=textualize_datetime(r[4]),creditallowed=r[5],longdescription=r[6],
        tradingtimecreated=textualize_datetime(r[7]),created=humanize_date(r[7]),updated=humanize_date(r[8]),
        tradingtimeupdated=textualize_datetime(r[8]),
        type=[x['text'] for x in trdtypes if x['value']==r[1]][0],
        state=[x['text'] for x in tradingstate if x['value']==r[2]][0],
        origin=[x['text'] for x in contractorigin if x['value']==r[11]][0],
        credit=[x['text'] for x in creditallowed if x['value']==r[5]][0],
        stage=[x['text'] for x in contractstate if x['value']==r[12]][0],
        contract_title=r[9],contractmember_id=r[10],contractorigin=r[11],contractstate=r[12],contractusage=r[13],
        contractcomments=r[14],contracttimecreated=textualize_datetime(r[15]),_rowVariant='success',
        contracttimeapproved=textualize_datetime(r[16]),approved=humanize_date(r[16]),
        contracttimeactivated=textualize_datetime(r[17]),activated=humanize_date(r[17]),deployed=humanize_date(r[18]),
        contracttimedeployed=textualize_datetime(r[18]),created_by=r[19],participant=Trading.particpantname(r[20])
        ) for r in res]

    @staticmethod
    def readcontracts(language_id):
        cursor.execute("""select trading.trading_id,trading.trdtype_id,trading.state,trading.starttime,
        trading.endtime,trading.creditallowed,trddesc.longdescription,trddesc.timecreated,trddesc.timeupdated,
        contract.name,contract.member_id,contract.origin,contract.state,contract.usage,contract.comments,
        contract.timecreated,contract.timeapproved,contract.timeactivated,contract.timedeployed,
        orgentity.orgentityname,participnt.member_id from trading inner join 
        trddesc on trading.trading_id=trddesc.trading_id inner join contract on trading.trading_id=contract.contract_id
        inner join orgentity on contract.member_id=orgentity.orgentity_id inner join participnt on trading.
        trading_id=participnt.trading_id where trddesc.language_id=%s and trading.trdtype_id=1 and contract.usage>0""",
        (language_id,));res=cursor.fetchall()
        if len(res) <= 0: return [dict()]
        elif len(res) > 0:return [dict(trading_id=r[0],trdtype_id=r[1],tradingstate=r[2],
        tradingstarttime=textualize_datetime(r[3]),starting=humanize_date(r[3]),ending=humanize_date(r[4]),
        tradingendtime=textualize_datetime(r[4]),creditallowed=r[5],longdescription=r[6],
        tradingtimecreated=textualize_datetime(r[7]),created=humanize_date(r[7]),updated=humanize_date(r[8]),
        tradingtimeupdated=textualize_datetime(r[8]),
        type=[x['text'] for x in trdtypes if x['value']==r[1]][0],
        state=[x['text'] for x in tradingstate if x['value']==r[2]][0],
        origin=[x['text'] for x in contractorigin if x['value']==r[11]][0],
        credit=[x['text'] for x in creditallowed if x['value']==r[5]][0],
        stage=[x['text'] for x in contractstate if x['value']==r[12]][0],
        contract_title=r[9],contractmember_id=r[10],contractorigin=r[11],contractstate=r[12],contractusage=r[13],
        contractcomments=r[14],contracttimecreated=textualize_datetime(r[15]),
        contracttimeapproved=textualize_datetime(r[16]),approved=humanize_date(r[16]),
        contracttimeactivated=textualize_datetime(r[17]),activated=humanize_date(r[17]),deployed=humanize_date(r[18]),
        contracttimedeployed=textualize_datetime(r[18]),created_by=r[19],participant=Trading.particpantname(r[20])) for r in res]
    
    @staticmethod
    def readcontract(tid,lid):
        cursor.execute("""select 
        trading.trading_id,trading.trdtype_id,trading.state,trading.starttime,trading.endtime,trading.creditallowed,
        trddesc.longdescription,trddesc.timecreated,trddesc.timeupdated,
        contract.name,contract.member_id,orgentity.orgentityname,contract.origin,contract.state,contract.usage,
        contract.timeapproved,contract.timeactivated,contract.timedeployed,
        participnt.member_id,participnt.partrole_id,partroleds.description,storecntr.store_id
        from trading inner join trddesc on trading.trading_id=trddesc.trading_id 
        inner join contract on trading.trading_id=contract.contract_id 
        inner join storecntr on trading.trading_id=storecntr.contract_id
        inner join orgentity on contract.member_id=orgentity.orgentity_id 
        inner join participnt on trading.trading_id=participnt.trading_id
        inner join partroleds on participnt.partrole_id=partroleds.partrole_id
        where trading.trading_id=%s and trddesc.language_id=%s""",(tid,lid,))
        res=cursor.fetchone()
        if len(res) <= 0:return dict()
        elif len(res) > 0:return dict(trading_id=res[0],trdtype_id=res[1],
        trdtype_str=[x['text'] for x in trdtypes if x['value']==res[1]][0],
        trading_state=res[2],tradingstate=[x['text'] for x in tradingstate if x['value']==res[2]][0],
        trading_starttime=textualize_datetime(res[3]),trading_starts=humanize_date(res[3]),
        trading_endtime=textualize_datetime(res[4]),trading_ends=humanize_date(res[4]),
        trading_creditallowed=res[5],creditallowed=[x['text'] for x in creditallowed if x['value']==res[5]][0],
        description_comment=res[6],trading_timecreated=textualize_datetime(res[7]),created_on=humanize_date(res[7]),
        trading_timeupdated=textualize_datetime(res[8]),updated_on=humanize_date(res[8]),contract_name=res[9],
        contract_member_id=res[10],owner=res[11],contract_origin=res[12],origin=[x['text'] for x in contractorigin if x['value']==res[12]][0],
        contract_state=res[13],stage=[x['text'] for x in contractstate if x['value']==res[13]][0],contract_usage=res[14],
        usage=[x['text'] for x in contractusage if x['value']==res[14]][0],contract_timeapproved=textualize_datetime(res[15]),
        approved_on=humanize_date(res[15]),contract_timeactivated=textualize_datetime(res[16]),activated_on=humanize_date(res[16]),
        contract_timedeployed=textualize_datetime(res[17]),deployed_on=humanize_date(res[17]),participant_id=res[18],
        participant=Trading.particpantname(res[18]),partrole_id=res[19],participant_role=res[20],store_id=res[21])

    @staticmethod
    def read(tid,lid):
        cursor.execute("""select trading.trading_id,trading.trdtype_id,trading.account_id,trading.state,
        trading.markfordelete,trading.referencecount,trading.starttime,trading.endtime,trading.creditallowed,
        trading.reftrading_id,trddesc.description as code,trddesc.longdescription as description,trddesc.timecreated,
        trddesc.timeupdated from trading inner join trddesc on trading.trading_id=trddesc.trading_id where trading.
        trading_id=%s and trddesc.language_id=%s""",(tid,lid,));res=cursor.fetchone()
        if res==None:return dict(trading_id=None,trdtype_id=None,account_id=None,state=None,markfordelete=None,
        referencecount=None,starttime=None,endtime=None,creditallowed=None,reftrading_id=None,code=None,description=None,
        timecreated=None,timeupdated=None,contract=None,participant=None)
        elif res != None:return dict(trading_id=res[0],trdtype_id=res[1],account_id=res[2],state=res[3],
        trdtype_str=[x['text'] for x in trdtypes if x['value']==res[1]][0],
        state_str=[x['text'] for x in tradingstate if x['value']==res[3]][0],
        markfordelete=res[4],referencecount=res[5],starttime=textualize_datetime(res[6]),starttime_str=humanize_date(res[6]),
        endtime=textualize_datetime(res[7]),endtime_str=humanize_date(res[7]),creditallowed=res[8],
        creditallowed_str=[x['text'] for x in creditallowed if x['value']==res[8]][0],
        reftrading_id=res[9],code=res[10],description=res[11],timecreated=textualize_datetime(res[12]),
        timeupdated=textualize_datetime(res[13]),contract=Contract.read(res[0]),participant=Participnt.read(res[0]))
    
    def save(self):
        try:
            cursor.execute("""insert into trading(trdtype_id,account_id,state,markfordelete,
            referencecount,starttime,endtime,creditallowed,reftrading_id)values(%s,%s,%s,%s,%s,
            %s,%s,%s,%s)returning trading_id""",(self.trdtype_id,self.account_id,self.state,
            self.markfordelete,self.referencecount,self.starttime,self.endtime,self.creditallowed,
            self.reftrading_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Trddesc:
    def __init__(self,trading_id,language_id,description=None,longdescription=None,
    timecreated=None,timeupdated=None):
        self.trading_id=trading_id
        self.language_id=language_id
        self.description=description
        self.longdescription=longdescription
        self.timecreated=timecreated
        self.timeupdated=timeupdated

    def save(self):
        try:
            cursor.execute("""insert into trddesc(trading_id,language_id,description,longdescription,
            timecreated,timeupdated)values(%s,%s,%s,%s,%s,%s)on conflict(trading_id,language_id)
            do update set trading_id=%s,language_id=%s,description=%s,longdescription=%s,timecreated=%s,
            timeupdated=%s returning trading_id""",(self.trading_id,self.language_id,self.description,
            self.longdescription,self.timecreated,self.timeupdated,self.trading_id,self.language_id,self.description,
            self.longdescription,self.timecreated,self.timeupdated,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Account:
    def __init__(self,account_id,name,member_id,store_id=None,state=0,currency=None,defaultcontract=0,
    markfordelete=0,comments=None,timecreated=None,timeupdated=None,timeapproved=None,
    timeactivated=None,prcplcypref=None,userprcplcypref=None):
        self.account_id=account_id
        self.name=name
        self.member_id=member_id
        self.store_id=store_id
        self.state=state
        self.currency=currency
        self.defaultcontract=defaultcontract
        self.markfordelete=markfordelete
        self.comments=comments
        self.timecreated=timecreated
        self.timeupdated=timeupdated
        self.timeapproved=timeapproved
        self.timeactivated=timeactivated
        self.prcplcypref=prcplcypref
        self.userprcplcypref=userprcplcypref
        # 15
    
    def save(self):
        try:
            cursor.execute("""insert into account(account_id,name,member_id,store_id,state,currency,
            defaultcontract,markfordelete,comments,timecreated,timeupdated,timeapproved,timeactivated,
            prcplcypref,userprcplcypref)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict
            (account_id,name,member_id)do update set account_id=%s,name=%s,member_id=%s,store_id=%s,
            state=%s,currency=%s,defaultcontract=%s,markfordelete=%s,comments=%s,timecreated=%s,timeupdated=%s,
            timeapproved=%s,timeactivated=%s,prcplcypref=%s,userprcplcypref=%s returning account_id""",
            (self.account_id,self.name,self.member_id,self.store_id,self.state,self.currency,self.defaultcontract,
            self.markfordelete,self.comments,self.timecreated,self.timeupdated,self.timeapproved,self.timeactivated,
            self.prcplcypref,self.userprcplcypref,
            self.account_id,self.name,self.member_id,self.store_id,self.state,self.currency,self.defaultcontract,
            self.markfordelete,self.comments,self.timecreated,self.timeupdated,self.timeapproved,self.timeactivated,
            self.prcplcypref,self.userprcplcypref,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Contract:
    def __init__(self,contract_id,name,member_id,majorversion=1,minorversion=0,origin=0,
    state=0,usage=0,markfordelete=0,comments=None,timecreated=None,timeupdated=None,
    timeapproved=None,timeactivated=None,timedeployed=None,family_id=None):
        self.contract_id=contract_id
        self.majorversion=majorversion
        self.minorversion=minorversion
        self.name=name
        self.member_id=member_id
        self.origin=origin
        self.state=state
        self.usage=usage
        self.markfordelete=markfordelete
        self.comments=comments
        self.timecreated=timecreated
        self.timeupdated=timeupdated
        self.timeapproved=timeapproved
        self.timeactivated=timeactivated
        self.timedeployed=timedeployed
        self.family_id=family_id

    @staticmethod
    def code():
        cursor.execute("select trading_id from trading order by trading_id desc limit 1")
        res=cursor.fetchone()
        if res==None:return 'PR/CO/{0}'.format(1)
        elif res !=None:return 'PR/CO/{0}'.format(res[0]+1)
    
    def save(self):
        try:
            cursor.execute("""insert into contract(contract_id,majorversion,minorversion,name,member_id,origin,state,
            usage,markfordelete,comments,timecreated,timeupdated,timeapproved,timeactivated,timedeployed,family_id)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(name,member_id,majorversion,minorversion,
            origin)do update set contract_id=%s,majorversion=%s,minorversion=%s,name=%s,member_id=%s,origin=%s,state=%s,
            usage=%s,markfordelete=%s,comments=%s,timecreated=%s,timeupdated=%s,timeapproved=%s,timeactivated=%s,
            timedeployed=%s,family_id=%s returning contract_id""",(self.contract_id,self.majorversion,self.minorversion,
            self.name,self.member_id,self.origin,self.state,self.usage,self.markfordelete,self.comments,self.timecreated,
            self.timeupdated,self.timeapproved,self.timeactivated,self.timedeployed,self.family_id,
            self.contract_id,self.majorversion,self.minorversion,
            self.name,self.member_id,self.origin,self.state,self.usage,self.markfordelete,self.comments,self.timecreated,
            self.timeupdated,self.timeapproved,self.timeactivated,self.timedeployed,self.family_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    @staticmethod
    def read(contract_id):
        cursor.execute("""select contract.contract_id,contract.majorversion,contract.minorversion,contract.name,
        contract.member_id,contract.origin,contract.state,contract.usage,contract.markfordelete,contract.comments,
        contract.timecreated,contract.timeupdated,contract.timeapproved,contract.timeactivated,contract.timedeployed,
        contract.family_id,orgentity.orgentityname from contract inner join orgentity on contract.member_id=orgentity.
        orgentity_id where contract_id=%s""",(contract_id,));res=cursor.fetchone()
        if res==None:return dict(contract_id=None,majorversion=None,minorversion=None,name=None,member_id=None,
        origin=None,state=None,usage=None,markfordelete=None,comments=None,timecreated=None,timeupdated=None,
        timeapproved=None,timeactivated=None,timedeployed=None,family_id=None,owner=None)
        elif res != None:return dict(contract_id=res[0],majorversion=res[1],minorversion=res[2],name=res[3],member_id=res[4],
        origin=res[5],state=res[6],usage=res[7],markfordelete=res[8],comments=res[9],created_on=humanize_date(res[10]),
        origin_str=[x['text'] for x in contractorigin if x['value']==res[5]][0],
        timecreated=textualize_datetime(res[10]),updated_on=humanize_date(res[11]),timeupdated=textualize_datetime(res[11]),
        state_str=[x['text'] for x in contractstate if x['value']==res[6]][0],approved_on=humanize_date(res[12]),
        timeapproved=textualize_datetime(res[12]),activated_on=humanize_date(res[13]),timeactivated=textualize_datetime(res[13]),
        deployed_on=humanize_date(res[14]),timedeployed=textualize_datetime(res[14]),family_id=res[15],owner=res[16])

# print(Contract.read(1))

class Cntrname:
    def __init__(self,name,member_id,origin):
        self.name=name
        self.member_id=member_id
        self.origin=origin
    
    def save(self):
        try:
            cursor.execute("""insert into cntrname(name,member_id,origin)values(%s,%s,%s)on conflict
            (name,member_id,origin)do update set name=%s,member_id=%s,origin=%s returning name""",
            (self.name,self.member_id,self.origin,self.name,self.member_id,self.origin,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Attachment:
    def __init__(self,attachmenturl,member_id,attachusg_id,mimetype,mimetypeencoding,timecreated,timeupdated,
    markfordelete,description,filename,filesize,createmethod,image1,image2,content,reserved):
        self.attachmenturl=attachmenturl
        self.member_id=member_id
        self.attachusg_id=attachusg_id
        self.mimetype=mimetype
        self.mimetypeencoding=mimetypeencoding
        self.timecreated=timecreated
        self.timeupdated=timeupdated
        self.markfordelete=markfordelete
        self.description=description
        self.filename=filename
        self.filesize=filesize
        self.createmethod=createmethod
        self.image1=image1
        self.image2=image2
        self.content=content
        self.reserved=reserved
    
    def save(self):
        try:
            cursor.execute("""insert into attachment(attachmenturl,member_id,attachusg_id,mimetype,mimetypeencoding,
            timecreated,timeupdated,markfordelete,description,filename,filesize,createmethod,image1,image2,content,
            reserved)on conflict(attachmenturl)do update set attachmenturl=%s,member_id=%s,attachusg_id=%s,mimetype=%s,
            mimetypeencoding=%s,timecreated=%s,timeupdated=%s,markfordelete=%s,description=%s,filename=%s,filesize=%s,
            createmethod=%s,image1=%s,image2=%s,content=%s,reserved=%s""",(self.attachmenturl,self.member_id,
            self.attachusg_id,self.mimetype,self.mimetypeencoding,self.timecreated,self.timeupdated,self.markfordelete,
            self.description,self.filename,self.filesize,self.createmethod,self.image1,self.image2,self.content,
            self.reserved,self.attachmenturl,self.member_id,self.attachusg_id,self.mimetype,self.mimetypeencoding,
            self.timecreated,self.timeupdated,self.markfordelete,self.description,self.filename,self.filesize,
            self.createmethod,self.image1,self.image2,self.content,self.reserved,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Attachusg:
    def __init__(self,attachusg_id):
        self.attachusg_id=attachusg_id
    
    def save(self):
        try:
            cursor.execute("""insert into attachusg(attachusg_id)values(%s)on conflict(attachusg_id)
            do update set attachusg_id=%s returning attachusg_id""",(self.attachusg_id,self.attachusg_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Trdattach:
    def __init__(self,trading_id,attachment_id):
        self.trading_id=trading_id
        self.attachment_id=attachment_id
    
    def save(self):
        try:
            cursor.execute("""insert into trdattach(trading_id,attachment_id)values(%s,%s)on conflict
            (trading_id,attachment_id)do update set trading_id=%s,attachment_id=%s returning trading_id""",
            (self.trading_id,self.attachment_id,self.trading_id,self.attachment_id,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Termcond:
    def __init__(self,tcsubtype_id,trading_id,mandatory=0,changeable=0,timecreated=None,timeupdated=None,stringfield1=None,
    stringfield2=None,stringfield3=None,integerfield1=None,integerfield2=None,integerfield3=None,bigintfield1=None,
    bigintfield2=None,bigintfield3=None,floatfield1=None,floatfield2=None,floatfield3=None,timefield1=None,
    timefield2=None,timefield3=None,decimalfield1=None,decimalfield2=None,decimalfield3=None,sequence=0):
        self.tcsubtype_id=tcsubtype_id
        self.trading_id=trading_id
        self.mandatory=mandatory
        self.changeable=changeable
        self.timecreated=timecreated
        self.timeupdated=timeupdated
        self.stringfield1=stringfield1
        self.stringfield2=stringfield2
        self.stringfield3=stringfield3
        self.integerfield1=integerfield1
        self.integerfield2=integerfield2
        self.integerfield3=integerfield3
        self.bigintfield1=bigintfield1
        self.bigintfield2=bigintfield2
        self.bigintfield3=bigintfield3
        self.floatfield1=floatfield1
        self.floatfield2=floatfield2
        self.floatfield3=floatfield3
        self.timefield1=timefield1
        self.timefield2=timefield2
        self.timefield3=timefield3
        self.decimalfield1=decimalfield1
        self.decimalfield2=decimalfield2
        self.decimalfield3=decimalfield3
        self.sequence=sequence
    
    def save(self):
        try:
            cursor.execute("""insert into termcond(tcsubtype_id,trading_id,mandatory,changeable,timecreated,timeupdated,
            stringfield1,stringfield2,stringfield3,integerfield1,integerfield2,integerfield3,bigintfield1,bigintfield2,
            bigintfield3,floatfield1,floatfield2,floatfield3,timefield1,timefield2,timefield3,decimalfield1,decimalfield2,
            decimalfield3,sequence)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            on conflict(trading_id,tcsubtype_id)do update set tcsubtype_id=%s,trading_id=%s,mandatory=%s,changeable=%s,
            timecreated=%s,timeupdated=%s,stringfield1=%s,stringfield2=%s,stringfield3=%s,integerfield1=%s,integerfield2=%s,
            integerfield3=%s,bigintfield1=%s,bigintfield2=%s,bigintfield3=%s,floatfield1=%s,floatfield2=%s,floatfield3=%s,
            timefield1=%s,timefield2=%s,timefield3=%s,decimalfield1=%s,decimalfield2=%s,decimalfield3=%s,sequence=%s
            returning termcond_id""",(self.tcsubtype_id,self.trading_id,self.mandatory,self.changeable,self.timecreated,
            self.timeupdated,self.stringfield1,self.stringfield2,self.stringfield3,self.integerfield1,self.integerfield2,
            self.integerfield3,self.bigintfield1,self.bigintfield2,self.bigintfield3,self.floatfield1,self.floatfield2,
            self.floatfield3,self.timefield1,self.timefield2,self.timefield3,self.decimalfield1,self.decimalfield2,
            self.decimalfield3,self.sequence,
            self.tcsubtype_id,self.trading_id,self.mandatory,self.changeable,self.timecreated,
            self.timeupdated,self.stringfield1,self.stringfield2,self.stringfield3,self.integerfield1,self.integerfield2,
            self.integerfield3,self.bigintfield1,self.bigintfield2,self.bigintfield3,self.floatfield1,self.floatfield2,
            self.floatfield3,self.timefield1,self.timefield2,self.timefield3,self.decimalfield1,self.decimalfield2,
            self.decimalfield3,self.sequence,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Tcattr:
    def __init__(self,termcond_id,ttype,trading_id,xmldefinition,sequence=0):
        self.termcond_id=termcond_id
        self.type=ttype
        self.trading_id=trading_id
        self.xmldefinition=xmldefinition
        self.sequence=sequence
    
    def save(self):
        try:
            cursor.execute("""insert into tcattr(termcond_id,type,trading_id,sequence,xmldefinition)
            values(%s,%s,%s,%s,%s)on conflict(termcond_id,type,sequence)do update set termcond_id=%s,type=%s,
            trading_id=%s,sequence=%s,xmldefinition=%s returning termcond_id""",(self.termcond_id,self.type,
            self.trading_id,self.sequence,self.xmldefinition,self.termcond_id,self.type,self.trading_id,
            self.sequence,self.xmldefinition,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Tctype:
    def __init__(self,tctype_id):
        self.tctype_id=tctype_id
    
    def save(self):
        try:
            cursor.execute("""insert into tctype(tctype_id)values(%s)on conflict(tctype_id)
            do update set tctype_id=%s returning tctype_id""",(self.tctype_id,self.tctype_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Tcsubtype:
    def __init__(self,tcsubtype_id,tctype_id,accessbeanname=None,deploycommand=None):
        self.tcsubtype_id=tcsubtype_id
        self.tctype_id=tctype_id
        self.accessbeanname=accessbeanname
        self.deploycommand=deploycommand
    
    def save(self):
        try:
            cursor.execute("""insert into tcsubtype(tcsubtype_id,tctype_id,accessbeanname,deploycommand)
            values(%s,%s,%s,%s)on conflict(tcsubtype_id)do update set tcsubtype_id=%s,tctype_id=%s,
            accessbeanname=%s,deploycommand=%s returning tcsubtype_id""",(self.tcsubtype_id,self.tctype_id,
            self.accessbeanname,self.deploycommand,self.tcsubtype_id,self.tctype_id,self.accessbeanname,
            self.deploycommand,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Tcsubtypds:
    def __init__(self,tcsubtype_id,language_id,description=None):
        self.tcsubtype_id=tcsubtype_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into tcsubtypds(tcsubtype_id,language_id,description)values(%s,%s,%s)
            on conflict(tcsubtype_id,language_id)do update set tcsubtype_id=%s,language_id=%s,description=%s
            returning tcsubtype_id""",(self.tcsubtype_id,self.language_id,self.description,self.tcsubtype_id,
            self.language_id,self.description,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Partrole:
    def __init__(self,partrole_id):
        self.partrole_id=partrole_id
    
    def save(self):
        try:
            cursor.execute("""insert into partrole(partrole_id)values(%s)on conflict(partrole_id)
            do update set partrole_id=%s returning partrole_id""",(self.partrole_id,self.partrole_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Partroleds:
    def __init__(self,partrole_id,language_id,description=None):
        self.partrole_id=partrole_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into partroleds(partrole_id,language_id,description)values(%s,%s,%s)
            on conflict(partrole_id,language_id)do update set partrole_id=%s,language_id=%s,description=%s
            returning partrole_id""",(self.partrole_id,self.language_id,self.description,
            self.partrole_id,self.language_id,self.description,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Tcdesc:
    def __init__(self,termcond_id,language_id,description=None,longdescription=None,timecreated=None,timeupdated=None):
        self.termcond_id=termcond_id
        self.language_id=language_id
        self.description=description
        self.longdescription=longdescription
        self.timecreated=timecreated
        self.timeupdated=timeupdated
    
    def save(self):
        try:
            cursor.execute("""insert into tcdesc(termcond_id,language_id,description,longdescription,timecreated,
            timeupdated)values(%s,%s,%s,%s,%s,%s)on conflict(termcond_id,language_id)do update set termcond_id=%s,
            language_id=%s,description=%s,longdescription=%s,timecreated=%s,timeupdated=%s""",(self.termcond_id,
            self.language_id,self.description,self.longdescription,self.timecreated,self.timeupdated,self.termcond_id,
            self.language_id,self.description,self.longdescription,self.timecreated,self.timeupdated,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Policytc:
    def __init__(self,termcond_id,policy_id):
        self.termcond_id=termcond_id
        self.policy_id=policy_id
    
    def save(self):
        try:
            cursor.execute("""insert into policytc(termcond_id,policy_id)values(%s,%s)on conflict
            (policy_id,termcond_id)do update set termcond_id=%s,policy_id=%s returning termcond_id""",
            (self.termcond_id,self.policy_id,self.termcond_id,self.policy_id,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Policy:
    def __init__(self,policyname,policytype_id,storeent_id,properties=None,starttime=None,endtime=None):
        self.policyname=policyname
        self.policytype_id=policytype_id
        self.storeent_id=storeent_id
        self.properties=properties
        self.starttime=starttime
        self.endtime=endtime
    
    def save(self):
        try:
            cursor.execute("""insert into policy(policyname,policytype_id,storeent_id,properties,starttime,
            endtime)values(%s,%s,%s,%s,%s,%s)on conflict(policyname,policytype_id,storeent_id)do update set 
            policyname=%s,policytype_id=%s,storeent_id=%s,properties=%s,starttime=%s,endtime=%s returning
            policy_id""",(self.policyname,self.policytype_id,self.storeent_id,self.properties,self.starttime,
            self.endtime,self.policyname,self.policytype_id,self.storeent_id,self.properties,self.starttime,
            self.endtime,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Policydesc:
    def __init__(self,policy_id,language_id,description,longdescription=None,timecreated=None,timeupdated=None):
        self.policy_id=policy_id
        self.language_id=language_id
        self.description=description
        self.longdescription=longdescription
        self.timecreated=timecreated
        self.timeupdated=timeupdated
    
    def save(self):
        try:
            cursor.execute("""insert into policydesc(policy_id,language_id,description,longdescription,timecreated,
            timeupdated)values(%s,%s,%s,%s,%s,%s)on conflict(policy_id,language_id)do update set policy_id=%s,language_id=%s,
            description=%s,longdescription=%s,timecreated=%s,timeupdated=%s returning policy_id""",(self.policy_id,self.language_id,
            self.description,self.longdescription,self.timecreated,self.timeupdated,self.policy_id,self.language_id,
            self.description,self.longdescription,self.timecreated,self.timeupdated,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Policytype:
    def __init__(self,policytype_id):
        self.policytype_id=policytype_id
    
    def save(self):
        try:
            cursor.execute("""insert into policytype(policytype_id)values(%s)on conflict(policytype_id)
            do update set policytype_id=%s returning policytype_id""",(self.policytype_id,self.policytype_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Plcytypdsc:
    def __init__(self,policytype_id,language_id,description=None):
        self.policytype_id=policytype_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into plcytypdsc(policytype_id,language_id,description)values(%s,%s,%s)
            on conflict(policytype_id,language_id)do update set policytype_id=%s,language_id=%s,description=%s
            returning policytype_id""",(self.policytype_id,self.language_id,self.description,self.policytype_id,
            self.language_id,self.description,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Fileupload:
    def __init__(self,filepath,member_id=None,store_id=None,sccjobrefnum=None,filename=None,filesize=None,filetype=None,
    fileencoding=None,uploadtime=None,hostname=None,version=None,status=0):
        self.filepath=filepath
        self.member_id=member_id
        self.store_id=store_id
        self.sccjobrefnum=sccjobrefnum
        self.filename=filename
        self.filesize=filesize
        self.filetype=filetype
        self.fileencoding=fileencoding
        self.uploadtime=uploadtime
        self.hostname=hostname
        self.version=version
        self.status=status
    
    def save(self):
        try:
            cursor.execute("""insert into fileupload(member_id,store_id,sccjobrefnum,filepath,filename,filesize,
            filetype,fileencoding,uploadtime,hostname,version,status)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            on conflict(filepath,version)do update set member_id=%s,store_id=%s,sccjobrefnum=%s,filepath=%s,filename=%s,
            filesize=%s,filetype=%s,fileencoding=%s,uploadtime=%s,hostname=%s,version=%s,status=%s""",(self.member_id,
            self.store_id,self.sccjobrefnum,self.filepath,self.filename,self.filesize,self.filetype,self.fileencoding,
            self.uploadtime,self.hostname,self.version,self.status,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Storedef:
    def __init__(self,store_id,contract_id=None,shipmode_id=None):
        self.store_id=store_id
        self.contract_id=contract_id
        self.shipmode_id=shipmode_id
    
    def save(self):
        try:
            cursor.execute("""insert into storedef(store_id,contract_id,shipmode_id)values(%s,%s,%s)
            on conflict(store_id)do update set store_id=%s,contract_id=%s,shipmode_id=%s returning contract_id""",
            (self.store_id,self.contract_id,self.shipmode_id,self.store_id,self.contract_id,self.shipmode_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Storecntr:
    def __init__(self,contract_id,store_id):
        self.contract_id=contract_id
        self.store_id=store_id
    
    def save(self):
        try:
            cursor.execute("""insert into storecntr(contract_id,store_id)values(%s,%s)on conflict
            (contract_id,store_id)do update set contract_id=%s,store_id=%s returning contract_id""",
            (self.contract_id,self.store_id,self.contract_id,self.store_id,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Tdpscncntr:
    def __init__(self,tradeposcn_id,contract_id):
        self.tradeposcn_id=tradeposcn_id
        self.contract_id=contract_id
    
    def save(self):
        try:
            cursor.execute("""insert into tdpscncntr(tradeposcn_id,contract_id)values(%s,%s)
            on conflict(contract_id,tradeposcn_id)do update set tradeposcn_id=%s,contract_id=%s
            returning tradeposcn_id""",(self.tradeposcn_id,self.contract_id,self.tradeposcn_id,self.contract_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catcntr:
    def __init__(self,catalog_id,contract_id):
        self.catalog_id=catalog_id
        self.contract_id=contract_id
    
    def save(self):
        try:
            cursor.execute("""insert into catcntr(catalog_id,contract_id)values(%s,%s)
            on conflict(contract_id,catalog_id)do update set catalog_id=%s,contract_id=%s
            returning catalog_id""",(self.catalog_id,self.contract_id,self.catalog_id,self.contract_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Tradeposcn:
    def __init__(self,member_id,name,productset_id=None,description=None,precedence=0,markfordelete=0,ttype='S',flags=0):
        self.member_id=member_id
        self.productset_id=productset_id
        self.name=name
        self.description=description
        self.precedence=precedence
        self.markfordelete=markfordelete
        self.type=ttype
        self.flags=flags
    
    @staticmethod
    def read(member_id,trading_id):
        cursor.execute("""with tradepositions as(select tradeposcn_id from tdpscncntr where contract_id=%s)
        select tradepositions.tradeposcn_id,tradeposcn.member_id,tradeposcn.productset_id,tradeposcn.description,
        tradeposcn.name,tradeposcn.precedence,tradeposcn.markfordelete,tradeposcn.type,tradeposcn.flags from
        tradepositions inner join tradeposcn on tradepositions.tradeposcn_id=tradeposcn.tradeposcn_id where tradeposcn.
        member_id=%s""",(trading_id,member_id,));res=cursor.fetchall()
        if len(res) <= 0:return [dict()]
        elif len(res) > 0:return [dict(tradeposcn_id=r[0],member_id=r[1],productset_id=r[2],description=r[3],
        name=r[4],precedence=r[5],markfordelete=r[6],type=r[7],flags=r[8])for r in res]

    def save(self):
        try:
            cursor.execute("""insert into tradeposcn(member_id,productset_id,description,name,precedence,markfordelete,
            type,flags)values(%s,%s,%s,%s,%s,%s,%s,%s)on conflict(member_id,name)do update set member_id=%s,productset_id=%s,
            description=%s,name=%s,precedence=%s,markfordelete=%s,type=%s,flags=%s returning tradeposcn_id""",(self.member_id,
            self.productset_id,self.description,self.name,self.precedence,self.markfordelete,self.type,self.flags,
            self.member_id,self.productset_id,self.description,self.name,self.precedence,self.markfordelete,self.type,self.flags,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

# print( Tradeposcn.read(1,20) )

class Productset:
    def __init__(self,member_id,name=None,xmldefinition=None,publishtime=None,markfordelete=0,static=None):
        self.member_id=member_id
        self.name=name
        self.xmldefinition=xmldefinition
        self.publishtime=publishtime
        self.markfordelete=markfordelete
        self.static=static
    
    def save(self):
        try:
            cursor.execute("""insert into productset(name,member_id,xmldefinition,publishtime,markfordelete,
            static)values(%s,%s,%s,%s,%s,%s)on conflict(name,member_id)do update set name=%s,member_id=%s,xmldefinition=%s,
            publishtime=%s,markfordelete=%s,static=%s returning productset_id""",
            (self.name,self.member_id,self.xmldefinition,self.publishtime,self.markfordelete,self.static,
            self.name,self.member_id,self.xmldefinition,self.publishtime,self.markfordelete,self.static,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Prsetcerel:
    def __init__(self,productset_id,catentry_id):
        self.productset_id=productset_id
        self.catentry_id=catentry_id
    
    def save(self):
        try:
            cursor.execute("""insert into prsetcerel(productset_id,catentry_id)values(%s,%s)on conflict
            (productset_id,catentry_id)do update set productset_id=%s,catentry_id=%s returning productset_id""",
            (self.productset_id,self.catentry_id,self.productset_id,self.catentry_id,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Prodsetdsc:
    def __init__(self,productset_id,language_id,description=None):
        self.productset_id=productset_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into prodsetdsc(productset_id,language_id,description)values(%s,%s,%s)
            on conflict(productset_id,language_id)do update set productset_id=%s,language_id=%s,description=%s
            returning productset_id""",(self.productset_id,self.language_id,self.description,self.productset_id,
            self.language_id,self.description,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Psetadjmnt:
    def __init__(self,termcond_id,productset_id,ttype,adjustment=0,precedence=0):
        self.termcond_id=termcond_id
        self.productset_id=productset_id
        self.type=ttype
        self.adjustment=adjustment
        self.precedence=precedence
    
    def save(self):
        try:
            cursor.execute("""insert into psetadjmnt(termcond_id,productset_id,type,adjustment,precedence)
            values(%s,%s,%s,%s,%s)on conflict(termcond_id,productset_id)do update set termcond_id=%s,
            productset_id=%s,type=%s,adjustment=%s,precedence=%s returning termcond_id""",
            (self.termcond_id,self.productset_id,self.type,self.adjustment,self.precedence,
            self.termcond_id,self.productset_id,self.type,self.adjustment,self.precedence,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class ExcludedItems:
    def __init__(self,trading_id,tcsubtype_id,extype=3):
        self.extype=extype
        self.tcsubtype_id=tcsubtype_id
        self.trading_id=trading_id
        self.termcond_id=self.gettermcond()
        self.pset_id=self.getpset_id()
    
    def gettermcond(self):
        cursor.execute("select termcond_id from termcond where trading_id=%s and tcsubtype_id=%s",
        (self.trading_id,self.tcsubtype_id,));res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def getpset_id(self):
        cursor.execute("select productset_id from psetadjmnt where termcond_id=%s and type=%s",
        (self.termcond_id,self.extype,));res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def get_items(self):
        cursor.execute("select catentry_id from prsetcerel where productset_id=%s",(self.pset_id,))
        res=cursor.fetchall()
        if len(res)<=0:return list()
        elif len(res)>0:return [x for (x,)in res]

class InstallTradetypes:
    def __init__(self,fname):
        self.fname=fname
    
    def isfilled(self):
        cursor.execute("select count(trdtype_id)from trdtype")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False

    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            values=df.values[:,[0]]
            descriptions=df.values[:,[0,2,1]]
            [Trdtype(*v).save() for v in values]
            [Trdtypedsc(*d).save() for d in descriptions]

class InstallTctypes:
    def __init__(self,fname):
        self.fname=fname

    def isfilled(self):
        cursor.execute("select count(tcsubtype_id)from tcsubtype")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False

    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            values=df.values[:,[0]]
            subtypes=df.values[:,[0,1]]
            descriptions=df.values[:,[1,2,3]]
            [Tctype(*v).save() for v in values]
            [Tcsubtype(*v).save() for v in subtypes]
            [Tcsubtypds(*v).save() for v in descriptions]

class InstallAttachusg:
    def __init__(self,fname):
        self.fname=fname

    def isfilled(self):
        cursor.execute("select count(attachusg_id)from attachusg")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False
    
    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            values=df.values[:,[0]]
            [Attachusg(*x).save() for x in values]

class InstallPartroles:
    def __init__(self,fname):
        self.fname=fname

    def isfilled(self):
        cursor.execute("select count(partrole_id)from partrole")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False
    
    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            roles=df.values[:,[0]]
            descriptions=df.values[:,[0,1,2]]
            [Partrole(*x).save() for x in roles]
            [Partroleds(*x).save() for x in descriptions]

