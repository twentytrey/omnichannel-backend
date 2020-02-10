from .db_con import createcon
# from db_con import createcon
import psycopg2
con,cursor=createcon('retail','jmso','localhost','5432')

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
    
    def save(self):
        try:
            cursor.execute("""insert into plcypasswd(minpasswdlength,minalphabetic,minnumeric,maxinstances,maxconsecutivetype,
            maxlifetime,matchuserid,reusepassword)values(%s,%s,%s,%s,%s,%s,%s,%s)returning plcylasswd_id""",(self.minpasswdlength,
            self.minalphabetic,self.minnumeric,self.maxinstances,self.maxconsecutivetype,self.maxlifetime,self.matchuserid,
            self.reusepassword,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Plcypwddsc:
    def __init__(self,plcypasswd_id,language_id,description=None):
        self.plcypasswd_id=plcypasswd_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into plcypwddsc(plcypasswd_id,language_id,description)values(%s,%s,%s)
            on conflict(plcypasswd_id,language_id)do update set plcypasswd_id=%s,language_id=%s,description=%s
            returning plcypasswd_id""",(self.plcypasswd_id,self.language_id,self.description,));con.commit()
            return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

        