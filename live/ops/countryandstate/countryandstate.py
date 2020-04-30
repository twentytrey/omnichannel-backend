from .db_con import createcon
# from db_con import createcon
import psycopg2
con,cursor=createcon('retail','pronov','localhost','5432')
import pandas as pd
import numpy as np
import os

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Country:
    def __init__(self,countryabbr,language_id,name=None,callingcode=None):
        self.countryabbr=countryabbr
        self.language_id=language_id
        self.name=name
        self.callingcode=callingcode
    
    @staticmethod
    def countries():
        cursor.execute("select countryabbr::text,language_id,name,callingcode from country")
        return [{"countryabbr":a,"lang_id":b,"name":c,"callingcode":d} for a,b,c,d in cursor.fetchall()]
    
    def save(self):
        try:
            cursor.execute("""insert into country(countryabbr,language_id,name,callingcode)
            values(%s,%s,%s,%s)on conflict(countryabbr,language_id)do update set countryabbr=%s,
            language_id=%s,name=%s,callingcode=%s returning countryabbr""",(self.countryabbr,
            self.language_id,self.name,self.callingcode,self.countryabbr,self.language_id,self.name,
            self.callingcode,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Stateprov:
    def __init__(self,stateprovabbr,language_id,name=None,countryabbr=None):
        self.stateprovabbr=stateprovabbr
        self.language_id=language_id
        self.name=name
        self.countryabbr=countryabbr
    
    @staticmethod
    def statesforcountry(countryabbr):
        cursor.execute("select stateprovabbr::text,language_id,name from stateprov where countryabbr=%s",
        (countryabbr,));return[{"stateprovabbr":a,"language_id":b,"name":c} for a,b,c in cursor.fetchall()]
    
    def save(self):
        try:
            cursor.execute("""insert into stateprov(stateprovabbr,language_id,name,countryabbr)
            values(%s,%s,%s,%s)on conflict(stateprovabbr,language_id)do update set stateprovabbr=%s,
            language_id=%s,name=%s,countryabbr=%s returning stateprovabbr""",(self.stateprovabbr,
            self.language_id,self.name,self.countryabbr,self.stateprovabbr,self.language_id,
            self.name,self.countryabbr,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class StateprovDefaults:
    def __init__(self,fname,countryabbr):
        self.fname=fname
        self.countryabbr=countryabbr
    
    def isfilled(self):
        cursor.execute("select count(stateprovabbr)from stateprov")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False

    def defaultlang(self):
        cursor.execute("select language_id from languageds where description='English (Nigeria)'")
        return cursor.fetchone()[0]

    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            df['language_id']=pd.Series([self.defaultlang()]*df.shape[0])
            df['countryabbr']=pd.Series([self.countryabbr]*df.shape[0])
            values=df.values[:,[1,7,0,8]]
            [Stateprov(*s).save() for s in values]

class CountryDefaults:
    def __init__(self,fname):
        self.fname=fname
    
    def isfilled(self):
        cursor.execute("select count(countryabbr) from country")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False

    def defaultlang(self):
        cursor.execute("select language_id from languageds where description='English (Nigeria)'")
        return cursor.fetchone()[0]

    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            df['language_id']=pd.Series([self.defaultlang()]*df.shape[0])
            values=df.values[:,[1,5,0,4]]
            [Country(*c).save() for c in values]
