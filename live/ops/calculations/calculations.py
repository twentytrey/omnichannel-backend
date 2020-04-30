from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon('retail','pronov','localhost','5432')
import  importlib
import pandas as pd
import numpy as np
from ops import textualize_datetime,humanize_date

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Calusage:
    def __init__(self,calusage_id,description=None):
        self.calusage_id=calusage_id
        self.description=description
    
    @staticmethod
    def read():
        cursor.execute("select calusage_id,description from calusage")
        res=cursor.fetchall()
        if len(res) <=0 :return [dict(calusage_id=None,description=None)]
        elif len(res) > 0:return [dict(calusage_id=r[0],description=r[1]) for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into calusage(calusage_id,description)values(%s,%s)
            on conflict(calusage_id)do update set calusage_id=%s,description=%s returning calusage_id""",
            (self.calusage_id,self.description,self.calusage_id,self.description,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Calusage.read())
class Stencalusg:
    def __init__(self,storeent_id,calusage_id,atcc_calmethod_id=None,atrc_calmethod_id=None,calcode_id=None,
    calmethod_id_app=None,calmethod_id_sum=None,calmethod_id_fin=None,useflags=0,calmethod_id_ini=None,sequence=0):
        self.storeent_id=storeent_id
        self.calusage_id=calusage_id
        self.atcc_calmethod_id=atcc_calmethod_id
        self.atrc_calmethod_id=atrc_calmethod_id
        self.calcode_id=calcode_id
        self.calmethod_id_app=calmethod_id_app
        self.calmethod_id_sum=calmethod_id_sum
        self.calmethod_id_fin=calmethod_id_fin
        self.useflags=useflags
        self.calmethod_id_ini=calmethod_id_ini
        self.sequence=sequence
    
    @staticmethod
    def update_calcode(calcode_id,storeent_id,calusage_id):
        try:
            cursor.execute("""update stencalusg set calcode_id=%s where storeent_id=%s and calusage_id=%s""",
            (calcode_id,storeent_id,calusage_id,));con.commit()
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def save(self):
        try:
            cursor.execute("""insert into stencalusg(storeent_id,calusage_id,atcc_calmethod_id,atrc_calmethod_id,
            calcode_id,calmethod_id_app,calmethod_id_sum,calmethod_id_fin,useflags,calmethod_id_ini,sequence)values
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(storeent_id,calusage_id)do update set storeent_id=%s,calusage_id=%s,
            atcc_calmethod_id=%s,atrc_calmethod_id=%s,calcode_id=%s,calmethod_id_app=%s,calmethod_id_sum=%s,calmethod_id_fin=%s,
            useflags=%s,calmethod_id_ini=%s,sequence=%s returning storeent_id""",(self.storeent_id,self.calusage_id,self.atcc_calmethod_id,
            self.atrc_calmethod_id,self.calcode_id,self.calmethod_id_app,self.calmethod_id_sum,self.calmethod_id_fin,self.useflags,
            self.calmethod_id_ini,self.sequence,self.storeent_id,self.calusage_id,self.atcc_calmethod_id,self.atrc_calmethod_id,self.calcode_id,
            self.calmethod_id_app,self.calmethod_id_sum,self.calmethod_id_fin,self.useflags,self.calmethod_id_ini,self.sequence,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Calmethod:
    def __init__(self,storeent_id,calusage_id,taskname=None,description=None,subclass=None,name=None):
        self.storeent_id=storeent_id
        self.calusage_id=calusage_id
        self.taskname=taskname
        self.description=description
        self.subclass=subclass
        self.name=name
    
    @staticmethod
    def read(storeent_id,calusage_id):
        cursor.execute("""select calmethod_id,storeent_id,calusage_id,taskname,description,subclass,name from
        calmethod where storeent_id=%s and calusage_id=%s""",(storeent_id,calusage_id,));res=cursor.fetchall()
        if len(res) <= 0:return [dict(calmethod_id=None,storeent_id=storeent_id,calusage_id=calusage_id,
        taskname=None,description=None,subclass=None,name=None)]
        elif len(res) > 0:return [dict(calmethod_id=r[0],storeent_id=r[1],calusage_id=r[2],taskname=r[3],
        description=r[4],subclass=r[5],name=r[6]) for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into calmethod(storeent_id,calusage_id,taskname,description,subclass,
            name)values(%s,%s,%s,%s,%s,%s)on conflict(subclass,calusage_id,storeent_id,name)do update set
            storeent_id=%s,calusage_id=%s,taskname=%s,description=%s,subclass=%s,name=%s returning calmethod_id""",
            (self.storeent_id,self.calusage_id,self.taskname,self.description,self.subclass,self.name,
            self.storeent_id,self.calusage_id,self.taskname,self.description,self.subclass,self.name,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Calmethod.read(1,3))
class Calscale:
    def __init__(self,storeent_id,calusage_id,calmethod_id,qtyunit_id=None,code=None,description=None,
    setccurr=None,field1=None):
        self.storeent_id=storeent_id
        self.calusage_id=calusage_id
        self.calmethod_id=calmethod_id
        self.qtyunit_id=qtyunit_id
        self.code=code
        self.description=description
        self.setccurr=setccurr
        self.field1=field1
    
    @staticmethod
    def taxtypes(cid):
        cursor.execute("select description from calusage where calusage_id=%s",(cid,))
        return cursor.fetchone()[0]
    
    @staticmethod
    def methodname(mid):
        if mid==None:return None
        elif mid != None:
            cursor.execute("select name from calmethod where calmethod_id=%s",(mid,))
            return cursor.fetchone()[0]

    @staticmethod
    def read(storeent_id,language_id):
        cursor.execute("""select calscale.calscale_id,calscale.qtyunit_id,calscale.code::text,calscale.description,
        calscale.storeent_id,calscale.calusage_id,calscale.setccurr,calscale.calmethod_id,calscale.field1,
        calscaleds.description from calscale left join calscaleds on calscale.calscale_id=calscaleds.
        calscale_id where calscale.storeent_id=%s and calscaleds.language_id=%s""",(storeent_id,language_id,))
        res=cursor.fetchall()
        if len(res) <= 0:return [dict(calscale_id=None,qtyunit_id=None,code=None,name=None,storeent_id=None,
        calusage_id=None,tax_type=None,setccurr=None,calmethod_id=None,field1=None,description=None)]
        elif len(res) > 0:return [dict(calscale_id=r[0],qtyunit_id=r[1],code=r[2],name=r[3],storeent_id=r[4],
        calusage_id=r[5],tax_type=Calscale.methodname(r[7]),setccurr=r[6],calmethod_id=r[7],field1=r[8],
        description=r[9]) for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into calscale(qtyunit_id,code,description,storeent_id,calusage_id,
            setccurr,calmethod_id,field1)values(%s,%s,%s,%s,%s,%s,%s,%s)on conflict(calusage_id,code,storeent_id)
            do update set qtyunit_id=%s,code=%s,description=%s,storeent_id=%s,calusage_id=%s,setccurr=%s,
            calmethod_id=%s,field1=%s returning calscale_id""",(self.qtyunit_id,self.code,self.description,
            self.storeent_id,self.calusage_id,self.setccurr,self.calmethod_id,self.field1,
            self.qtyunit_id,self.code,self.description,
            self.storeent_id,self.calusage_id,self.setccurr,self.calmethod_id,self.field1,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Calscale.read(1,1))
class Calscaleds:
    def __init__(self,calscale_id,language_id,description=None):
        self.calscale_id=calscale_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into calscaleds(calscale_id,language_id,description)
            values(%s,%s,%s)on conflict(language_id,calscale_id)do update set calscale_id=%s,
            language_id=%s,description=%s returning calscale_id""",(self.calscale_id,
            self.language_id,self.description,self.calscale_id,self.language_id,self.description,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Calrule:
    def __init__(self,calcode_id,calmethod_id,calmethod_id_qfy,startdate=None,taxcgry_id=None,enddate=None,sequence=0,combination=2,field1=None,field2=None,flags=0,identifier=1):
        self.calcode_id=calcode_id
        self.startdate=startdate
        self.taxcgry_id=taxcgry_id
        self.enddate=enddate
        self.sequence=sequence
        self.combination=combination
        self.calmethod_id=calmethod_id
        self.calmethod_id_qfy=calmethod_id_qfy
        self.field1=field1
        self.field2=field2
        self.flags=flags
        self.identifier=identifier
    
    def save(self):
        try:
            cursor.execute("""insert into calrule(calcode_id,startdate,taxcgry_id,enddate,sequence,combination,
            calmethod_id,calmethod_id_qfy,field1,field2,flags,identifier)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s)on conflict(calcode_id,field2)do update set calcode_id=%s,startdate=%s,taxcgry_id=%s,
            enddate=%s,sequence=%s,combination=%s,calmethod_id=%s,calmethod_id_qfy=%s,field1=%s,field2=%s,
            flags=%s,identifier=%s returning calrule_id""",(self.calcode_id,self.startdate,self.taxcgry_id,
            self.enddate,self.sequence,self.combination,self.calmethod_id,self.calmethod_id_qfy,self.field1,
            self.field2,self.flags,self.identifier,self.calcode_id,self.startdate,self.taxcgry_id,
            self.enddate,self.sequence,self.combination,self.calmethod_id,self.calmethod_id_qfy,self.field1,
            self.field2,self.flags,self.identifier,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Calcode:
    def __init__(self,code,calusage_id,storeent_id,calmethod_id,calmethod_id_app,calmethod_id_qfy,groupby=0,
    txcdclass_id=None,published=1,sequence=0,combination=None,lastupdate=None,field1=None,description=None,displaylevel=0,
    startdate=None,enddate=None,flags=0,precedence=0):
        self.code=code
        self.calusage_id=calusage_id
        self.storeent_id=storeent_id
        self.groupby=groupby
        self.txcdclass_id=txcdclass_id
        self.published=published
        self.sequence=sequence
        self.combination=combination
        self.lastupdate=lastupdate
        self.calmethod_id=calmethod_id
        self.calmethod_id_app=calmethod_id_app
        self.calmethod_id_qfy=calmethod_id_qfy
        self.field1=field1
        self.description=description
        self.displaylevel=displaylevel
        self.startdate=startdate
        self.enddate=enddate
        self.flags=flags
        self.precedence=precedence

    @staticmethod
    def usagename(cusage_id):
        if cusage_id==None:return None
        else:
            cursor.execute("select description from calusage where calusage_id=%s",(cusage_id,))
            return cursor.fetchone()[0]
    
    @staticmethod
    def storename(store_id):
        if store_id==None:return None
        else:
            cursor.execute("select identifier from storeent where storeent_id=%s",(store_id,))
            return cursor.fetchone()[0]

    @staticmethod
    def methodname(mid):
        if mid==None:return None
        else:
            cursor.execute("select name from calmethod where calmethod_id=%s",(mid,))
            return cursor.fetchone()[0]

    @staticmethod
    def read(sid,lid,usages):
        cursor.execute("""select calcode.calcode_id,calcode.calusage_id,calusage.description,calcode.storeent_id,
        calcode.groupby,calcode.txcdclass_id,calcode.published,calcode.sequence,calcode.combination,calcode.lastupdate,
        calcode.calmethod_id,calcode.calmethod_id_app,calcode.calmethod_id_qfy,calcode.field1,calcode.description,
        calcode.displaylevel,calcode.startdate,calcode.enddate,calcode.flags,calcode.precedence,calcodedesc.description,
        calcode.code::text from calcode inner join calusage on calcode.calusage_id=calusage.calusage_id inner join 
        calcodedesc on calcode.calcode_id=calcodedesc.calcode_id where calcode.storeent_id=%s and calcodedesc.
        language_id=%s and calcode.calusage_id in %s""",(sid,lid,tuple(usages),));res=cursor.fetchall()
        if len(res) <= 0:return [dict(calcode_id=None,calusage_id=None,tax_type=None,storeent_id=None,groupby=None,
        txcdclass_id=None,published=None,sequence=None,combination=None,lastupdate=None,calmethod_id=None,
        calmethod_id_app=None,calmethod_id_qfy=None,field1=None,description2=None,displaylevel=None,startdate=None,
        enddate=None,flags=None,precedence=None,description=None,code=None,storename=None,usage=None,updated=None)]
        elif len(res) > 0:return [dict(calcode_id=r[0],calusage_id=r[1],tax_type=r[2],type=r[2],storeent_id=r[3],groupby=r[4],
        txcdclass_id=r[5],published=r[6],sequence=r[7],combination=r[8],lastupdate=textualize_datetime(r[9]),calmethod_id=r[10],
        calculation=Calcode.methodname(r[10]),application=Calcode.methodname(r[11]),qualification=Calcode.methodname(r[12]),
        calmethod_id_app=r[11],calmethod_id_qfy=r[12],field1=r[13],description2=r[14],displaylevel=r[15],
        startdate=r[16],enddate=r[17],flags=r[18],precedence=r[19],description=r[20],code=r[21],usage=Calcode.usagename(r[1]),
        updated=humanize_date(r[9]),storename=Calcode.storename(r[3]),attached=r[3]!=None)for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into calcode(code,calusage_id,storeent_id,groupby,txcdclass_id,published,
            sequence,combination,lastupdate,calmethod_id,calmethod_id_app,calmethod_id_qfy,field1,description,
            displaylevel,startdate,enddate,flags,precedence)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s)on conflict(calusage_id,code,storeent_id)do update set code=%s,calusage_id=%s,
            storeent_id=%s,groupby=%s,txcdclass_id=%s,published=%s,sequence=%s,combination=%s,lastupdate=%s,
            calmethod_id=%s,calmethod_id_app=%s,calmethod_id_qfy=%s,field1=%s,description=%s,displaylevel=%s,
            startdate=%s,enddate=%s,flags=%s,precedence=%s returning calcode_id""",(self.code,self.calusage_id,
            self.storeent_id,self.groupby,self.txcdclass_id,self.published,self.sequence,self.combination,
            self.lastupdate,self.calmethod_id,self.calmethod_id_app,self.calmethod_id_qfy,self.field1,
            self.description,self.displaylevel,self.startdate,self.enddate,self.flags,self.precedence,
            self.code,self.calusage_id,
            self.storeent_id,self.groupby,self.txcdclass_id,self.published,self.sequence,self.combination,
            self.lastupdate,self.calmethod_id,self.calmethod_id_app,self.calmethod_id_qfy,self.field1,
            self.description,self.displaylevel,self.startdate,self.enddate,self.flags,self.precedence,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Calcode.read(1,1,[3,4,2]))
class Calcodedesc:
    def __init__(self,calcode_id,language_id,description):
        self.calcode_id=calcode_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into calcodedesc(calcode_id,language_id,description)values(%s,%s,%s)
            on conflict(calcode_id,language_id)do update set calcode_id=%s,language_id=%s,description=%s
            returning calcode_id""",(self.calcode_id,self.language_id,self.description,self.calcode_id,
            self.language_id,self.description,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Crulescale:
    def __init__(self,calscale_id,calrule_id):
        self.calscale_id=calscale_id
        self.calrule_id=calrule_id
    
    def save(self):
        try:
            cursor.execute("""insert into crulescale(calscale_id,calrule_id)values(%s,%s)on 
            conflict(calrule_id,calscale_id)do update set calscale_id=%s,calrule_id=%s
            returning calrule_id""",(self.calscale_id,self.calrule_id,self.calscale_id,
            self.calrule_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Calrange:
    def __init__(self,calmethod_id,calscale_id=None,rangestart=None,cumulative=0,
    field1=None,field2=None,field3=None,markfordelete=0):
        self.calscale_id=calscale_id
        self.calmethod_id=calmethod_id
        self.rangestart=rangestart
        self.cumulative=cumulative
        self.field1=field1
        self.field2=field2
        self.field3=field3
        self.markfordelete=markfordelete
    
    @staticmethod
    def getusageforscale(cid):
        cursor.execute("""with cusage as (select calusage_id from calscale where calscale_id=%s)
        select calusage.description from calusage inner join cusage on calusage.calusage_id=
        cusage.calusage_id""",(cid,));return cursor.fetchone()[0]
    
    @staticmethod
    def methodname(mid):
        cursor.execute("select name from calmethod where calmethod_id=%s",(mid,))
        return cursor.fetchone()[0]
    
    @staticmethod
    def read():
        cursor.execute("""select calrange.calrange_id,calrange.calscale_id,calrange.calmethod_id,
        calrange.rangestart::float,calrange.cumulative,calrange.field1,calrange.field2,calrange.field3,
        calrange.markfordelete,calrlookup.calrlookup_id,calrlookup.setccurr,calrlookup.value::float from 
        calrange inner join calrlookup on calrange.calrange_id=calrlookup.calrange_id""")
        res=cursor.fetchall()
        if len(res) <= 0:return [dict(calrange_id=None,calscale_id=None,calmethod_id=None,rangestart=None,
        cumulative=None,field1=None,field2=None,field3=None,markfordelete=None,calrlookup_id=None,setccurr=None,
        value=None)]
        elif len(res) > 0:return [dict(calrange_id=r[0],calscale_id=r[1],scale=Calrange.getusageforscale(r[1]),
        calculation=Calrange.methodname(r[2]),calmethod_id=r[2],rangestart=r[3],cumulative=r[4],field1=r[5],
        field2=r[6],field3=r[7],markfordelete=r[8],calrlookup_id=r[9],setccurr=r[10],value=r[11]) for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into calrange(calscale_id,calmethod_id,rangestart,cumulative,field1,field2,field3,
            markfordelete)values(%s,%s,%s,%s,%s,%s,%s,%s)on conflict(calscale_id,rangestart)do update set calscale_id=%s,
            calmethod_id=%s,rangestart=%s,cumulative=%s,field1=%s,field2=%s,field3=%s,markfordelete=%s returning calrange_id""",
            (self.calscale_id,self.calmethod_id,self.rangestart,self.cumulative,self.field1,self.field2,self.field3,
            self.markfordelete,self.calscale_id,self.calmethod_id,self.rangestart,self.cumulative,self.field1,self.field2,
            self.field3,self.markfordelete,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Calrange.read())
class Calrlookup:
    def __init__(self,calrange_id,setccurr=None,value=0):
        self.setccurr=setccurr
        self.calrange_id=calrange_id
        self.value=value

    def save(self):
        try:
            cursor.execute("""insert into calrlookup(setccurr,calrange_id,value)values(%s,%s,%s)
            on conflict(calrange_id,setccurr)do update set setccurr=%s,calrange_id=%s,value=%s
            returning calrlookup_id""",(self.setccurr,self.calrange_id,self.value,self.setccurr,
            self.calrange_id,self.value,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordcalcd:
    def __init__(self,orders_id,calcode_id,calflags=0,calparmtype=0,calparmamt=0):
        self.orders_id=orders_id
        self.calcode_id=calcode_id
        self.calflags=calflags
        self.calparmtype=calparmtype
        self.calparmamt=calparmamt
    
    def save(self):
        try:
            cursor.execute("""insert into ordcalcd(orders_id,calcode_id,calflags,calparmtype,calparmamt)
            values(%s,%s,%s,%s,%s)returning ordcalcd_id""",(self.orders_id,self.calcode_id,self.calflags,
            self.calparmtype,self.calparmamt,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordicalcd:
    def __init__(self,calcode_id,orderitems_id,calflags=0,calparmtype=0,calparmamt=0):
        self.calcode_id=calcode_id
        self.orderitems_id=orderitems_id
        self.calflags=calflags
        self.calparmtype=calparmtype
        self.calparmamt=calparmamt
    
    def save(self):
        try:
            cursor.execute("""insert into ordicalcd(calcode_id,orderitems_id,calflags,calparmtype,calparmamt)
            values(%s,%s,%s,%s,%s)returning ordicalcd_id""",(self.calcode_id,self.orderitems_id,self.calflags,
            self.calparmtype,self.calparmamt,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Caladjust:
    def __init__(self,orders_id,calusage_id,servicerep_id,shipmode_id=None,parmtype=0,parmamt=0,field1=None,field2=None,basecost=0.00000):
        self.orders_id=orders_id
        self.calusage_id=calusage_id
        self.servicerep_id=servicerep_id
        self.shipmode_id=shipmode_id
        self.parmtype=parmtype
        self.parmamt=parmamt
        self.field1=field1
        self.field2=field2
        self.basecost=basecost
    
    def save(self):
        try:
            cursor.execute("""insert into caladjust(orders_id,calusage_id,servicerep_id,shipmode_id,parmtype,parmamt,
            field1,field2,basecost)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)returning caladjust_id""",(self.orders_id,
            self.calusage_id,self.servicerep_id,self.shipmode_id,self.parmtype,self.parmamt,self.field1,self.field2,self.basecost,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class CalusageDefaults:
    def __init__(self):
        self.data=[(1,'Discount'),(2,'Shipping'),(3,'Sales Tax'),(4,'Shipping Tax'),(5,'Coupon'),
        (6,'Surcharge'),(7,'Shipping Adjustment')]

    def isfilled(self):
        cursor.execute("select count(calusage_id) from calusage")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False

    def save(self):[Calusage(*x).save() for x in self.data]

class InstallStencal:
    def __init__(self,fname,storeent_id):
        self.fname=fname
        self.storeent_id=storeent_id

    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            df['storeent_id']=pd.Series([self.storeent_id]*df.shape[0])
            df=df.where(pd.notnull(df),None);values=df.values
            values=[list(v) for v in values]
            [Stencalusg(*v).save() for v in values]

# InstallStencal('stencalusg.csv',1).save()

class InstallCalmethods:
    def __init__(self,fname,storeent_id):
        self.fname=fname
        self.storeent_id=storeent_id
    
    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            df['storeent_id']=pd.Series([self.storeent_id]*df.shape[0])
            df=df.where(pd.notnull(df),None);values=df.values
            values=[list(v) for v in values]
            [Calmethod(*v).save() for v in df.values]

# InstallCalmethods('calmethods.csv',1).save()

# def packagenames():
#     bdir=os.path.abspath(os.path.dirname(__file__))
#     cdir=os.path.join(bdir,"calculationframework/")
#     exclude=['__init__',];data=dict()
#     filter1=[x.split('.py')[0] for x in [x for x in os.listdir(cdir) if '.py' in x]]
#     [data.update({x:'calculationframework.{0}'.format(x)}) for x in list(set(filter1)-set(exclude))]
#     return data

# def getpackage(packagename):
#     packages=packagenames()
#     return {key:value for key,value in packages.items() if key==packagename}[packagename]

# modstring='calculationframework.initializecalculationusage.initializecalculationusage'
# mod=importlib.import_module(modstring)
# print(mod)

class discountcalrangemethods:
    def __init__(self,name,storeent_id,calusage_id):
        self.name=name
        self.storeent_id=storeent_id
        self.calusage_id=calusage_id
    
    def get(self):
        cursor.execute("""select calmethod_id from calmethod where storeent_id=%s and calusage_id=%s 
        and name=%s""",(self.storeent_id,self.calusage_id,self.name,));return cursor.fetchone()[0]

class discountcalscalemethods:
    def __init__(self,name,storeent_id,calusage_id):
        self.name=name
        self.storeent_id=storeent_id
        self.calusage_id=calusage_id
    
    def get(self):
        cursor.execute("""select calmethod_id from calmethod where storeent_id=%s and calusage_id=%s 
        and name=%s""",(self.storeent_id,self.calusage_id,self.name,));return cursor.fetchone()[0]

class discountcalcodemethods:
    def __init__(self,name,storeent_id,calusage_id):
        self.name=name
        self.storeent_id=storeent_id
        self.calusage_id=calusage_id
    
    def get(self):
        cursor.execute("""select calmethod_id from calmethod where name=%s and storeent_id=%s 
        and calusage_id=%s""",(self.name,self.storeent_id,self.calusage_id,))
        return cursor.fetchone()[0]

class discountcalrulemethods:
    def __init__(self,name,storeent_id,calusage_id):
        self.name=name
        self.storeent_id=storeent_id
        self.calusage_id=calusage_id
    
    def get(self):
        cursor.execute("""select calmethod_id from calmethod where storeent_id=%s and calusage_id=%s 
        and name=%s""",(self.storeent_id,self.calusage_id,self.name,));return cursor.fetchone()[0]

# print( discountcalcodemethods('Calculation Code Calculate',1,1).get() )
