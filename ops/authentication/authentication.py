# from .db_con import createcon
# from db_con import createcon
import psycopg2,os
import pandas as pd
import numpy as np
# con,cursor=createcon('retail','jmso','localhost','5432')
from ops.connector.connector import evcon
con,cursor=evcon()


class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Plcyacclck:
    def __init__(self,lockoutthreshold=6,waittime=10):
        self.lockoutthreshold=lockoutthreshold
        self.waittime=waittime
    
    def has_policy(self,pid):
        try:
            cursor.execute("""select count(plcyacclck_id)from plcyacclck where plcyacclck_id=%s""",
            (pid,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def save(self):
        try:
            cursor.execute("""insert into plcyacclck(lockoutthreshold,waittime)values(%s,%s)
            returning plcyacclck_id""",(self.lockoutthreshold,self.waittime,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Plcylckdsc:
    def __init__(self,plcyacclck_id,language_id,description=None):
        self.plcyacclck_id=plcyacclck_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into plcylckdsc(plcyacclck_id,language_id,description)values(%s,%s,%s)
            on conflict(plcyacclck_id,language_id)do update set plcyacclck_id=%s,language_id=%s,description=%s
            returning plcyacclck_id""",(self.plcyacclck_id,self.language_id,self.description,self.plcyacclck_id,
            self.language_id,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Plcyacct:
    def __init__(self,plcyacclck_id,plcypasswd_id):
        self.plcyacclck_id=plcyacclck_id
        self.plcypasswd_id=plcypasswd_id
    
    @staticmethod
    def read_default():
        cursor.execute("""select plcyacct.plcyacct_id,plcyacct.plcyacclck_id,plcyacct.plcypasswd_id,plcyaccdsc.description
        from plcyacct left join plcyaccdsc on plcyacct.plcyacct_id=plcyaccdsc.plcyacct_id where plcyaccdsc.language_id=1 and 
        plcyaccdsc.description='Default Account Policy'""");res=cursor.fetchone()
        keys=['plcyacct_id','plcyacclck_id','plcypasswd_id','description']
        return dict(zip(keys,res))
    
    def save(self):
        try:
            cursor.execute("""insert into plcyacct(plcyacclck_id,plcypasswd_id)values(%s,%s)returning plcyacct_id""",
            (self.plcyacclck_id,self.plcypasswd_id,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Plcyaccdsc:
    def __init__(self,plcyacct_id,language_id,description=None):
        self.plcyacct_id=language_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into plcyaccdsc(plcyacct_id,language_id,description)values(%s,%s,%s)on conflict
            (plcyacct_id,language_id)do update set plcyacct_id=%s,language_id=%s,description=%s returning plcyacct_id""",
            (self.plcyacct_id,self.language_id,self.description,self.plcyacct_id,self.language_id,self.description,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Plcypasswd:
    def __init__(self,minpasswdlength,minalphabetic,minnumeric,maxinstances,maxconsecutivetype,maxlifetime,matchuserid,reusepassword):
        self.minpasswdlength=minpasswdlength
        self.minalphabetic=minalphabetic
        self.minnumeric=minnumeric
        self.maxinstances=maxinstances
        self.maxconsecutivetype=maxconsecutivetype
        self.maxlifetime=maxlifetime
        self.matchuserid=matchuserid
        self.reusepassword=reusepassword
    
    @staticmethod
    def readdefault():
        cursor.execute("""select plcypasswd.minpasswdlength,plcypasswd.minalphabetic,plcypasswd.minnumeric,
        plcypasswd.maxinstances,plcypasswd.maxconsecutivetype,plcypasswd.maxlifetime,plcypasswd.matchuserid,
        plcypasswd.reusepassword from plcypasswd left join plcypwddsc on plcypasswd.plcypasswd_id=plcypwddsc.plcypasswd_id
        where plcypwddsc.description='Default Password Policy'""");res=cursor.fetchone();keys=['minpasswdlength','minalphabetic',
        'minnumeric','maxinstances','maxconsecutivetype','maxlifetime','matchuserid','reusepassword'];return dict(zip(keys,res))
    
    def save(self):
        try:
            cursor.execute("""insert into plcypasswd(minpasswdlength,minalphabetic,minnumeric,maxinstances,maxconsecutivetype,
            maxlifetime,matchuserid,reusepassword)values(%s,%s,%s,%s,%s,%s,%s,%s)returning plcypasswd_id""",(self.minpasswdlength,
            self.minalphabetic,self.minnumeric,self.maxinstances,self.maxconsecutivetype,self.maxlifetime,self.matchuserid,
            self.reusepassword,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

# print(Plcypasswd.read())

class Plcypwddsc:
    def __init__(self,plcypasswd_id,language_id,description=None):
        self.plcypasswd_id=plcypasswd_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into plcypwddsc(plcypasswd_id,language_id,description)values(%s,%s,%s)
            on conflict(plcypasswd_id,language_id)do update set plcypasswd_id=%s,language_id=%s,description=%s
            returning plcypasswd_id""",(self.plcypasswd_id,self.language_id,self.description,self.plcypasswd_id,
            self.language_id,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class DefaultLockoutPolicy:
    def __init__(self,fname):
        self.fname=fname
    
    def isfilled(self):
        cursor.execute("""select count(plcyacclck.plcyacclck_id)from plcyacclck left join
        plcylckdsc on plcyacclck.plcyacclck_id=plcylckdsc.plcyacclck_id""");res=cursor.fetchone()[0]
        if res <= 0:return False
        elif res > 0:return True
    
    def defaultlang(self):
        cursor.execute("select language_id from languageds where description='English (Nigeria)'")
        return cursor.fetchone()[0]

    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            df['language_id']=pd.Series([self.defaultlang()]*df.shape[0])
            policies=df.values[:,[0,1]];pids=[Plcyacclck(*p).save() for p in policies]
            df['plcyacclck_id']=pd.Series(pids)
            descriptions=df.values[:,[4,2,3]];[Plcylckdsc(*d).save() for d in descriptions]

class DefaultPasswordPolicy:
    def __init__(self,fname):
        self.fname=fname
    
    def isfilled(self):
        cursor.execute("""select count(plcypasswd.plcypasswd_id) from plcypasswd left join plcypwddsc
        on plcypasswd.plcypasswd_id=plcypwddsc.plcypasswd_id""");res=cursor.fetchone()[0]
        if res <= 0:return False
        elif res > 0:return True
    
    def defaultlang(self):
        cursor.execute("select language_id from languageds where description='English (Nigeria)'")
        return cursor.fetchone()[0]

    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            df['language_id']=pd.Series([self.defaultlang()]*df.shape[0])
            policies=df.values[:,[0,1,2,3,4,5,6,7]]
            pids=[Plcypasswd(*p).save() for p in policies]
            df['plcypasswd_id']=pd.Series(pids)
            descriptions=df.values[:,[10,8,9]]
            [Plcypwddsc(*d).save() for d in descriptions]

class DefaultAccountPolicy:
    def __init__(self):
        self.plcyacclck_id=self.getlockout()
        self.plcypasswd_id=self.getpassword()
        self.language_id=self.getdefaultlang()
        self.description='Default Account Policy'
    
    def isfilled(self):
        cursor.execute("select count(plcyacct_id) from plcyaccdsc where description='Default Account Policy'")
        return cursor.fetchone()[0]
    
    def getlockout(self):
        cursor.execute("select plcyacclck_id from plcylckdsc where description='Default Lockout Policy'")
        return cursor.fetchone()[0]
    
    def getpassword(self):
        cursor.execute("select plcypasswd_id from plcypwddsc where description='Default Password Policy'")
        return cursor.fetchone()[0]
    
    def getdefaultlang(self):
        cursor.execute("select language_id from languageds where description='English (Nigeria)'")
        return cursor.fetchone()[0]
    
    def save(self):
        try:
            cursor.execute("""insert into plcyacct(plcyacclck_id,plcypasswd_id)values(%s,%s)returning plcyacct_id""",
            (self.plcyacclck_id,self.plcypasswd_id,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def savedescription(self):
        try:
            plcyacct_id=self.save()
            cursor.execute("""insert into plcyaccdsc(plcyacct_id,language_id,description)values(%s,%s,%s)
            on conflict(plcyacct_id,language_id)do update set plcyacct_id=%s,language_id=%s,description=%s
            returning plcyacct_id""",(plcyacct_id,self.language_id,self.description,plcyacct_id,self.language_id,
            self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
