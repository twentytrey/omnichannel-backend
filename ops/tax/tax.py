from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","jmso","localhost","5432")
import  importlib
import pandas as pd
import numpy as np

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Taxtype:
    def  __init__(self,taxtype_id,txcdscheme_id,sequence):
        self.taxtype_id=taxtype_id
        self.txcdscheme_id=txcdscheme_id
        self.sequence=sequence
    
    @staticmethod
    def read():
        cursor.execute("""select taxtype.taxtype_id,calusage.description from taxtype inner join
        calusage on taxtype.taxtype_id=calusage.calusage_id""");res=cursor.fetchall()
        if len(res) <= 0:return [dict(taxtype_id=None,description=None)]
        elif len(res) > 0:return [dict(taxtype_id=r[0],description=r[1]) for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into taxtype(taxtype_id,txcdscheme_id,sequence)values(%s,%s,%s)
            on conflict(taxtype_id)do update set taxtype_id=%s,txcdscheme_id=%s,sequence=%s returning
            taxtype_id""",(self.taxtype_id,self.txcdscheme_id,self.sequence,self.taxtype_id,
            self.txcdscheme_id,self.sequence,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Taxtype.read())
class Taxcgry:
    def __init__(self,taxtype_id,storeent_id,name=None,calculationseq=0,displayseq=0,displayusage=0,field1=None,
    field2=None,field3=None,markfordelete=0):
        self.taxtype_id=taxtype_id
        self.storeent_id=storeent_id
        self.name=name
        self.calculationseq=calculationseq
        self.displayseq=displayseq
        self.displayusage=displayusage
        self.field1=field1
        self.field2=field2
        self.field3=field3
        self.markfordelete=markfordelete
    
    @staticmethod
    def read(storeent_id,language_id):
        cursor.execute("""select taxcgry.taxcgry_id,taxcgry.taxtype_id,calusage.description,taxcgry.storeent_id,
        taxcgry.name,taxcgry.calculationseq,taxcgry.displayseq,taxcgry.displayusage,taxcgry.field1,taxcgry.field2,
        taxcgry.field3,taxcgry.markfordelete,taxcgryds.description from taxcgry left join calusage on taxcgry.
        taxtype_id=calusage.calusage_id inner join taxcgryds on taxcgry.taxcgry_id=taxcgryds.taxcgry_id where 
        taxcgryds.language_id=%s and taxcgry.storeent_id=%s""",(language_id,storeent_id,));res=cursor.fetchall()
        if len(res) <= 0:return [dict(taxcgry_id=None,taxtype_id=None,tax_type=None,storeent_id=storeent_id,
        name=None,calculationseq=0,displayseq=0,displayusage=None,field1=None,field2=None,field3=None,markfordelete=None,
        description=None)]
        elif len(res) > 0:return [dict(taxcgry_id=r[0],taxtype_id=r[1],tax_type=r[2],storeent_id=r[3],name=r[4],
        calculationseq=r[5],displayseq=r[6],displayusage=r[7],field1=r[8],field2=r[9],field3=r[10],markfordelete=r[11],
        description=r[12])for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into taxcgry(taxtype_id,storeent_id,name,calculationseq,displayseq,displayusage,
            field1,field2,field3,markfordelete)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(name,storeent_id)do 
            update set taxtype_id=%s,storeent_id=%s,name=%s,calculationseq=%s,displayseq=%s,displayusage=%s,field1=%s,
            field2=%s,field3=%s,markfordelete=%s returning taxcgry_id""",(self.taxtype_id,self.storeent_id,self.name,
            self.calculationseq,self.displayseq,self.displayusage,self.field1,self.field2,self.field3,self.markfordelete,
            self.taxtype_id,self.storeent_id,self.name,
            self.calculationseq,self.displayseq,self.displayusage,self.field1,self.field2,self.field3,self.markfordelete,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Taxcgry.read(1,1))
class Taxcgryds:
    def __init__(self,language_id,taxcgry_id,description=None):
        self.language_id=language_id
        self.taxcgry_id=taxcgry_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into taxcgryds(language_id,taxcgry_id,description)values(%s,%s,%s)
            on conflict(language_id,taxcgry_id)do update set language_id=%s,taxcgry_id=%s,description=%s
            returning taxcgry_id""",(self.language_id,self.taxcgry_id,self.description,self.language_id,
            self.taxcgry_id,self.description,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Taxjcrule:
    def __init__(self,calrule_id,ffmcenter_id=None,jurstgroup_id=None,precedence=0):
        self.calrule_id=calrule_id
        self.ffmcenter_id=ffmcenter_id
        self.jurstgroup_id=jurstgroup_id
        self.precedence=precedence
    
    def save(self):
        try:
            cursor.execute("""insert into taxjcrule(calrule_id,ffmcenter_id,jurstgroup_id,precedence)
            values(%s,%s,%s,%s)on conflict(calrule_id,ffmcenter_id,jurstgroup_id)do update set calrule_id=%s,
            ffmcenter_id=%s,jurstgroup_id=%s,precedence=%s returning taxjcrule_id""",(self.calrule_id,
            self.ffmcenter_id,self.jurstgroup_id,self.precedence,self.calrule_id,self.ffmcenter_id,
            self.jurstgroup_id,self.precedence,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Jurstgroup:
    def __init__(self,subclass,storeent_id,code,description=None,markfordelete=0):
        self.description=description
        self.subclass=subclass
        self.storeent_id=storeent_id
        self.code=code
        self.markfordelete=markfordelete
    
    @staticmethod
    def mapsubclass(subclass):
        if subclass==None:return None
        elif subclass==1:return 'ShippingJurisdictionGroup'
        elif subclass==2:return 'TaxJurisdictionGroup'
    
    @staticmethod
    def read(storeent_id,subclass):
        cursor.execute("""select jurstgroup_id,description,subclass,storeent_id,code,markfordelete from 
        jurstgroup where storeent_id=%s and subclass=%s""",(storeent_id,subclass,));res=cursor.fetchall()
        if len(res) <= 0:return [dict(jurstgroup_id=None,description=None,subclass=None,storeent_id=storeent_id,markfordelete=None)]
        elif len(res) > 0:return [dict(jurstgroup_id=r[0],description=r[1],subclass=r[2],storeent_id=r[3],code=r[4],
        markfordelete=r[5])for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into jurstgroup(description,subclass,storeent_id,code,markfordelete)
            values(%s,%s,%s,%s,%s)on conflict(code,storeent_id,subclass,description)do update set description=%s,
            subclass=%s,storeent_id=%s,code=%s,markfordelete=%s returning jurstgroup_id""",(self.description,
            self.subclass,self.storeent_id,self.code,self.markfordelete,self.description,self.subclass,
            self.storeent_id,self.code,self.markfordelete,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Jurstgroup.read(1))
class Jurst:
    def __init__(self,storeent_id,code,subclass,country=None,description=None,city=None,state=None,
    stateabbr=None,countryabbr=None,district=None,county=None,zipcodestart=None,zipcodeend=None,
    geocode=None,markfordelete=0):
        self.country=country
        self.storeent_id=storeent_id
        self.code=code
        self.subclass=subclass
        self.description=description
        self.city=city
        self.state=state
        self.stateabbr=stateabbr
        self.countryabbr=countryabbr
        self.district=district
        self.county=county
        self.zipcodestart=zipcodestart
        self.zipcodeend=zipcodeend
        self.geocode=geocode
        self.markfordelete=markfordelete
    
    @staticmethod
    def mapsubclass(subclass):
        if subclass==None:return None
        elif subclass==1:return 'Shipping Jurisdiction'
        elif subclass==2:return 'Tax Jurisdiction'
    
    @staticmethod
    def read(storeent_id,subclass):
        cursor.execute("""select country,storeent_id,code,description,subclass,city,state,stateabbr,countryabbr,
        district,county,zipcodestart,zipcodeend,geocode,markfordelete from jurst where storeent_id=%s and 
        subclass=%s""",(storeent_id,subclass,));res=cursor.fetchall()
        if len(res)<=0:return [dict(country=None,storeent_id=storeent_id,code=None,description=None,subclass=None,
        sub_class=Jurst.mapsubclass(None),city=None,state=None,stateabbr=None,countryabbr=None,district=None,county=None,
        zipcodestart=None,zipcodeend=None,geocode=None,markfordelete=None,_showDetails=False)]
        elif len(res) > 0:return [dict(country=r[0],storeent_id=r[1],code=r[2],description=r[3],subclass=r[4],
        sub_class=Jurst.mapsubclass(r[4]),city=r[5],state=r[6],stateabbr=r[7],countryabbr=r[8],district=r[9],
        county=r[10],zipcodestart=r[11],zipcodeend=r[12],geocode=r[13],markfordelete=r[14],_showDetails=False) for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into jurst(country,storeent_id,code,description,subclass,city,state,
            stateabbr,countryabbr,district,county,zipcodestart,zipcodeend,geocode,markfordelete)values
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(code,storeent_id,subclass)do update
            set country=%s,storeent_id=%s,code=%s,description=%s,subclass=%s,city=%s,state=%s,stateabbr=%s,
            countryabbr=%s,district=%s,county=%s,zipcodestart=%s,zipcodeend=%s,geocode=%s,markfordelete=%s
            returning jurst_id""",(self.country,self.storeent_id,self.code,self.description,self.subclass,
            self.city,self.state,self.stateabbr,self.countryabbr,self.district,self.county,self.zipcodestart,
            self.zipcodeend,self.geocode,self.markfordelete,
            self.country,self.storeent_id,self.code,self.description,self.subclass,
            self.city,self.state,self.stateabbr,self.countryabbr,self.district,self.county,self.zipcodestart,
            self.zipcodeend,self.geocode,self.markfordelete,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Jurst.read(1))
class Jurstgprel:
    def __init__(self,jurst_id,jurstgroup_id,subclass):
        self.jurst_id=jurst_id
        self.jurstgroup_id=jurstgroup_id
        self.subclass=subclass
    
    @staticmethod
    def mapsubclass(subclass):
        if subclass==None:return None
        elif subclass==1:return 'ShippingJurisdiction'
        elif subclass==2:return 'TaxJurisdiction'

    @staticmethod
    def read(jurst_id):
        cursor.execute("select jurst_id,jurstgroup_id,subclass from jurstgprel where jurst_id=%s",(jurst_id,))
        res=cursor.fetchall()
        if len(res) <= 0:return [dict(jurst_id=None,jurstgroup_id=None,subclass=None,sub_class=Jurstgprel.mapsubclass(None))]
        elif len(res) > 0:return [dict(jurst_id=r[0],jurstgroup_id=r[1],subclass=r[2],sub_class=Jurstgprel.mapsubclass(r[2]))
        for r in res]

    def save(self):
        try:
            cursor.execute("""insert into jurstgprel(jurst_id,jurstgroup_id,subclass)values(%s,%s,%s)
            on conflict(jurst_id,jurstgroup_id)do update set jurst_id=%s,jurstgroup_id=%s,subclass=%s
            returning jurstgroup_id""",(self.jurst_id,self.jurstgroup_id,self.subclass,self.jurst_id,
            self.jurstgroup_id,self.subclass,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Jurstgprel.read(1))
class TaxCalrule:
    @staticmethod
    def codename(cid):
        if cid==None:return None
        elif cid !=None:
            cursor.execute("select description from calcodedesc where calcode_id=%s",(cid,))
            return cursor.fetchone()[0]
    @staticmethod
    def categoryname(tid):
        if tid==None:return None
        elif tid != None:
            cursor.execute("select name from taxcgry where taxcgry_id=%s",(tid,))
            return cursor.fetchone()[0]
    @staticmethod
    def methodnames(mid):
        if mid==None:return None
        elif mid != None:
            cursor.execute("select name from calmethod where calmethod_id=%s",(mid,))
            return cursor.fetchone()[0]
    @staticmethod
    def ffmcenter(fid):
        if fid==None:return None
        elif fid != None:
            cursor.execute("select name from ffmcenter where ffmcenter_id=%s",(fid,))
            return cursor.fetchone()[0]
    @staticmethod
    def jurstnames(jid):
        if jid==None:return None
        elif jid != None:
            cursor.execute("select description from jurstgroup where jurstgroup_id=%s",(jid,))
            return cursor.fetchone()[0]
    @staticmethod
    def read():
        cursor.execute("""select calrule.calrule_id,calrule.calcode_id,calrule.startdate,calrule.taxcgry_id,
        calrule.enddate,calrule.sequence,calrule.combination,calrule.calmethod_id,calrule.calmethod_id_qfy,
        calrule.field1,calrule.field2,calrule.flags,calrule.identifier,taxjcrule.ffmcenter_id,taxjcrule.
        jurstgroup_id from calrule left join taxjcrule on calrule.calrule_id=taxjcrule.calrule_id""")
        res=cursor.fetchall()
        if len(res) <=0: return [dict(calrule_id=None,calcode_id=None,startdate=None,taxcgry_id=None,
        enddate=None,sequence=None,combination=None,calmethod_id=None,calmethod_id_qfy=None,field1=None,
        field2=None,flags=None,identifier=None,ffmcenter_id=None,jurstgroup_id=None)]
        elif len(res) > 0:return [dict(calrule_id=r[0],calcode_id=r[1],tax_code=TaxCalrule.codename(r[1]),
        startdate=r[2],taxcgry_id=r[3],tax_category=TaxCalrule.categoryname(r[3]),enddate=r[4],sequence=r[5],
        combination=r[6],calmethod_id=r[7],calculation=TaxCalrule.methodnames(r[7]),calmethod_id_qfy=r[8],
        qualification=TaxCalrule.methodnames(r[8]),field1=r[9],field2=r[10],flags=r[11],identifier=r[12],
        ffmcenter_id=r[13],shipping=TaxCalrule.ffmcenter(r[13]),jurstgroup_id=r[14],
        jurisdiction=TaxCalrule.jurstnames(r[14]))for r in res]
# print(TaxCalrule.read())
class InstallTaxtype:
    def __init__(self,fname):
        self.fname=fname
    
    def isfilled(self):
        cursor.execute("select count(taxtype_id)from taxtype")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False
    
    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            df=df.where(pd.notnull(df),None);values=df.values
            values=[list(v) for v in values]
            [Taxtype(*v).save() for v in values]

class MethodFromCalscale:
    def __init__(self,calscale_id,storeent_id):
        self.calscale_id=calscale_id
        self.storeent_id=storeent_id
        self.calusage_id=self.getusage()
    
    def getusage(self):
        cursor.execute("select calusage_id from calscale where calscale_id=%s",(self.calscale_id,))
        return cursor.fetchone()[0]
    
    def getmethods(self):
        cursor.execute("select calmethod_id,name from calmethod where calusage_id=%s",(self.calusage_id,))
        return [dict(text=x[1],value=x[0]) for x in cursor.fetchall()]

class MethodsFromTaxcat:
    def __init__(self,taxcat_id):
        self.taxcat_id=taxcat_id
        self.calusage_id=self.gettaxtype()
    
    def gettaxtype(self):
        cursor.execute("select taxtype_id from taxcgry where taxcgry_id=%s",(self.taxcat_id,))
        return cursor.fetchone()[0]
    
    def getmethods(self):
        cursor.execute("select calmethod_id,name from calmethod where calusage_id=%s",(self.calusage_id,))
        return [dict(text=x[1],value=x[0])for x in cursor.fetchall()]
