from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","pronov","localhost","5432")
import  importlib
from ops import textualize_datetime,humanize_date,CurrencyHelper

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Shpjcrule:
    def __init__(self,calrule_id,ffmcenter_id=None,jurstgroup_id=None,precedence=0,shipmode_id=None):
        self.calrule_id=calrule_id
        self.ffmcenter_id=ffmcenter_id
        self.jurstgroup_id=jurstgroup_id
        self.precedence=precedence
        self.shipmode_id=shipmode_id
    
    def save(self):
        try:
            cursor.execute("""insert into shpjcrule(calrule_id,ffmcenter_id,jurstgroup_id,precedence,shipmode_id)
            values(%s,%s,%s,%s,%s)on conflict(ffmcenter_id,shipmode_id,jurstgroup_id,calrule_id)do update set
            calrule_id=%s,ffmcenter_id=%s,jurstgroup_id=%s,precedence=%s,shipmode_id=%s returning shpjcrule_id""",
            (self.calrule_id,self.ffmcenter_id,self.jurstgroup_id,self.precedence,self.shipmode_id,self.calrule_id,
            self.ffmcenter_id,self.jurstgroup_id,self.precedence,self.shipmode_id,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Shipmodclcd:
    def __init__(self,store_id,calcode_id,shipmode_id=None,trading_id=None):
        self.store_id=store_id
        self.calcode_id=calcode_id
        self.shipmode_id=shipmode_id
        self.trading_id=trading_id
    
    def save(self):
        try:
            cursor.execute("""insert into shipmodclcd(store_id,calcode_id,shipmode_id,trading_id)values(%s,%s,%s,%s)
            on conflict(store_id,calcode_id,shipmode_id,trading_id)do update set store_id=%s,calcode_id=%s,shipmode_id=%s,
            trading_id=%s""",(self.store_id,self.calcode_id,self.shipmode_id,self.trading_id,self.store_id,self.calcode_id,
            self.shipmode_id,self.trading_id,));con.commit()
        except(Exception,psycopg2.DatabaseError)as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Shipmode:
    def __init__(self,storeent_id,field1=None,field2=None,code=None,carrier=None,trackingname=None,
    trackingurl=None,trackinghost=None,trackingport=None,trackingicon=None,
    trackingtype=None,markfordelete=0):
        self.storeent_id=storeent_id
        self.field1=field1
        self.field2=field2
        self.code=code
        self.carrier=carrier
        self.trackingname=trackinghost
        self.trackingurl=trackingurl
        self.trackinghost=trackinghost
        self.trackingport=trackingport
        self.trackingicon=trackingicon
        self.trackingtype=trackingtype
        self.markfordelete=markfordelete
    
    @staticmethod
    def read(sid,lid):
        cursor.execute("""select shipmode.code,shipmode.carrier,shipmode.storeent_id,shipmodedsc.description from
        shipmode inner join shipmodedsc on shipmode.shipmode_id=shipmodedsc.shipmode_id where
        shipmode.storeent_id=%s and shipmodedsc.language_id=%s""",(sid,lid,))
        res=cursor.fetchall()
        if len(res) <= 0:return [dict(code=None,carrier=None,storeent_id=None,description=None)]
        elif len(res) > 0:return [dict(code=r[0],carrier=r[1],storeent_id=r[2],description=r[3],attached=r[2]!=None) 
        for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into shipmode(field1,storeent_id,field2,code,carrier,trackingname,trackingurl,
            trackinghost,trackingport,trackingicon,trackingtype,markfordelete)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s)on conflict(storeent_id,code,carrier)do update set field1=%s,storeent_id=%s,field2=%s,code=%s,
            carrier=%s,trackingname=%s,trackingurl=%s,trackinghost=%s,trackingport=%s,trackingicon=%s,trackingtype=%s,
            markfordelete=%s returning shipmode_id""",(self.field1,self.storeent_id,self.field2,self.code,self.carrier,
            self.trackingname,self.trackingurl,self.trackinghost,self.trackingport,self.trackingicon,self.trackingtype,
            self.markfordelete,self.field1,self.storeent_id,self.field2,self.code,self.carrier,
            self.trackingname,self.trackingurl,self.trackinghost,self.trackingport,self.trackingicon,self.trackingtype,
            self.markfordelete,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Shipmodedsc:
    def __init__(self,shipmode_id,language_id,description=None,field1=None,field2=None):
        self.shipmode_id=shipmode_id
        self.language_id=language_id
        self.description=description
        self.field1=field1
        self.field2=field2
    
    def save(self):
        try:
            cursor.execute("""insert into shipmodedsc(shipmode_id,language_id,description,field1,field2)
            values(%s,%s,%s,%s,%s)on conflict(shipmode_id,language_id)do update set shipmode_id=%s,
            language_id=%s,description=%s,field1=%s,field2=%s returning shipmode_id""",(self.shipmode_id,
            self.language_id,self.description,self.field1,self.field2,self.shipmode_id,self.language_id,
            self.description,self.field1,self.field2,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Shparrange:
    def __init__(self,store_id,ffmcenter_id,shipmode_id,startdate=None,enddate=None,trackingnumber=None,field1=None,
    precedence=0,field2=None,flags=0):
        self.store_id=store_id
        self.ffmcenter_id=ffmcenter_id
        self.shipmode_id=shipmode_id
        self.startdate=startdate
        self.enddate=enddate
        self.trackingnumber=trackingnumber
        self.field1=field1
        self.precedence=precedence
        self.field2=field2
        self.flags=flags
    
    def save(self):
        try:
            cursor.execute("""insert into shparrange(store_id,ffmcenter_id,shipmode_id,startdate,enddate,trackingnumber,
            field1,precedence,field2,flags)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(ffmcenter_id,shipmode_id,
            store_id,startdate,enddate)do update set store_id=%s,ffmcenter_id=%s,shipmode_id=%s,startdate=%s,enddate=%s,
            trackingnumber=%s,field1=%s,precedence=%s,field2=%s,flags=%s returning shparrange_id""",
            (self.store_id,self.ffmcenter_id,self.shipmode_id,self.startdate,self.enddate,self.trackingnumber,self.field1,
            self.precedence,self.field2,self.flags,
            self.store_id,self.ffmcenter_id,self.shipmode_id,self.startdate,self.enddate,self.trackingnumber,self.field1,
            self.precedence,self.field2,self.flags,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Shparjurgp:
    def __init__(self,shparrange_id,jurstgroup_id):
        self.shparrange_id=shparrange_id
        self.jurstgroup_id=jurstgroup_id
    
    def save(self):
        try:
            cursor.execute("""insert into shparjurgp(shparrange_id,jurstgroup_id)values(%s,%s)on conflict
            (shparrange_id,jurstgroup_id)do update set shparrange_id=%s,jurstgroup_id=%s""",
            (self.shparrange_id,self.jurstgroup_id,self.shparrange_id,self.jurstgroup_id,))
            con.commit()
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catencalcd:
    def __init__(self,store_id,trading_id=None,catentry_id=None,calcode_id=None,calflags=None):
        self.store_id=store_id
        self.trading_id=trading_id
        self.catentry_id=catentry_id
        self.calcode_id=calcode_id
        self.calflags=calflags
    
    def save(self):
        try:
            cursor.execute("""insert into catencalcd(store_id,trading_id,catentry_id,calcode_id,calflags)
            values(%s,%s,%s,%s,%s)on conflict(store_id,catentry_id,calcode_id,trading_id)do update set store_id=%s,
            trading_id=%s,catentry_id=%s,calcode_id=%s,calflags=%s returning catencalcd_id""",(self.store_id,
            self.trading_id,self.catentry_id,self.calcode_id,self.calflags,self.store_id,self.trading_id,self.catentry_id,
            self.calcode_id,self.calflags,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catgpcalcd:
    def __init__(self,store_id,trading_id,catgroup_id,calcode_id,calflags):
        self.store_id=store_id
        self.trading_id=trading_id
        self.catgroup_id=catgroup_id
        self.calcode_id=calcode_id
        self.calflags=calflags
    
    def save(self):
        try:
            cursor.execute("""insert into catgpcalcd(store_id,trading_id,catgroup_id,calcode_id,calflags)
            values(%s,%s,%s,%s,%s)on conflict(store_id,catgroup_id,calcode_id,trading_id)do update set 
            store_id=%s,trading_id=%s,catgroup_id=%s,calcode_id=%s,calflags=%s returning catgpcalcd_id""",
            (self.store_id,self.trading_id,self.catgroup_id,self.calcode_id,self.calflags,
            self.store_id,self.trading_id,self.catgroup_id,self.calcode_id,self.calflags,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class ShpCalrule:
    @staticmethod
    def codename(cid):
        if cid==None:return None
        elif cid != None:
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
        calrule.field1,calrule.field2,calrule.flags,calrule.identifier,shpjcrule.ffmcenter_id,shpjcrule.
        jurstgroup_id from calrule left join shpjcrule on calrule.calrule_id=shpjcrule.calrule_id""")
        res=cursor.fetchall()
        if len(res) <=0: return [dict(calrule_id=None,calcode_id=None,startdate=None,taxcgry_id=None,
        enddate=None,sequence=None,combination=None,calmethod_id=None,calmethod_id_qfy=None,field1=None,
        field2=None,flags=None,identifier=None,ffmcenter_id=None,jurstgroup_id=None)]
        elif len(res) > 0:return [dict(calrule_id=r[0],calcode_id=r[1],tax_code=ShpCalrule.codename(r[1]),
        startdate=r[2],taxcgry_id=r[3],tax_category=r[3],enddate=r[4],sequence=r[5],combination=r[6],
        calmethod_id=r[7],calculation=ShpCalrule.methodnames(r[7]),calmethod_id_qfy=r[8],
        qualification=ShpCalrule.methodnames(r[8]),field1=r[9],field2=r[10],flags=r[11],identifier=r[12],
        ffmcenter_id=r[13],shipping=ShpCalrule.ffmcenter(r[13]),jurstgroup_id=r[14],
        jurisdiction=ShpCalrule.jurstnames(r[14]))for r in res]
# print(ShpCalrule.read())
class MethodsFromCalcode:
    def __init__(self,calcode_id):
        self.calcode_id=calcode_id
        self.calusage_id=self.gettaxtype()
    
    def gettaxtype(self):
        cursor.execute("select calusage_id from calcode where calcode_id=%s",(self.calcode_id,))
        return cursor.fetchone()[0]
    
    def getmethods(self):
        cursor.execute("select calmethod_id,name from calmethod where calusage_id=%s",(self.calusage_id,))
        return [dict(text=x[1],value=x[0])for x in cursor.fetchall()]
# print(MethodsFromCalcode(2).getmethods())

class ShippingPolicy:
    def __init__(self,language_id,policytype_id):
        self.language_id=language_id
        self.policytype_id=policytype_id
    
    def read(self):
        cursor.execute("""select policy.policy_id,policy.policyname,policy.policytype_id::text,
        policy.storeent_id,storeent.identifier,policy.properties,policy.starttime,policy.endtime,
        policydesc.description,policydesc.timecreated,policydesc.timeupdated from policy inner join 
        storeent on policy.storeent_id=storeent.storeent_id inner join
        policydesc on policy.policy_id=policydesc.policy_id where policy.policytype_id=%s and 
        policydesc.language_id=%s""",(self.policytype_id,self.language_id,))
        res=cursor.fetchall()
        if len(res) <=0:return [dict()]
        elif len(res)>0:return[dict(policy_id=r[0],name=r[1],type=r[2],storeent_id=r[3],store=r[4],
        properties=r[5],starttime=textualize_datetime(r[6]),endtime=textualize_datetime(r[7]),
        description=r[8],created=humanize_date(r[9]),updated=humanize_date(r[10])) for r in res]
