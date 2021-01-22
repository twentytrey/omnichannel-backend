# from .db_con import createcon
# from db_con import createcon
import psycopg2
# con,cursor=createcon('retail','jmso','localhost','5432')
from ops.connector.connector import evcon
con,cursor=evcon()

import os
import pandas as pd
import numpy as np

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Language:
    def __init__(self,language_id,localename=None,language=None,country=None,variant=None,encoding=None,mimecharset=None):
        self.language_id=language_id
        self.localename=localename
        self.language=language
        self.country=country
        self.variant=variant
        self.encoding=encoding
        self.mimecharset=mimecharset
    
    @staticmethod
    def languages():
        cursor.execute("""select language.language_id,language.localename::text,language.language::text,language.country::text,
        language.variant::text,language.encoding,language.mimeset,languageds.description from language left join languageds
        on language.language_id=languageds.language_id""");return [dict(language_id=x[0],localename=x[1],language=x[2],
        country=x[3],variant=x[4],encoding=x[5],mimeset=x[6],description=x[7]) for x in cursor.fetchall()]
    
    def save(self):
        try:
            cursor.execute("""insert into language(language_id,localename,language,country,variant,encoding,mimeset)
            values(%s,%s,%s,%s,%s,%s,%s)on conflict(language_id)do update set language_id=%s,localename=%s,language=%s,
            country=%s,variant=%s,encoding=%s,mimeset=%s returning language_id""",(self.language_id,self.localename,
            self.language,self.country,self.variant,self.encoding,self.mimecharset,self.language_id,self.localename,
            self.language,self.country,self.variant,self.encoding,self.mimecharset,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

# print(Language.languages())

class Languageds:
    def __init__(self,language_id,description,language_id_desc=None):
        self.language_id=language_id
        self.description=description
        self.language_id_desc=language_id_desc
    
    def save(self):
        try:
            cursor.execute("""insert into languageds(language_id,description,language_id_desc)values(%s,%s,%s)
            on conflict(language_id)do update set language_id=%s,description=%s,language_id_desc=%s returning
            language_id""",(self.language_id,self.description,self.language_id_desc,self.language_id,self.description,
            self.language_id_desc,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Langpair:
    def __init__(self,storeent_id,language_id,language_id_alt,sequence=0):
        self.storeent_id=storeent_id
        self.language_id=language_id
        self.language_id_alt=language_id_alt
        self.sequence=sequence
    
    def save(self):
        try:
            cursor.execute("""insert into langpair(storeent_id,language_id,language_id_alt,sequence)values(%s,%s,%s,%s)
            on conflict(language_id,language_id_alt,storeent_id)do update set storeent_id=%s,language_id=%s,language_id_alt=%s,
            sequence=%s returning language_id""",(self.storeent_id,self.language_id,self.language_id_alt,self.sequence,
            self.storeent_id,self.language_id,self.language_id_alt,self.sequence,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class LanguageDefault:
    def __init__(self,fname):
        self.fname=fname
    
    def isfilled(self):
        cursor.execute("select count(language_id) from language");res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False
    
    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl);df=df.fillna('');languages=df.values[:,[0,1,2,3,4,5,6]]
            lids=[Language(*l).save() for l in languages]
            df['language_id_desc']=pd.Series(lids)
            descriptions=df.values[:,[0,7,8]]
            lids=[Languageds(*d).save() for d in descriptions]

