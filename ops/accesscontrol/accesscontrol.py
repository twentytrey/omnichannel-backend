# from .db_con import createcon
# from db_con import createcon
import psycopg2
# con,cursor=createcon('retail','jmso','localhost','5432')
from ops.connector.connector import evcon
con,cursor=evcon()


class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Acclogmain:
    def __init__(self,users_id,storeent_id,threadid=None,hostname=None):
        self.users_id=users_id
        self.storeent_id=storeent_id
        self.threadid=threadid
        self.hostname=hostname
    
    def save(self):
        try:
            cursor.execute("""insert into acclogmain(threadid,hostname,storeent_id,users_id)values(%s,%s,%s,%s)
            returning acclogmain_id""",(self.threadid,self.hostname,self.storeent_id,self.users_id,));con.commit()
            return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acclogsub:
    def __init__(self,acclogmain_id,users_id,logtime=None,action=None,result=None,resources=None):
        self.acclogmain_id=acclogmain_id
        self.users_id=users_id
        self.logtime=logtime
        self.action=action
        self.result=result
        self.resources=resources
    
    def save(self):
        try:
            cursor.execute("""insert into acclogsub(acclogmain_id,logtime,action,result,resources,users_id)
            values(%s,%s,%s,%s,%s,%s)returning acclogsub_id""",(self.acclogmain_id,self.logtime,self.action,self.result,
            self.resources,self.users_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Roleasnprm:
    def __init__(self,assigning_role_id,orgentity_id,assignable_role_id):
        self.assigning_role_id=assigning_role_id
        self.orgentity_id=orgentity_id
        self.assignable_role_id=assignable_role_id
    
    def save(self):
        try:
            cursor.execute("""insert into roleasnprm(assigning_role_id,orgentity_id,assignable_role_id)
            values(%s,%s,%s)on conflict(assigning_role_id,orgentity_id,assignable_role_id)do update set
            assigning_role_id=%s,orgentity_id=%s,assignable_role_id=%s returning roleasnprm_id""",
            (self.assigning_role_id,self.orgentity_id,self.assignable_role_id,self.assigning_role_id,
            self.orgentity_id,self.assignable_role_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acaction:
    def __init__(self,action):
        self.action=action
    
    def save(self):
        try:
            cursor.execute("""insert into acaction(action)values(%s)returning acaction_id""",(self.action,))
            con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acactdesc:
    def __init__(self,acaction_id,displayname,language_id,description=None):
        self.acaction_id=acaction_id
        self.displayname=displayname
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into acactdesc(acaction_id,displayname,description,language_id)values(%s,%s,%s,%s)
            on conflict(acaction_id,language_id)do update set acaction_id=%s,displayname=%s,description=%s,language_id=%s
            returning acaction_id""",(self.acaction_id,self.displayname,self.description,self.language_id,self.acaction_id,
            self.displayname,self.description,self.language_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acpolicy:
    def __init__(self,acactgrp_id,acresgrp_id,mbrgrp_id,member_id,policyname=None,acrelgrp_id=None,acrelation_id=None,
    policytype=None,field1=None):
        self.acactgrp_id=acactgrp_id
        self.acresgrp_id=acresgrp_id
        self.mbrgrp_id=mbrgrp_id
        self.member_id=member_id
        self.policyname=policyname
        self.acrelgrp_id=acrelgrp_id
        self.acrelation_id=acrelation_id
        self.policytype=policytype
        self.field1=field1
    
    def save(self):
        try:
            cursor.execute("""insert into acpolicy(policyname,acrelgrp_id,acactgrp_id,acresgrp_id,acrelation_id,policytype,
            field1,mbrgrp_id,member_id)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(policyname,member_id)do update set
            policyname=%s,acrelgrp_id=%s,acactgrp_id=%s,acresgrp_id=%s,acrelation_id=%s,policytype=%s,
            field1=%s,mbrgrp_id=%s,member_id=%s returning acpolicy_id""",(self.policyname,self.acrelgrp_id,self.acactgrp_id,
            self.acresgrp_id,self.acrelation_id,self.policytype,self.field1,self.mbrgrp_id,
            self.member_id,self.policyname,self.acrelgrp_id,self.acactgrp_id,
            self.acresgrp_id,self.acrelation_id,self.policytype,self.field1,self.mbrgrp_id,self.member_id,))
            con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acpoldesc:
    def __init__(self,acpolicy_id,language_id,displayname,description=None):
        self.acpolicy_id=acpolicy_id
        self.language_id=language_id
        self.displayname=displayname
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into acpoldesc(acpolicy_id,language_id,displayname,description)values(%s,%s,%s,%s)
            on conflict(acpolicy_id,language_id)do update set acpolicy_id=%s,language_id=%s,displayname=%s,description=%s
            returning acpolicy_id""",(self.acpolicy_id,self.language_id,self.displayname,self.description,self.acpolicy_id,
            self.language_id,self.displayname,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acactgrp:
    def __init__(self,groupname,member_id,field1):
        self.groupname=groupname
        self.member_id=member_id
        self.field1=field1
    
    def save(self):
        try:
            cursor.execute("""insert into acactgrp(groupname,member_id,field1)values(%s,%s,%s)on conflict(groupname)
            do update set groupname=%s,member_id=%s,field1=%s returning acactgrp_id""",(self.groupname,self.member_id,
            self.field1,self.groupname,self.member_id,self.field1,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acacgpdesc:
    def __init__(self,acactgrp_id,language_id,displayname=None,description=None):
        self.acactgrp_id=acactgrp_id
        self.language_id=language_id
        self.displayname=displayname
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into acacgpdesc(acactgrp_id,displayname,description,language_id)values(%s,%s,%s,%s)
            on conflict(acactgrp_id,language_id)do update set acactgrp_id=%s,displayname=%s,description=%s,language_id=%s
            returning acactgrp_id""",(self.acactgrp_id,self.displayname,self.description,self.language_id,self.acactgrp_id,
            self.displayname,self.description,self.language_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acresgrp:
    def __init__(self,member_id,grpname,description=None,conditions=None,field1=None,field2=None):
        self.member_id=member_id
        self.grpname=grpname
        self.description=description
        self.conditions=conditions
        self.field1=field1
        self.field2=field2
    
    def save(self):
        try:
            cursor.execute("""insert into acresgrp(member_id,grpname,description,conditions,field1,field2)values(%s,%s,%s,%s,%s,%s)
            on conflict(grpname)do update set member_id=%s,grpname=%s,description=%s,conditions=%s,field1=%s,field2=%s returning
            acresgrp_id""",(self.member_id,self.grpname,self.description,self.conditions,self.field1,self.field2,self.member_id,
            self.grpname,self.description,self.conditions,self.field1,self.field2,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acresgpdes:
    def __init__(self,acresgrp_id,displayname,language_id,description=None):
        self.acresgrp_id=acresgrp_id
        self.displayname=displayname
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into acresgpdes(acresgrp_id,displayname,description,language_id)values(%s,%s,%s,%s)
            on conflict(acresgrp_id,language_id)do update set acresgrp_id=%s,displayname=%s,description=%s,language_id=%s
            returning acresgrp_id""",(self.acresgrp_id,self.displayname,self.description,self.language_id,self.acresgrp_id,
            self.displayname,self.description,self.language_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acpolgrp:
    def __init__(self,name,member_id):
        self.name=name
        self.member_id=member_id
    
    def save(self):
        try:
            cursor.execute("""insert into acpolgrp(name,member_id)values(%s,%s)on conflict(name,member_id)do update set
            name=%s,member_id=%s returning acpolgrp_id""",(self.name,self.member_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acplgpdesc:
    def __init__(self,acpolgrp_id,language_id,displayname,description=None):
        self.acpolgrp_id=acpolgrp_id
        self.language_id=language_id
        self.displayname=displayname
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into acplgpdesc(acpolgrp_id,language_id,displayname,description)values(%s,%s,%s,%s)
            on conflict(acpolgrp_id,language_id)do update set acpolgrp_id=%s,language_id=%s,displayname=%s,description=%s
            returning acpolgrp_id""",(self.acpolgrp_id,self.language_id,self.displayname,self.description,self.acpolgrp_id,
            self.language_id,self.displayname,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acpolsubgp:
    def __init__(self,child_id,parent_id):
        self.child_id=child_id
        self.parent_id=parent_id
    
    def save(self):
        try:
            cursor.execute("""insert into acpolsubgp(child_id,parent_id)values(%s,%s)on conflict(child_id,parent_id)
            do update set child_id=%s,parent_id=%s returning child_id""",(self.child_id,self.parent_id,self.child_id,
            self.parent_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acplgpsubs:
    def __init__(self,acpolgrp_id,orgentity_id):
        self.acpolgrp_id=acpolgrp_id
        self.orgentity_id=orgentity_id
    
    def save(self):
        try:
            cursor.execute("""insert into acplgpsubs(acpolgrp_id,orgentity_id)values(%s,%s)
            on conflict(orgentity_id,acpolgrp_id)do update set acpolgrp_id=%s,orgentity_id=%s
            returning acpolgrp_id""",(self.acpolgrp_id,self.orgentity_id,));con.commit()
            return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acpolgppol:
    def __init__(self,acpolicy_id,acpolgrp_id):
        self.acpolicy_id=acpolicy_id
        self.acpolgrp_id=acpolgrp_id
    
    def save(self):
        try:
            cursor.execute("""insert into acpolgppol(acpolicy_id,acpolgrp_id)values(%s,%s)on conflict(acpolicy_id,
            acpolgrp_id)do update set acpolicy_id=%s,acpolgrp_id=%s returning acpolicy_id""",(self.acpolicy_id,self.acpolgrp_id,
            self.acpolicy_id,self.acpolgrp_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acorgpol:
    def __init__(self,acpolicy_id,member_id):
        self.acpolicy_id=acpolicy_id
        self.member_id=member_id
    
    def save(self):
        try:
            cursor.execute("""insert into acorgpol(acpolicy_id,member_id)values(%s,%s)on conflict(acpolicy_id,member_id)
            do update set acpolicy_id=%s,member_id=%s returning acpolicy_id""",(self.acpolicy_id,self.member_id,self.acpolicy_id,
            self.member_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acresgpres:
    def __init__(self,acresgrp_id,acrescgry_id,field1=None):
        self.acresgrp_id=acresgrp_id
        self.acrescgry_id=acrescgry_id
        self.field1=field1
    
    def save(self):
        try:
            cursor.execute("""insert into acresgpres(acresgrp_id,acrescgry_id,field1)values(%s,%s,%s)
            on conflict(acresgrp_id,acrescgry_id)do update set acresgrp_id=%s,acrescgry_id=%s,field1=%s
            returning acresgrp_id""",(self.acresgrp_id,self.acrescgry_id,self.field1,self.acresgrp_id,
            self.acrescgry_id,self.field1,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acreldesc:
    def __init__(self,acrelation_id,displayname,language_id,description=None):
        self.acrelation_id=acrelation_id
        self.displayname=displayname
        self.description=description
        self.language_id=language_id
    
    def save(self):
        try:
            cursor.execute("""insert into acreldesc(acrelation_id,displayname,description,language_id)values(%s,%s,%s,%s)
            on conflict(acrelation_id,language_id)do update set acrelation_id=%s,displayname=%s,description=%s,
            language_id=%s returning acrelation_id""",(self.acrelation_id,self.displayname,self.description,self.language_id,
            self.acrelation_id,self.displayname,self.description,self.language_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acrelation:
    def __init__(self,relationname):
        self.relationname=relationname
    
    def save(self):
        try:
            cursor.execute("""insert into acrelation(relationname)values(%s)returning acrelation_id""",(self.relationname,))
            con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acresrel:
    def __init__(self,acrelation_id,acrescgry_id,resreltable,resrelmemcol,resrelkeycol=None,resrelcol=None,
    resjoincol=None,field1=None,resourcetype=None):
        self.acrelation_id=acrelation_id
        self.acrescgry_id=acrescgry_id
        self.resreltable=resreltable
        self.resrelmemcol=resrelmemcol
        self.resrelkeycol=resrelkeycol
        self.resrelcol=resrelcol
        self.resjoincol=resjoincol
        self.field1=field1
        self.resourcetype=resourcetype
    
    def save(self):
        try:
            cursor.execute("""insert into acresrel(acrelation_id,acrescgry_id,resreltable,resrelmemcol,resrelkeycol,resrelcol,
            resjoincol,field1,resourcetype)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(acrelation_id,acrescgry_id)do update
            set acrelation_id=%s,acrescgry_id=%s,resreltable=%s,resrelmemcol=%s,resrelkeycol=%s,resrelcol=%s,resjoincol=%s,
            field1=%s,resourcetype=%s returning acrelation_id""",(self.acrelation_id,self.acrescgry_id,self.resreltable,
            self.resrelmemcol,self.resrelkeycol,self.resrelcol,self.resjoincol,self.field1,self.resourcetype,self.acrelation_id,
            self.acrescgry_id,self.resreltable,self.resrelmemcol,self.resrelkeycol,self.resrelcol,self.resjoincol,self.field1,
            self.resourcetype,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acrescgry:
    def __init__(self,resprimarytable=None,resownertable=None,resownercol=None,reskeyowncol=None,field1=None,
    resclassname=None,resjoinkey=None):
        self.resprimarytable=resprimarytable
        self.resownertable=resownertable
        self.resownercol=resownercol
        self.reskeyowncol=reskeyowncol
        self.field1=field1
        self.resclassname=resclassname
        self.resjoinkey=resjoinkey
    
    def save(self):
        try:
            cursor.execute("""insert into acrescgry(resprimarytable,resownertable,resownercol,reskeyowncol,field1,
            resclassname,resjoinkey)values(%s,%s,%s,%s,%s,%s,%s)on conflict(resclassname)do update set resprimarytable=%s,
            resownertable=%s,resownercol=%s,reskeyowncol=%s,field1=%s,resclassname=%s,resjoinkey=%s returning acrescgry_id""",(self.resprimarytable,
            self.resownertable,self.resownercol,self.reskeyowncol,self.field1,self.resclassname,self.resjoinkey,
            self.resownertable,self.resownercol,self.reskeyowncol,self.field1,self.resclassname,self.resjoinkey,))
            con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acresact:
    def __init__(self,acrescgry_id,acaction_id):
        self.acrescgry_id=acrescgry_id
        self.acaction_id=acaction_id
    
    def save(self):
        try:
            cursor.execute("""insert into acresact(acrescgry_id,acaction_id)values(%s,%s)on conflict(acrescgry_id,acaction_id)
            do update set acrescgry_id=%s,acaction_id=%s returning acrescgry_id""",(self.acrescgry_id,self.acaction_id,
            self.acrescgry_id,self.acaction_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acrescgdes:
    def __init__(self,language_id,acrescgry_id,displayname,description=None):
        self.language_id=language_id
        self.acrescgry_id=acrescgry_id
        self.displayname=displayname
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into acrescgdes(language_id,acrescgry_id,displayname,description)values(%s,%s,%s,%s)
            on conflict(language_id,acrescgry_id)do update set language_id=%s,acrescgry_id=%s,displayname=%s,description=%s
            returning acrescgry_id""",(self.language_id,self.acrescgry_id,self.displayname,self.description,self.language_id,
            self.acrescgry_id,self.displayname,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acresprim:
    def __init__(self,acrescgry_id,resprimarycol,field1=None):
        self.acrescgry_id=acrescgry_id
        self.resprimarycol=resprimarycol
        self.field1=field1
    
    def save(self):
        try:
            cursor.execute("""insert into acresprim(acrescgry_id,resprimarycol,field1)values(%s,%s,%s)
            on conflict(acrescgry_id)do update set acrescgry_id=%s,resprimarycol=%s,field1=%s returning
            acrescgry_id""",(self.acrescgry_id,self.resprimarycol,self.field1,self.acrescgry_id,self.resprimarycol,
            self.field1,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acrelgrp:
    def __init__(self,member_id,grpname=None,field1=None,description=None):
        self.member_id=member_id
        self.grpname=grpname
        self.field1=field1
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into acrelgrp(member_id,grpname,field1,description)values(%s,%s,%s,%s)
            on conflict(grpname,member_id)do update set member_id=%s,grpname=%s,field1=%s,description=%s
            returning acrelgrp_id""",(self.member_id,self.grpname,self.field1,self.description,self.member_id,
            self.grpname,self.field1,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acresatrel:
    def __init__(self,acattr_id,acrescgry_id,attrtblname,attrcolname,reskeycolname,field1):
        self.acattr_id=acattr_id
        self.acrescgry_id=acrescgry_id
        self.attrtblname=attrtblname
        self.attrcolname=attrcolname
        self.reskeycolname=reskeycolname
        self.field1=field1
    
    def save(self):
        try:
            cursor.execute("""insert into acresatrel(acattr_id,acrescgry_id,attrtblname,attrcolname,reskeycolname,field1)
            values(%s,%s,%s,%s,%s,%s)on conflict(acattr_id,acrescgry_id)do update set acattr_id=%s,acrescgry_id=%s,attrtblname=%s,
            attrcolname=%s,reskeycolname=%s,field1=%s returning acattr_id""",(self.acattr_id,self.acrescgry_id,self.attrtblname,
            self.attrcolname,self.reskeycolname,self.field1,self.acattr_id,self.acrescgry_id,self.attrtblname,self.attrcolname,
            self.reskeycolname,self.field1,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acattr:
    def __init__(self,attrname,datatype,field1):
        self.attrname=attrname
        self.datatype=datatype
        self.field1=field1
    
    def save(self):
        try:
            cursor.execute("""insert into acattr(attrname,datatype,field1)values(%s,%s,%s)on conflict(attrname)
            do update set attrname=%s,datatype=%s,field1=%s returning acattr_id""",(self.attrname,self.datatype,self.field1,
            self.attrname,self.datatype,self.field1,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acresmemrl:
    def __init__(self,member_id,acrelation_id,acrescgry_id,resourceid=None):
        self.member_id=member_id
        self.acrelation_id=acrelation_id
        self.acrescgry_id=acrescgry_id
        self.resourceid=resourceid
    
    def save(self):
        try:
            cursor.execute("""insert into acresmemrl(resourceid,member_id,acrelation_id,acrescgry_id)values(%s,%s,%s,%s)
            on conflict(member_id,resourceid,acrelation_id,acrescgry_id)do update set resourceid=%s,member_id=%s,acrelation_id=%s,
            acrescgry_id=%s returning acresmemrl_id""",(self.resourceid,self.member_id,self.acrelation_id,self.acrescgry_id,
            self.resourceid,self.member_id,self.acrelation_id,self.acrescgry_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Acattrdesc:
    def __init__(self,acattr_id,displayname,language_id,description=None):
        self.acattr_id=acattr_id
        self.displayname=displayname
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into acattrdesc(acattr_id,displayname,description,language_id)values(%s,%s,%s,%s)
            on conflict(acattr_id,language_id)do update set acattr_id=%s,displayname=%s,description=%s,language_id=%s
            returning acattr_id""",(self.acattr_id,self.displayname,self.description,self.language_id,self.acattr_id,
            self.displayname,self.description,self.language_id,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])