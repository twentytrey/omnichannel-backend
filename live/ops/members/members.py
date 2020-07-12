from .db_con import createcon
# from db_con import createcon
import psycopg2
con,cursor=createcon('retail','pronov','localhost','5432')
import pandas as pd
import numpy as np
import os,re
from ops import CurrencyHelper,humanize_date,timestamp_forever,timestamp_now,textualize_datetime

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class RevokedToken:
    def __init__(self,token):
        self.token=token
    
    def add(self):
        try:
            cursor.execute("""insert into token_revoked(jti)values(%s)returning token_id""",(self.token,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def isbanned(self):
        try:
            # print(self.token)
            cursor.execute("select jti from token_revoked where jti=%s",(self.token,))
            res=cursor.fetchone()
            if res == None:return False
            elif res != None:return True
        except (Exception, psycopg2.DatabaseError) as e:
            raise EntryException(str(e).strip().split('\n')[0])

class Member:
    def __init__(self,membertype,memberstate=None):
        self.membertype=membertype
        self.memberstate=memberstate
    
    @staticmethod
    def user_exists(logonid):
        cursor.execute("select users_id from userreg where logonid=%s",(logonid,))
        res=cursor.fetchall()
        if len(res) > 0:return True
        elif len(res) <= 0:return False
    
    @staticmethod
    def approve_member(mid):
        try:
            cursor.execute("update member set state=1 where member_id=%s returning member_id",
            (mid,));con.commit();return cursor.fetchone()[0]
            cursor.execute("update users set registertype='R' where users_id=%s",(mid,))
            con.commit()
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    @staticmethod
    def suspend_member(mid):
        try:
            cursor.execute("update member set state=0 where member_id=%s returning member_id",
            (mid,));con.commit();return cursor.fetchone()[0]
            cursor.execute("update users set registertype='G' where users_id=%s",(mid,))
            con.commit()
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    @staticmethod
    def mapmemberstates(mstate):
        states=[(0,'Pending Approval'),(1,'Approved'),(2,'Rejected'),(3,'Pending Email Activation')]
        if mstate==None:return None
        else:return [state[1] for state in states if state[0]==mstate][0]

    @staticmethod
    def mapmembertypes(mtype):
        if mtype==None:return None
        else:return {'O':'Organizational Entity','U':'User','G':'Member Group'}[mtype]
    
    @staticmethod
    def readmember(mid):
        try:
            cursor.execute("select member_id,type::text,state from member where member_id=%s",(mid,))
            res=cursor.fetchone();return dict(zip(['member_id','type','state','typestring','statestring'],
            (res[0],res[1],res[2],Member.mapmembertypes(res[1]),Member.mapmemberstates(res[2]))))
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    def save(self):
        try:
            cursor.execute("""insert into member(type,state)values(%s,%s)
            returning member_id""",(self.membertype,self.memberstate,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Orgentity:
    def __init__(self,orgentity_id,orgentitytype,orgentityname,legalid=None,businesscategory=None,
    description=None,adminfirstname=None,adminlastname=None,adminmiddlename=None,
    preferreddelivery=None,field1=None,field2=None,dn=None,taxpayerid=None,field3=None,
    status=0):
        self.orgentity_id=orgentity_id
        self.legalid=legalid
        self.orgentitytype=orgentitytype
        self.orgentityname=orgentityname
        self.businesscategory=businesscategory
        self.description=description
        self.adminfirstname=adminfirstname
        self.adminmiddlename=adminmiddlename
        self.adminlastname=adminlastname
        self.preferreddelivery=preferreddelivery
        self.field1=field1
        self.field2=field2
        self.dn=dn
        self.taxpayerid=taxpayerid
        self.field3=field3
        self.status=status
    
    @staticmethod
    def maporgentitytype(otype):
        return {"O":"Organization","OU":"Organization Unit","AD":"Authorization Domain"}[otype]
    
    @staticmethod
    def listorgentities():
        cursor.execute("""select orgentity_id,legalid,orgentitytype,orgentityname,businesscategory,
        description,adminfirstname,adminlastname,preferreddelivery,field1,field2,dn,taxpayerid,field3,
        status from orgentity""");res=cursor.fetchall()
        if len(res) <= 0:return [dict(orgentity_id=None,legalid=None,orgentitytype=None,orgentityname=None,
        businesscategory=None,description=None,adminfirstname=None,adminlastname=None,preferreddelivery=None,
        field1=None,field2=None,dn=None,taxpayerid=None,field3=None,status=None)]
        elif len(res) > 0:return [dict(orgentity_id=r[0],legalid=r[1],orgentitytype=r[2],orgentityname=r[3],
        businesscategory=r[4],description=r[5],adminfirstname=r[6],adminlastname=r[7],preferreddelivery=r[8],
        field1=r[9],field2=r[10],dn=r[11],taxpayerid=r[12],field3=r[13],status=r[14]) for r in res]

    @staticmethod
    def readorgentity(oid):
        try:
            cursor.execute("""select orgentity_id,legalid,orgentitytype::text,orgentityname,businesscategory,
            description,adminfirstname,adminmiddlename,adminlastname,preferreddelivery,field1,
            field2,dn,taxpayerid,field3,status from orgentity where orgentity_id=%s""",(oid,))
            res=cursor.fetchone()
            if res==None:
                data=dict(zip(['orgentity_id','legalid','orgentitytype','orgentityname','businesscategory','description','adminfirstname','adminmiddlename','adminlastname','preferreddelivery','field1','field2','dn','taxpayerid','field3','status','orgtypestring'],[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,]))
            elif res != None:
                data=dict(zip(['orgentity_id','legalid','orgentitytype','orgentityname','businesscategory','description','adminfirstname','adminmiddlename','adminlastname','preferreddelivery','field1','field2','dn','taxpayerid','field3','status'],res))
                data.update({"orgtypestring":Orgentity.maporgentitytype(res[2])})
            return data
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    def save(self):
        try:
            cursor.execute("""insert into orgentity(orgentity_id,legalid,orgentitytype,orgentityname,
            businesscategory,description,adminfirstname,adminlastname,adminmiddlename,preferreddelivery,
            field1,field2,dn,taxpayerid,field3,status)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            returning orgentity_id""",(self.orgentity_id,self.legalid,self.orgentitytype,self.orgentityname,
            self.businesscategory,self.description,self.adminfirstname,self.adminlastname,self.adminmiddlename,
            self.preferreddelivery,self.field1,self.field2,self.dn,self.taxpayerid,self.field3,
            self.status,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def update(self):
        try:
            cursor.execute("""update orgentity set orgentitytype=%s,legalid=%s,orgentityname=%s,taxpayerid=%s,
            businesscategory=%s,description=%s,adminfirstname=%s,adminmiddlename=%s,adminlastname=%s where orgentity_id=%s
            returning orgentity_id""",(self.orgentitytype,self.legalid,self.orgentityname,self.taxpayerid,self.businesscategory,
            self.description,self.adminfirstname,self.adminmiddlename,self.adminlastname,self.orgentity_id,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

# print(Orgentity.readorgentity(2))

class Busprof:
    def __init__(self,users_id,employeeid=None,org_id=None,orgunit_id=None,employeetype=None,
    departmentnum=None,alternateid=None,manager=None,secretary=None,requisitionerid=None):
        self.users_id=users_id
        self.employeeid=employeeid
        self.org_id=org_id
        self.orgunit_id=orgunit_id
        self.employeetype=employeetype
        self.departmentnum=departmentnum
        self.alternateid=alternateid
        self.manager=manager
        self.secretary=secretary
        self.requisitionerid=requisitionerid
    
    @staticmethod
    def readbusprof(uid):
        try:
            cursor.execute("""select busprof.employeeid,busprof.org_id,orgentity.orgentityname,busprof.orgunit_id,
            busprof.employeetype,busprof.departmentnum,busprof.alternateid,busprof.manager,busprof.secretary,
            busprof.requisitionerid from busprof inner join orgentity on busprof.org_id=orgentity.orgentity_id
            where busprof.users_id=%s""",(uid,));res=cursor.fetchone();return dict(zip(['employeeid','org_id',
            'orgentityname','orgunit_id','employeetype','departmentnum','alternateid','manager','secretary',
            'requisitionerid'],res))
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def update(self):
        try:
            cursor.execute("""update busprof set users_id=%s,employeeid=%s,org_id=%s,orgunit_id=%s,employeetype=%s,
            departmentnum=%s,alternateid=%s,manager=%s,secretary=%s,requisitionerid=%s where users_id=%s returning users_id""",
            (self.users_id,self.employeeid,self.org_id,self.orgunit_id,self.employeetype,self.departmentnum,
            self.alternateid,self.manager,self.secretary,self.requisitionerid,self.users_id,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    def save(self):
        try:
            cursor.execute("""insert into busprof(users_id,employeeid,org_id,orgunit_id,employeetype,departmentnum,
            alternateid,manager,secretary,requisitionerid)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on conflict(users_id)
            do update set users_id=%s,employeeid=%s,org_id=%s,orgunit_id=%s,employeetype=%s,departmentnum=%s,
            alternateid=%s,manager=%s,secretary=%s,requisitionerid=%s returning users_id""",
            (self.users_id,self.employeeid,self.org_id,self.orgunit_id,self.employeetype,self.departmentnum,self.alternateid,
            self.manager,self.secretary,self.requisitionerid,
            self.users_id,self.employeeid,self.org_id,self.orgunit_id,self.employeetype,self.departmentnum,self.alternateid,
            self.manager,self.secretary,self.requisitionerid,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Userprof:
    def __init__(self,users_id,photo=None,description=None,displayname=None,preferredcomm=None,
    preferreddelivery=None,preferredmeasure=None,field1=None,taxpayerid=None,field2=None,rcvsmsnotification=0):
        self.users_id=users_id
        self.photo=photo
        self.description=description
        self.displayname=displayname
        self.preferredcomm=preferredcomm
        self.preferreddelivery=preferreddelivery
        self.preferredmeasure=preferredmeasure
        self.field1=field1
        self.taxpayerid=taxpayerid
        self.field2=field2
        self.rcvsmsnotification=rcvsmsnotification
    
    @staticmethod
    def isfilled(uid):
        cursor.execute("select count(users_id)from userprof where users_id=%s",(uid,))
        return cursor.fetchone()[0]
    
    @staticmethod
    def mappreferredcomm(pcid):
        return {"P1":"First Phone Number","P2":"Second Phone Number","E1":"First Email Address",
        "E2":"Second Email Address"}[pcid]
    
    @staticmethod
    def readuserprof(uid):
        try:
            cursor.execute("""select photo,description,displayname,preferredcomm,preferreddelivery,
            preferredmeasure,field1,taxpayerid,field2,rcvsmsnotification from userprof where users_id=%s""",
            (uid,));res=cursor.fetchone()
            if res==None:return dict(photo=None,description=None,displayname=None,preferredcomm=None,
            preferreddelivery=None,preferredmeasure=None,field1=None,taxpayerid=None,field2=None,
            rcvsmsnotification=None,preferredcommstring=None)
            elif res != None:return dict(photo=res[0],description=res[1],displayname=res[2],preferredcomm=res[3],
            preferreddelivery=res[4],preferredmeasure=res[5],field1=res[6],taxpayerid=res[7],field2=res[8],
            rcvsmsnotification=res[9],preferredcommstring=Userprof.mappreferredcomm(res[3]))
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    def update(self):
        try:
            cursor.execute("""update userprof set photo=%s,description=%s,displayname=%s,preferredcomm=%s,
            rcvsmsnotification=%s where users_id=%s returning users_id""",(self.photo,self.description,self.displayname,
            self.preferredcomm,self.rcvsmsnotification,self.users_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def save(self):
        try:
            cursor.execute("""insert into userprof(users_id,photo,description,displayname,preferredcomm,
            preferreddelivery,preferredmeasure,field1,taxpayerid,field2,rcvsmsnotification)values(%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s)on conflict(users_id)do update set users_id=%s,photo=%s,description=%s,
            displayname=%s,preferredcomm=%s,preferreddelivery=%s,preferredmeasure=%s,field1=%s,taxpayerid=%s,
            field2=%s,rcvsmsnotification=%s returning users_id""",(self.users_id,self.photo,self.description,
            self.displayname,self.preferredcomm,self.preferreddelivery,self.preferredmeasure,self.field1,
            self.taxpayerid,self.field2,self.rcvsmsnotification,self.users_id,self.photo,self.description,
            self.displayname,self.preferredcomm,self.preferreddelivery,self.preferredmeasure,self.field1,
            self.taxpayerid,self.field2,self.rcvsmsnotification,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Mbrgrp:
    def __init__(self,mbrgrp_id,owner_id,mbrgrpname,field1=None,description=None,field2=None,dn=None,
    field3=None,oid=None,lastupdate=None,lastupdatedby=None):
        self.mbrgrp_id=mbrgrp_id
        self.owner_id=owner_id
        self.mbrgrpname=mbrgrpname
        self.field1=field1
        self.description=description
        self.field2=field2
        self.dn=dn
        self.field3=field3
        self.oid=oid
        self.lastupdate=lastupdate
        self.lastupdatedby=lastupdatedby
    
    def save(self):
        try:
            cursor.execute("""insert into mbrgrp(mbrgrp_id,owner_id,field1,description,field2,dn,mbrgrpname,
            field3,oid,lastupdate,lastupdatedby)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(mbrgrp_id)
            do update set mbrgrp_id=%s,owner_id=%s,field1=%s,description=%s,field2=%s,dn=%s,mbrgrpname=%s,
            field3=%s,oid=%s,lastupdate=%s,lastupdatedby=%s returning mbrgrp_id""",(self.mbrgrp_id,self.owner_id,
            self.field1,self.description,self.field2,self.dn,self.mbrgrpname,self.field3,self.oid,self.lastupdate,
            self.lastupdatedby,self.mbrgrp_id,self.owner_id,self.field1,self.description,self.field2,self.dn,
            self.mbrgrpname,self.field3,self.oid,self.lastupdate,self.lastupdatedby,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Userreg:
    def __init__(self,users_id,logonid,timeout=1,status=None,plcyacct_id=None,logonpassword=None,passwordexpired=None,
    challengequestion=None,challengeanswer=None,salt=None,passwordcreation=None,passwordinvalid=None):
        self.users_id=users_id
        self.logonid=logonid
        self.timeout=timeout
        self.status=status
        self.plcyacct_id=plcyacct_id
        self.logonpassword=logonpassword
        self.passwordexpired=passwordexpired
        self.challengequestion=challengequestion
        self.challengeanswer=challengeanswer
        self.salt=salt
        self.passwordcreation=passwordcreation
        self.passwordinvalid=passwordinvalid

    @staticmethod
    def logoniswhat(logonid):
        mailmatch=re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",logonid,re.I)
        phonematch=re.match(r"^[0]\d{10}$",logonid,re.I)
        if mailmatch != None:return "email"
        elif phonematch != None:return "phone"
    
    def update(self):
        try:
            cursor.execute("""update userreg set status=%s,plcyacct_id=%s,logonid=%s,logonpassword=%s,passwordexpired=%s,
            challengequestion=%s,challengeanswer=%s,timeout=%s,salt=%s,passwordcreation=%s,passwordinvalid=%s where users_id=%s
            returning users_id""",
            (self.status,self.plcyacct_id,self.logonid,self.logonpassword,self.passwordexpired,self.challengequestion,
            self.challengeanswer,self.timeout,self.salt,self.passwordcreation,self.passwordinvalid,self.users_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    @staticmethod
    def readuserreg(uid):
        try:
            cursor.execute("""select status,plcyacct_id,logonid,logonpassword,passwordexpired,challengequestion,challengeanswer,
            timeout,salt,passwordcreation,passwordinvalid from userreg where users_id=%s""",(uid,));res=cursor.fetchone()
            res=dict(zip(['status','plcyacct_id','logonid','logonpassword','passwordexpired','challengequestion',
            'challengeanswer','timeout','salt','passwordcreation','passwordinvalid'],res))
            res['passwordcreation']=humanize_date(res['passwordcreation']);return res
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    def save(self):
        try:
            cursor.execute("""insert into userreg(users_id,status,plcyacct_id,logonid,logonpassword,passwordexpired,challengequestion,
            challengeanswer,timeout,salt,passwordcreation,passwordinvalid)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(users_id)
            do update set users_id=%s,status=%s,plcyacct_id=%s,logonid=%s,logonpassword=%s,passwordexpired=%s,challengequestion=%s,
            challengeanswer=%s,timeout=%s,salt=%s,passwordcreation=%s,passwordinvalid=%s returning users_id""",(self.users_id,self.status,
            self.plcyacct_id,self.logonid,self.logonpassword,self.passwordexpired,self.challengequestion,self.challengeanswer,self.timeout,
            self.salt,self.passwordcreation,self.passwordinvalid,self.users_id,self.status,self.plcyacct_id,self.logonid,self.logonpassword,
            self.passwordexpired,self.challengequestion,self.challengeanswer,self.timeout,self.salt,self.passwordcreation,self.passwordinvalid,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    @staticmethod
    def getusersid(logonid):
        cursor.execute("select users_id from userreg where logonid=%s",(logonid,))
        res=cursor.fetchone()
        if res==None:return None
        elif res != None:return res[0]

    @staticmethod
    def getsalt(logonid):
        cursor.execute("select salt from userreg where users_id=%s",(logonid,))
        res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]

    @staticmethod
    def getpassword(logonid):
        try:
            cursor.execute("select logonpassword from userreg where logonid=%s",(logonid,))
            res=cursor.fetchone()
            if res != None:return res[0]
            elif res==None:return None
        except(Exception,psycopg2.DatabaseError) as e:
            raise EntryException(str(e).strip().split('\n')[0])

class Mbrrole:
    def __init__(self,member_id,role_id,orgentity_id):
        self.member_id=member_id
        self.role_id=role_id
        self.orgentity_id=orgentity_id

    @staticmethod
    def read(mid):
        cursor.execute("""select mbrrole.member_id,mbrrole.role_id,mbrrole.orgentity_id,userprof.displayname,
        roledesc.displayname,orgentity.orgentityname from mbrrole left join userprof on mbrrole.member_id=
        userprof.users_id left join roledesc on roledesc.role_id=mbrrole.role_id left join orgentity on 
        orgentity.orgentity_id=mbrrole.orgentity_id where mbrrole.member_id=%s""",(mid,));res=cursor.fetchall()
        return [dict(zip(['member_id','role_id','orgentity_id','username','rolename','organization'],r))for r in res]

    def save(self):
        try:
            cursor.execute("""insert into mbrrole(member_id,role_id,orgentity_id)values(%s,%s,%s)on conflict(member_id,role_id,orgentity_id)
            do update set member_id=%s,role_id=%s,orgentity_id=%s returning member_id""",(self.member_id,self.role_id,self.orgentity_id,
            self.member_id,self.role_id,self.orgentity_id,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Mbrrole.read(1))
class Role:
    def __init__(self,name,description=None):
        self.name=name
        self.description=description

    @staticmethod
    def read_roles(language_id):
        cursor.execute("""select role.role_id,role.name,roledesc.displayname,roledesc.description from role 
        left join roledesc on role.role_id=roledesc.role_id where roledesc.language_id=%s""",(language_id,))
        keys=['role_id','name','displayname','description'];return [dict(zip(keys,z)) for z in cursor.fetchall()]

    def save(self):
        try:
            cursor.execute("""insert into role(name,description)values(%s,%s)on conflict(name)do update set
            name=%s,description=%s returning role_id""",(self.name,self.description,self.name,self.description,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Role.read_roles(1))
class Roledesc:
    def __init__(self,role_id,language_id,displayname,description=None):
        self.role_id=role_id
        self.language_id=language_id
        self.displayname=displayname
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into roledesc(role_id,language_id,displayname,description)values(%s,%s,%s,%s)
            on conflict(role_id,language_id)do update set role_id=%s,language_id=%s,displayname=%s,description=%s
            returning role_id""",(self.role_id,self.language_id,self.displayname,self.description,self.role_id,self.language_id,
            self.displayname,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Roleasnprm:
    def __init__(self,assigning_role_id,orgentity_id,assignable_role_id=None):
        self.assigning_role_id=int(assigning_role_id)
        self.orgentity_id=int(orgentity_id)
        self.assignable_role_id=int(assignable_role_id)
    
    def save(self):
        try:
            cursor.execute("""insert into roleasnprm(assigning_role_id,orgentity_id,assignable_role_id)values(%s,%s,%s)
            on conflict(assigning_role_id,orgentity_id,assignable_role_id)do update set assigning_role_id=%s,orgentity_id=%s,
            assignable_role_id=%s returning roleasnprm_id""",(self.assigning_role_id,self.orgentity_id,self.assignable_role_id,
            self.assigning_role_id,self.orgentity_id,self.assignable_role_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Mbrgrpusg:
    def __init__(self,mbrgrptype_id,mbrgrp_id,field1=None):
        self.mbrgrptype_id=mbrgrptype_id
        self.mbrgrp_id=mbrgrp_id
        self.field1=field1
    
    def save(self):
        try:
            cursor.execute("""insert into mbrgrpusg(mbrgrptype_id,mbrgrp_id,field1)values(%s,%s,%s)on conflict(mbrgrptype_id,
            mbrgrp_id,field1)do update set mbrgrptype_id=%s,mbrgrp_id=%s,field1=%s returning mbrgrptype_id""",(self.mbrgrptype_id,
            self.mbrgrp_id,self.field1,self.mbrgrptype_id,self.mbrgrp_id,self.field1,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Mgpcondele:
    def __init__(self,mbrgrp_id,name,gtype,parent=None,sequence=None,variable=None,operator=None,value=None,
    condname=None,negate=0):
        self.mbrgrp_id=mbrgrp_id
        self.name=name
        self.type=gtype
        self.parent=parent
        self.sequence=sequence
        self.variable=variable
        self.operator=operator
        self.value=value
        self.condname=condname
        self.negate=negate
    
    def save(self):
        try:
            cursor.execute("""insert into mgpcondele(mbrgrp_id,name,type,parent,sequence,variable,operator,value,condname,
            negate)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(name,mbrgrp_id)do update set mbrgrp_id=%s,name=%s,type=%s,
            parent=%s,sequence=%s,variable=%s,operator=%s,value=%s,condname=%s,negate=%s returning mgpcondele_id""",(self.mbrgrp_id,
            self.name,self.type,self.parent,self.sequence,self.variable,self.operator,self.value,self.condname,self.negate,
            self.mbrgrp_id,self.name,self.type,self.parent,self.sequence,self.variable,self.operator,self.value,self.condname,
            self.negate,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Mbrgrptype:
    def __init__(self,name,properties=None,description=None):
        self.name=name
        self.properties=properties
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into mbrgrptype(name,properties,description)values(%s,%s,%s)on conflict(name)
            do update set name=%s,properties=%s,description=%s returning mbrgrptype_id""",(self.name,self.properties,self.description,
            self.name,self.properties,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Mgpcondelenvp:
    def __init__(self,mgpcondele_id,name,value):
        self.mgpcondele_id=mgpcondele_id
        self.name=name
        self.value=value
    
    def save(self):
        try:
            cursor.execute("""insert into mgpcondelenvp(mgpcondele_id,name,value)values(%s,%s,%s)
            returning mgpcondelenvp_id""",(self.mgpcondele_id,self.name,self.value,self.mgpcondele_id,self.name,self.value,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Users:
    def __init__(self,users_id,registertype,dn=None,profiletype=None,language_id=None,field1=None,setccurr=None,field3=None,
    field2=None,lastorder=None,registration=None,lastsession=None,registrationupdate=None,registrationcancel=None,
    prevlastsession=None,personalizationid=None):
        self.users_id=users_id
        self.registertype=registertype
        self.dn=dn
        self.profiletype=profiletype
        self.language_id=language_id
        self.field1=field1
        self.setccurr=CurrencyHelper(self.language_id).intsymbol
        self.field3=field3
        self.field2=field2
        self.lastorder=lastorder
        self.registration=registration
        self.lastsession=lastsession
        self.registrationupdate=registrationupdate
        self.registrationcancel=registrationcancel
        self.prevlastsession=prevlastsession
        self.personalizationid=personalizationid
    
    @staticmethod
    def mapregproftypes(rtype):
        d=dict(R='Registered User',G='Guest User',A='Administrator',S='Site Administrator')
        return d[rtype]

    @staticmethod
    def mapprofiletypes(proftype):
        d=dict(C='Base Profile',B='Business Profile');return d[proftype]
    
    @staticmethod
    def readusers(uid):
        try:
            cursor.execute("""select dn,registertype::text,profiletype::text,language_id,field1,setccurr,field3,
            field2,lastorder,registration,lastsession,registrationupdate,registrationcancel,prevlastsession,
            personalizationid from users where users_id=%s""",(uid,));res=cursor.fetchone()
            res=dict(zip(['dn','registertype','profiletype','language_id','field1',
            'setccurr','field3','field2','lastorder','registration','lastsession',
            'registrationupdate','registrationcancel','prevlastsession','personalizationid'],res))
            res['registertypestring']=Users.mapregproftypes(res['registertype'])
            res['profiletypestring']=Users.mapprofiletypes(res['profiletype'])
            res['lastorder']=humanize_date(res['lastorder'])
            res["registration"]=humanize_date(res["registration"])
            res["lastsession"]=humanize_date(res["lastsession"])
            res["registrationupdate"]=humanize_date(res["registrationupdate"])
            res["registrationcancel"]=humanize_date(res["registrationcancel"])
            return res
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def update(self):
        try:
            cursor.execute("""update users set dn=%s,registertype=%s,profiletype=%s,language_id=%s,field1=%s,
            setccurr=%s,field3=%s,field2=%s,lastorder=%s,registrationupdate=%s,prevlastsession=%s,personalizationid=%s
            where users_id=%s returning users_id""",(self.dn,self.registertype,self.profiletype,self.language_id,self.field1,
            self.setccurr,self.field3,self.field2,self.lastorder,timestamp_now(),self.prevlastsession,self.personalizationid,
            self.users_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def save(self):
        try:
            cursor.execute("""insert into users(users_id,dn,registertype,profiletype,language_id,field1,setccurr,field3,
            field2,lastorder,registration,lastsession,registrationupdate,registrationcancel,prevlastsession,personalizationid)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(users_id)do update set users_id=%s,dn=%s,
            registertype=%s,profiletype=%s,language_id=%s,field1=%s,setccurr=%s,field3=%s,field2=%s,lastorder=%s,registration=%s,
            lastsession=%s,registrationupdate=%s,registrationcancel=%s,prevlastsession=%s,personalizationid=%s returning users_id""",
            (self.users_id,self.dn,self.registertype,self.profiletype,self.language_id,self.field1,self.setccurr,self.field3,self.field2,self.lastorder,self.registration,self.lastsession,self.registrationupdate,self.registrationcancel,self.prevlastsession,self.personalizationid,
            self.users_id,self.dn,self.registertype,self.profiletype,self.language_id,self.field1,self.setccurr,self.field3,self.field2,self.lastorder,self.registration,self.lastsession,self.registrationupdate,self.registrationcancel,self.prevlastsession,self.personalizationid,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Mbrgrpcond:
    def __init__(self,mbrgrp_id,conditions=None,field1=None,field2=None):
        self.mbrgrp_id=mbrgrp_id
        self.conditions=conditions
        self.field1=field1
        self.field2=field2
    
    def save(self):
        try:
            cursor.execute("""insert into mbrgrpcond(mbrgrp_id,conditions,field1,field2)values(%s,%s,%s,%s)
            on conflict(mbrgrp_id)do update set mbrgrp_id=%s,conditions=%s,field1=%s,field2=%s returning mbrgrp_id""",
            (self.mbrgrp_id,self.conditions,self.field1,self.field2,self.mbrgrp_id,self.conditions,self.field1,self.field2,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Mbrgrpmbr:
    def __init__(self,member_id,mbrgrp_id,field1=None,customerid=None,exclude='0'):
        self.member_id=member_id
        self.mbrgrp_id=mbrgrp_id
        self.field1=field1
        self.customerid=customerid
        self.exclude=exclude
    
    def save(self):
        try:
            cursor.execute("""insert into mbrgrpmbr(member_id,mbrgrp_id,field1,customerid,exclude)values(%s,%s,%s,%s,%s)
            on conflict(member_id,mbrgrp_id)do update set member_id=%s,mbrgrp_id=%s,field1=%s,customerid=%s,exclude=%s
            returning member_id""",(self.member_id,self.mbrgrp_id,self.field1,self.customerid,self.exclude,self.member_id,
            self.mbrgrp_id,self.field1,self.customerid,self.exclude,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Mbrrel:
    def __init__(self,descendant_id,ancestor_id,sequence=None):
        self.descendant_id=descendant_id
        self.ancestor_id=ancestor_id
        self.sequence=sequence
    
    def save(self):
        try:
            cursor.execute("""insert into mbrrel(descendant_id,ancestor_id,sequence)values(%s,%s,%s)on conflict(descendant_id,ancestor_id)
            do update set descendant_id=%s,ancestor_id=%s returning descendant_id""",(self.descendant_id,self.ancestor_id,self.sequence,
            self.descendant_id,self.ancestor_id,self.sequence,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Addrbook:
    def __init__(self,member_id,displayname,adbtype=None,description=None):
        self.member_id=member_id
        self.displayname=displayname
        self.type=adbtype
        self.description=description
    
    @staticmethod
    def readaddrbook(mid):
        cursor.execute("""select addrbook_id,type,displayname,description from addrbook where
        member_id=%s""",(mid,));res=cursor.fetchone();return dict(zip(["addrbook_id","type","displayname",
        "description"],res))

    def update(self):
        try:
            cursor.execute("""update addrbook set type=%s,displayname=%s,description=%s where member_id=%s 
            returning addrbook_id""",(self.type,self.displayname,self.description,self.member_id,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def save(self):
        try:
            cursor.execute("""insert into addrbook(member_id,type,displayname,description)values(%s,%s,%s,%s)
            on conflict(addrbook_id,member_id)do update set member_id=%s,type=%s,displayname=%s,description=%s
            returning addrbook_id""",(self.member_id,self.type,self.displayname,self.description,
            self.member_id,self.type,self.displayname,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Address:
    def __init__(self,addrbook_id,member_id,nickname,addresstype=None,orgunitname=None,field3=None,billingcode=None,
    billingcodetype=None,status=None,orgname=None,isprimary=None,lastname=None,persontitle=None,firstname=None,
    middlename=None,businesstitle=None,phone1=None,fax1=None,phone2=None,address1=None,fax2=None,address2=None,city=None,
    state=None,country=None,zipcode=None,email1=None,email2=None,phone1type=None,phone2type=None,bestcallingtime=None,
    packagesuppression=None,lastcreate=None,officeaddress=None,selfaddress=0,field1=None,field2=None,taxgeocode=None,
    shippinggeocode=None,mobilephone1=None,mobilephone1cntry=None,address3=None,publishphone1=None,publishphone2=None,
    address_id=None):
        self.addrbook_id=addrbook_id
        self.member_id=member_id
        self.nickname=nickname
        self.address3=address3
        self.publishphone1=publishphone1
        self.publishphone2=publishphone2
        self.addresstype=addresstype
        self.orgunitname=orgunitname
        self.field3=field3
        self.billingcode=billingcode
        self.billingcodetype=billingcodetype
        self.status=status
        self.orgname=orgname
        self.isprimary=isprimary
        self.lastname=lastname
        self.persontitle=persontitle
        self.firstname=firstname
        self.middlename=middlename
        self.businesstitle=businesstitle
        self.phone1=phone1
        self.fax1=fax1
        self.phone2=phone2
        self.address1=address1
        self.fax2=fax2
        self.address2=address2
        self.city=city
        self.state=state
        self.country=country
        self.zipcode=zipcode
        self.email1=email1
        self.email2=email2
        self.phone1type=phone1type
        self.phone2type=phone2type
        self.bestcallingtime=bestcallingtime
        self.packagesuppression=packagesuppression
        self.lastcreate=lastcreate
        self.officeaddress=officeaddress
        self.selfaddress=selfaddress
        self.field1=field1
        self.field2=field2
        self.taxgeocode=taxgeocode
        self.shippinggeocode=shippinggeocode
        self.mobilephone1=mobilephone1
        self.mobilephone1cntry=mobilephone1cntry
        self.address_id=address_id
    
    @staticmethod
    def readaddress(mid):
        try:
            cursor.execute("""select address_id,addresstype::text,member_id,addrbook_id,orgunitname,field3,billingcode,billingcodetype,
            status,orgname,isprimary,lastname,persontitle,firstname,middlename,businesstitle,phone1,fax1,phone2,address1,fax2,
            nickname,address2,address3,city,state,country,zipcode,email1,email2,phone1type,phone2type,publishphone1,
            publishphone2,bestcallingtime,packagesuppression,lastcreate,officeaddress,selfaddress,field1,field2,taxgeocode,
            shippinggeocode,mobilephone1,mobilephone1cntry from address where member_id=%s""",(mid,));res=cursor.fetchone()
            if res==None:return dict(address_id=None,addresstype=None,member_id=None,addrbook_id=None,orgunitname=None,
            field3=None,billingcode=None,billingcodetype=None,status=None,orgname=None,isprimary=None,lastname=None,
            persontitle=None,firstname=None,middlename=None,businesstitle=None,phone1=None,fax1=None,phone2=None,address1=None,
            fax2=None,nickname=None,address2=None,address3=None,city=None,state=None,country=None,zipcode=None,email1=None,
            email2=None,phone1type=None,phone2type=None,publishphone1=None,publishphone2=None,bestcallingtime=None,
            packagesuppression=None,lastcreate=None,officeaddress=None,selfaddress=None,field1=None,field2=None,taxgeocode=None,
            shippinggeocode=None,mobilephone1=None,mobilephone1cntry=None)
            elif res != None:return dict(address_id=res[0],addresstype=res[1],member_id=res[2],addrbook_id=res[3],orgunitname=res[4],
            field3=res[5],billingcode=res[6],billingcodetype=res[7],status=res[8],orgname=res[9],isprimary=res[10],lastname=res[11],
            persontitle=res[12],firstname=res[13],middlename=res[14],businesstitle=res[15],phone1=res[16],fax1=res[17],phone2=res[18],
            address1=res[19],fax2=res[20],nickname=res[21],address2=res[22],address3=res[23],city=res[24],state=res[25],country=res[26],
            zipcode=res[27],email1=res[28],email2=res[29],phone1type=res[30],phone2type=res[31],publishphone1=res[32],publishphone2=res[33],
            bestcallingtime=res[34],packagesuppression=res[35],lastcreate=textualize_datetime(res[36]),officeaddress=res[37],selfaddress=res[38],
            field1=res[39],field2=res[40],taxgeocode=res[41],shippinggeocode=res[42],mobilephone1=res[43],mobilephone1cntry=res[44])
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    def update(self):
        try:
            cursor.execute("""update address set addresstype=%s,member_id=%s,addrbook_id=%s,orgunitname=%s,field3=%s,
            billingcode=%s,billingcodetype=%s,status=%s,orgname=%s,isprimary=%s,lastname=%s,persontitle=%s,firstname=%s,
            middlename=%s,businesstitle=%s,phone1=%s,fax1=%s,phone2=%s,address1=%s,fax2=%s,nickname=%s,address2=%s,
            address3=%s,city=%s,state=%s,country=%s,zipcode=%s,email1=%s,email2=%s,phone1type=%s,phone2type=%s,publishphone1=%s,
            publishphone2=%s,bestcallingtime=%s,packagesuppression=%s,lastcreate=%s,officeaddress=%s,selfaddress=%s,
            field1=%s,field2=%s,taxgeocode=%s,shippinggeocode=%s,mobilephone1=%s,mobilephone1cntry=%s where address_id=%s
            returning address_id""",
            (self.addresstype,self.member_id,self.addrbook_id,self.orgunitname,self.field3,self.billingcode,self.billingcodetype,
            self.status,self.orgname,self.isprimary,self.lastname,self.persontitle,self.firstname,self.middlename,self.businesstitle,
            self.phone1,self.fax1,self.phone2,self.address1,self.fax2,self.nickname,self.address2,self.address3,self.city,self.state,
            self.country,self.zipcode,self.email1,self.email2,self.phone1type,self.phone2type,self.publishphone1,self.publishphone2,
            self.bestcallingtime,self.packagesuppression,self.lastcreate,self.officeaddress,self.selfaddress,self.field1,self.field2,
            self.taxgeocode,self.shippinggeocode,self.mobilephone1,self.mobilephone1cntry,self.address_id,))
            con.commit();return cursor.fetchone()[0]
        except (Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def save(self):
        try:
            cursor.execute("""insert into address(addresstype,member_id,addrbook_id,orgunitname,field3,billingcode,
            billingcodetype,status,orgname,isprimary,lastname,persontitle,firstname,middlename,businesstitle,phone1,
            fax1,phone2,address1,fax2,nickname,address2,address3,city,state,country,zipcode,email1,email2,phone1type,
            phone2type,publishphone1,publishphone2,bestcallingtime,packagesuppression,lastcreate,officeaddress,selfaddress,
            field1,field2,taxgeocode,shippinggeocode,mobilephone1,mobilephone1cntry)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            on conflict(nickname)do update set addresstype=%s,member_id=%s,addrbook_id=%s,orgunitname=%s,field3=%s,
            billingcode=%s,billingcodetype=%s,status=%s,orgname=%s,isprimary=%s,lastname=%s,persontitle=%s,firstname=%s,
            middlename=%s,businesstitle=%s,phone1=%s,fax1=%s,phone2=%s,address1=%s,fax2=%s,nickname=%s,
            address2=%s,address3=%s,city=%s,state=%s,country=%s,zipcode=%s,email1=%s,email2=%s,phone1type=%s,phone2type=%s,
            publishphone1=%s,publishphone2=%s,bestcallingtime=%s,packagesuppression=%s,lastcreate=%s,officeaddress=%s,
            selfaddress=%s,field1=%s,field2=%s,taxgeocode=%s,shippinggeocode=%s,mobilephone1=%s,mobilephone1cntry=%s
            returning address_id""",(self.addresstype,self.member_id,self.addrbook_id,self.orgunitname,self.field3,
            self.billingcode,self.billingcodetype,self.status,self.orgname,self.isprimary,self.lastname,self.persontitle,
            self.firstname,self.middlename,self.businesstitle,self.phone1,self.fax1,self.phone2,self.address1,self.fax2,
            self.nickname,self.address2,self.address3,self.city,self.state,self.country,self.zipcode,self.email1,self.email2,
            self.phone1type,self.phone2type,self.publishphone1,self.publishphone2,self.bestcallingtime,self.packagesuppression,
            self.lastcreate,self.officeaddress,self.selfaddress,self.field1,self.field2,self.taxgeocode,self.shippinggeocode,
            self.mobilephone1,self.mobilephone1cntry,self.addresstype,self.member_id,self.addrbook_id,self.orgunitname,
            self.field3,self.billingcode,self.billingcodetype,self.status,self.orgname,self.isprimary,self.lastname,
            self.persontitle,self.firstname,self.middlename,self.businesstitle,self.phone1,self.fax1,self.phone2,self.address1,
            self.fax2,self.nickname,self.address2,self.address3,self.city,self.state,self.country,self.zipcode,self.email1,
            self.email2,self.phone1type,self.phone2type,self.publishphone1,self.publishphone2,self.bestcallingtime,
            self.packagesuppression,self.lastcreate,self.officeaddress,self.selfaddress,self.field1,self.field2,self.taxgeocode,
            self.shippinggeocode,self.mobilephone1,self.mobilephone1cntry,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Mbrattrval:
    def __init__(self,member_id,attrtype_id,mbrattr_id,storeent_id=None,floatvalue=None,integervalue=None,stringvalue=None,datetimevalue=None):
        self.storeent_id=storeent_id
        self.member_id=member_id
        self.attrtype_id=attrtype_id
        self.mbrattr_id=mbrattr_id
        self.floatvalue=floatvalue
        self.integervalue=integervalue
        self.stringvalue=stringvalue
        self.datetimevalue=datetimevalue
    
    def save(self):
        try:
            cursor.execute("""insert into mbrattrval(storeent_id,member_id,attrtype_id,mbrattr_id,floatvalue,integervalue,
            stringvalue,datetimevalue)values(%s,%s,%s,%s,%s,%s,%s,%s)returning mbrattrval_id""",(self.storeent_id,self.member_id,
            self.attrtype_id,self.mbrattr_id,self.floatvalue,self.integervalue,self.stringvalue,self.datetimevalue,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Mbrattr:
    def __init__(self,attrtype_id,name,description):
        self.attrtype_id=attrtype_id
        self.name=name
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into mbrattr(attrtype_id,name,description)values(%s,%s,%s)on conflict(name)
            do update set attrtype_id=%s,name=%s,description=%s returning mbrattr_id""",(self.attrtype_id,self.name,
            self.description,self.attrtype_id,self.name,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Attrtype:
    def __init__(self,attrtype_id,description=None,oid=None):
        self.attrtype_id=attrtype_id
        self.description=description
        self.oid=oid
    
    def save(self):
        try:
            cursor.execute("""insert into attrtype(attrtype_id,description,oid)values(%s,%s,%s)
            on conflict(attrtype_id)do update set attrtype_id=%s,description=%s,oid=%s returning attrtype_id""",
            (self.attrtype_id,self.description,self.oid,self.attrtype_id,self.description,self.oid,))
            con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class RolePermDefaults:
    def __init__(self,orgentity_id):
        self.orgentity_id=orgentity_id
    
    def roles(self):
        cursor.execute("select role_id,name from role")
        res=cursor.fetchall()
        master=[x for x in res if x[1]=="permission_editor"][0]
        data=[ [master[0],self.orgentity_id,x[0]] for x in res ]
        return data
    
    def isfilled(self):
        cursor.execute("select count(roleasnprm_id)from roleasnprm")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False
    
    def save(self):
        filled=self.isfilled()
        if filled==False:[Roleasnprm(*p).save() for p in self.roles()]
        elif filled==True:pass
# RolePermDefaults(34).save()
class RoleDefaults:
    def __init__(self,fname):
        self.fname=fname
    
    def isfilled(self):
        cursor.execute("select count(role.role_id)from role left join roledesc on role.role_id=roledesc.role_id")
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
            roles=df.values[:,[1,2]];roleids=[Role(*r).save() for r in roles]
            df['role_id']=pd.Series(roleids);descriptions=df.values[:,[0,5,3,2]]
            [Roledesc(*d).save() for d in descriptions]

class UserSign:
    def __init__(self,logonid):
        self.logonid=logonid
        self.member_id=self.getmemberid()
        self.roles=self.getroles()
        self.employer=self.getemployer()
        self.language_id=self.getlangpref()
        self.profiletype=self.getprofiletype()
    
    def getmemberid(self):
        cursor.execute("select users_id from userreg where logonid=%s",(self.logonid,))
        return cursor.fetchone()[0]
    
    def getroles(self):
        cursor.execute("""with mbrrole as(select role_id from mbrrole where member_id=%s)
        select mbrrole.role_id,role.name,roledesc.displayname from role inner join mbrrole 
        on mbrrole.role_id=role.role_id inner join roledesc on mbrrole.role_id=roledesc.role_id""",
        (self.member_id,));return [dict(zip(['role_id','rolename','roledisplayname'],x))for x in cursor.fetchall()]
    
    def getemployer(self):
        cursor.execute("""with org as(select org_id from busprof where users_id=%s)
        select org.org_id,orgentity.orgentityname from org inner join orgentity on
        org.org_id=orgentity.orgentity_id""",(self.member_id,))
        return dict(zip(['employer','employername'],cursor.fetchone()))
    
    def getlangpref(self):
        cursor.execute("select language_id from users where users_id=%s",(self.member_id,))
        return cursor.fetchone()[0]

    def getprofiletype(self):
        cursor.execute("select profiletype from users where users_id=%s",(self.member_id,))
        return cursor.fetchone()[0].strip()

# u=UserSign('info@pronov.co')
# print(u.logonid)
# print(u.member_id)
# print(u.roles)
# print(u.employer)
# print(u.language_id)
# print(u.profiletype)

class ListAllMembers:
    def data(self):
        cursor.execute("""select member_id from member""")
        ids=[x for (x,) in cursor.fetchall()]
        return [self.details(i) for i in ids]
    
    def findmaster(self,roles):
        find=len([x for x in roles if x['rolename']=="Permission Editor"])
        if find<=0:return False
        elif find>0:return True
    
    def details(self,x):
        data=dict(member=Member.readmember(x),orgentity=Orgentity.readorgentity(x),mbrrole=Mbrrole.read(x),
        busprof=Busprof.readbusprof(x),userprof=Userprof.readuserprof(x),userreg=Userreg.readuserreg(x),
        users=Users.readusers(x),addrbook=Addrbook.readaddrbook(x),address=Address.readaddress(x))
        data.update(dict(ismaster=self.findmaster(data["mbrrole"])));return data

# print(ListAllMembers().data())

class UserProfile:
    def __init__(self,user_id):
        self.user_id=user_id
        self.type=self.getusertype()
    
    def getusertype(self):
        cursor.execute("select type from member where member_id=%s",(self.user_id,))
        return cursor.fetchone()[0]
    
    def getname(self):
        if self.type=='O':
            cursor.execute("select orgentityname from orgentity where orgentity_id=%s",(self.user_id,))
            return cursor.fetchone()[0]
        elif self.type=='U':
            cursor.execute("select field1,field3 from users where users_id=%s",(self.user_id,))
            res=cursor.fetchone();return "{} {}".format(res[0],res[1])
    
    # def getlogonid(self):
    #     cursor.execute("select logonid from ")