from .db_con import createcon
# from db_con import createcon
import psycopg2
con,cursor=createcon('retail','jmso','localhost','5432')

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Member:
    def __init__(self,membertype,memberstate=None):
        self.membertype=membertype
        self.memberstate=memberstate
    
    def has_member(self,mid):
        try:
            cursor.execute("""select count(member_id) from member where member_id=%s""",
            (mid,));res=cursor.fetchone()
            if len(res) > 0:return True
            elif len(res) <=0: return False
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def save(self):
        try:
            cursor.execute("""insert into member(member_id,type,state)values(%s,%s)
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
        self.legalid=legalid
        self.orgentitytype=orgentityname
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
    
    def has_org(self,oid):
        try:
            cursor.execute("""select count(orgentity_id)from orgentity where
            orgentity_id=%s""",(oid,));res=cursor.fetchone()
            if len(res) > 0:return True
            elif len(res) <= 0:return False
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    def save(self):
        try:
            cursor.execute("""insert into orgentity(legalid,orgentitytype,orgentityname,
            businesscategory,description,adminfirstname,adminlastname,adminmiddlename,
            preferreddelivery,field1,field2,dn,taxpayerid,field3,status)values
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)returning orgentity_id""",
            (self.legalid,self.orgentitytype,self.orgentityname,self.businesscategory,
            self.description,self.adminfirstname,self.adminlastname,self.adminmiddlename,
            self.preferreddelivery,self.field1,self.field2,self.dn,self.taxpayerid,self.field3,
            self.status,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Busprof:
    def __init__(self,employeeid=None,org_id=None,orgunit_id=None,employeetype=None,
    departmentnum=None,alternateid=None,manager=None,secretary=None,requisitionerid=None):
        self.employeeid=employeeid
        self.org_id=org_id
        self.orgunit_id=orgunit_id
        self.employeetype=employeetype
        self.departmentnum=departmentnum
        self.alternateid=alternateid
        self.manager=manager
        self.secretary=secretary
        self.requisitionerid=requisitionerid
    
    def save(self):
        try:
            cursor.execute("""insert into busprof()""")
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])