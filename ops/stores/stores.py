# from .db_con import createcon
# from db_con import createcon
import psycopg2
# con,cursor=createcon('retail','jmso','localhost','5432')
from ops.connector.connector import evcon
con,cursor=evcon()

import pandas as pd
import numpy as np
import os,re
from ops import CurrencyHelper,humanize_date,timestamp_forever,timestamp_now

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Storeorgs:
    def __init__(self,orgentitytype='O',profiletype='C'):
        self.orgentitytype=orgentitytype
        self.profiletype=profiletype

    def getdata(self):
        cursor.execute("""select users.users_id,orgentity.orgentityname from users inner join orgentity on
        users.users_id=orgentity.orgentity_id where orgentity.orgentitytype=%s and users.profiletype=%s
        """,(self.orgentitytype,self.profiletype,));res=cursor.fetchall()
        if len(res) <= 0:return [dict(users_id=None,orgentityname=None)]
        elif len(res) > 0:return [dict(users_id=r[0],orgentityname=r[1])for r in res]

class Storeent:
    def __init__(self,member_id,stype,identifier,setccurr=None,markfordelete=0):
        self.member_id=member_id
        self.type=stype
        self.identifier=identifier
        self.setccurr=setccurr
        self.markfordelete=markfordelete
    
    @staticmethod
    def get_image(store_id):
        cursor.execute("select staddress_id_loc from storeentds where storeent_id=%s",(store_id,))
        res=cursor.fetchone();staddress_id=None
        if res==None:staddress_id=None
        elif res!=None:staddress_id=res[0]
        return Storeent.addressinfo(staddress_id)

    @staticmethod
    def mapstoretype(stype):
        if stype==None:return None
        elif stype=='S':return 'Store'
        elif stype=='G':return 'StoreGroup'
    
    @staticmethod
    def addressinfo(staddress_id):
        st=Staddress.read(staddress_id)
        return dict(address=st['address1'],city=st['city'],state=st['state'],country=st['country'],
        email=st['email1'],phone=st['phone1'],image=st['field1'],contact="{0} {2}".format(st['firstname'],
        st['middlename'],st['lastname']))

    @staticmethod
    def readstores(owner_id):
        cursor.execute("""select storeent.member_id,storeent.storeent_id,storeent.identifier,storeent.type,
        storeent.setccurr,storeentds.staddress_id_loc,setcurrdsc.description from storeent inner join storeentds 
        on storeent.storeent_id=storeentds.storeent_id left join setcurrdsc on storeent.setccurr=setcurrdsc.setccurr
        where storeent.member_id != %s""",(owner_id,));res=cursor.fetchall()
        if len(res) <= 0:return [dict(member_id=None,storeent_id=None,name=None,type=None,currency=None,staddress_id=None,
        staddress=None,address=None,city=None,state=None,country=None,email=None,phone=None,image=None,firstname=None,
        middlename=None,lastname=None)]
        elif len(res) > 0:
            data=[dict(member_id=r[0],storeent_id=r[1], name=r[2],type=Storeent.mapstoretype(r[3]),setccurr=r[4],
            staddress_id=r[5],currency=r[6]) for r in res]
            [x.update(Storeent.addressinfo(x['staddress_id'])) for x in data ];return data

    @staticmethod
    def yourstore(owner_id):
        cursor.execute("""select storeent.storeent_id,storeent.identifier,storeent.type,storeent.setccurr,
        storeentds.staddress_id_loc,setcurrdsc.description from storeent inner join storeentds on storeent.
        storeent_id=storeentds.storeent_id left join setcurrdsc on storeent.setccurr=setcurrdsc.setccurr
        where storeent.member_id=%s""",(owner_id,));res=cursor.fetchall()
        if len(res) <= 0:return [dict(storeent_id=None,name=None,type=None,currency=None,staddress_id=None,staddress=None,
        address=None,city=None,state=None,country=None,email=None,phone=None,image=None,firstname=None,middlename=None,
        lastname=None)]
        elif len(res) > 0:
            data=[dict(storeent_id=r[0], name=r[1],type=Storeent.mapstoretype(r[2]),setccurr=r[3],staddress_id=r[4],
            currency=r[5]) for r in res];[x.update(Storeent.addressinfo(x['staddress_id'])) for x in data ];return data
    
    @staticmethod
    def read(mid,lid):
        cursor.execute("""select storeent.storeent_id,storeent.identifier,storeent.type,storeent.setccurr,
        storeent.markfordelete,storeentds.staddress_id_loc,storeentds.description from storeent inner join
        storeentds on storeent.storeent_id=storeentds.storeent_id where storeent.member_id=%s and storeentds.
        language_id=%s""",(mid,lid,));res=cursor.fetchall()
        if len(res) <= 0:return [dict(storeent_id=None,identifier=None,stype=None,setccurr=None,markfordelete=None,
        staddress_id_loc=None,description=None)]
        elif len(res) > 0:return [dict(storeent_id=r[0],identifier=r[1],stype=r[2],stypetext=Storeent.mapstoretype(r[2]),
        setccurr=r[3],markfordelete=r[4],staddress_id_loc=Staddress.read(r[5]),description=r[6])for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into storeent(member_id,type,setccurr,identifier,markfordelete)
            values(%s,%s,%s,%s,%s)on conflict(identifier,member_id)do update set member_id=%s,type=%s,
            setccurr=%s,identifier=%s,markfordelete=%s returning storeent_id""",(self.member_id,self.type,
            self.setccurr,self.identifier,self.markfordelete,self.member_id,self.type,self.setccurr,
            self.identifier,self.markfordelete,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

# print(Storeent.readstores())

class Storeentds:
    def __init__(self,language_id,storeent_id,displayname=None,staddress_id_loc=None,description=None,staddress_id_cont=None):
        self.language_id=language_id
        self.storeent_id=storeent_id
        self.displayname=displayname
        self.staddress_id_loc=staddress_id_loc
        self.description=description
        self.staddress_id_cont=staddress_id_cont
    
    def update(self):
        try:
            cursor.execute("""update storeentds set language_id=%s,storeent_id=%s,displayname=%s,
            staddress_id_loc=%s,description=%s,staddress_id_cont=%s returning storeent_id""",(self.language_id,
            self.storeent_id,self.displayname,self.staddress_id_loc,self.description,self.staddress_id_cont,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    def save(self):
        try:
            cursor.execute("""insert into storeentds(language_id,storeent_id,displayname,staddress_id_loc,
            description,staddress_id_cont)values(%s,%s,%s,%s,%s,%s)on conflict(language_id,storeent_id)do update
            set language_id=%s,storeent_id=%s,displayname=%s,staddress_id_loc=%s,description=%s,staddress_id_cont=%s
            returning storeent_id""",(self.language_id,self.storeent_id,self.displayname,self.staddress_id_loc,
            self.description,self.staddress_id_cont,self.language_id,self.storeent_id,self.displayname,self.staddress_id_loc,
            self.description,self.staddress_id_cont,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError)as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Store:
    def __init__(self,store_id,storegrp_id,storecgry_id=None,language_id=None,ffmcenter_id=None,status=1,storelevel=None,
    quotegoodfor=43200,field1=None,field2=None,allocationgoodfor=43200,maxbooffset=7776000,rejectedorexpiry=259200,
    ffmselectionflags=0,bopmpadfactor=0,rtnffmctr_id=None,defaultbooffset=7776000,pricerefflags=0,storetype=None,
    rmagoodfor=86400,avsacceptcodes=None,crtdbycntr_id=None,lastupdatedstatus=None,allocationoffset=86400,
    maxfooffset=7776000,inventoryopflag=0,blockingactive=1,persistentsession=None,orderhistoryactive='Y',
    inventorysystem=-1):
        self.store_id=store_id
        self.storegrp_id=storegrp_id
        self.storecgry_id=storecgry_id
        self.language_id=language_id
        self.ffmcenter_id=ffmcenter_id
        self.status=status
        self.storelevel=storelevel
        self.quotegoodfor=quotegoodfor
        self.field1=field1
        self.field2=field2
        self.allocationgoodfor=allocationgoodfor
        self.maxbooffset=maxbooffset
        self.rejectedorexpiry=rejectedorexpiry
        self.ffmselectionflags=ffmselectionflags
        self.bopmpadfactor=bopmpadfactor
        self.rtnffmctr_id=rtnffmctr_id
        self.defaultbooffset=defaultbooffset
        self.pricerefflags=pricerefflags
        self.storetype=storetype
        self.rmagoodfor=rmagoodfor
        self.avsacceptcodes=avsacceptcodes
        self.crtdbycntr_id=crtdbycntr_id
        self.lastupdatedstatus=lastupdatedstatus
        self.allocationoffset=allocationoffset
        self.maxfooffset=maxfooffset
        self.inventoryopflag=inventoryopflag
        self.blockingactive=blockingactive
        self.persistentsession=persistentsession
        self.orderhistoryactive=orderhistoryactive
        self.inventorysystem=inventorysystem
    
    def save(self):
        try:
            cursor.execute("""insert into store(store_id,storegrp_id,storecgry_id,language_id,ffmcenter_id,status,storelevel,
            quotegoodfor,field1,field2,allocationgoodfor,maxbooffset,rejectedorexpiry,ffmselectionflags,bopmpadfactor,rtnffmctr_id,
            defaultbooffset,pricerefflags,storetype,rmagoodfor,avsacceptcodes,crtdbycntr_id,lastupdatestatus,allocationoffset,
            maxfooffset,inventoryopflag,blockingactive,persistentsession,orderhistoryactive,inventorysystem)values(%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(store_id)do update set
            store_id=%s,storegrp_id=%s,storecgry_id=%s,language_id=%s,ffmcenter_id=%s,status=%s,storelevel=%s,quotegoodfor=%s,
            field1=%s,field2=%s,allocationgoodfor=%s,maxbooffset=%s,rejectedorexpiry=%s,ffmselectionflags=%s,bopmpadfactor=%s,
            rtnffmctr_id=%s,defaultbooffset=%s,pricerefflags=%s,storetype=%s,rmagoodfor=%s,avsacceptcodes=%s,crtdbycntr_id=%s,
            lastupdatestatus=%s,allocationoffset=%s,maxfooffset=%s,inventoryopflag=%s,blockingactive=%s,persistentsession=%s,
            orderhistoryactive=%s,inventorysystem=%s returning store_id""",(self.store_id,self.storegrp_id,self.storecgry_id,
            self.language_id,self.ffmcenter_id,self.status,self.storelevel,self.quotegoodfor,self.field1,self.field2,
            self.allocationgoodfor,self.maxbooffset,self.rejectedorexpiry,self.ffmselectionflags,self.bopmpadfactor,self.rtnffmctr_id,
            self.defaultbooffset,self.pricerefflags,self.storetype,self.rmagoodfor,self.avsacceptcodes,self.crtdbycntr_id,
            self.lastupdatedstatus,self.allocationoffset,self.maxfooffset,self.inventoryopflag,self.blockingactive,self.persistentsession,
            self.orderhistoryactive,self.inventorysystem,self.store_id,self.storegrp_id,self.storecgry_id,
            self.language_id,self.ffmcenter_id,self.status,self.storelevel,self.quotegoodfor,self.field1,self.field2,
            self.allocationgoodfor,self.maxbooffset,self.rejectedorexpiry,self.ffmselectionflags,self.bopmpadfactor,self.rtnffmctr_id,
            self.defaultbooffset,self.pricerefflags,self.storetype,self.rmagoodfor,self.avsacceptcodes,self.crtdbycntr_id,
            self.lastupdatedstatus,self.allocationoffset,self.maxfooffset,self.inventoryopflag,self.blockingactive,self.persistentsession,
            self.orderhistoryactive,self.inventorysystem,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError)as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Streltyp:
    def __init__(self,streltyp_id,name=None):
        self.streltyp_id=streltyp_id
        self.name=name

    def save(self):
        try:
            cursor.execute("""insert into store(name,streltyp_id)values(%s,%s)on conflict(name)
            do update set streltyp_id=%s,name=%s returning streltyp_id""",(self.name,self.streltyp_id,
            self.name,self.streltyp_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Storerel:
    def __init__(self,streltyp_id,relatedstore_id,store_id,sequence=0,state=1):
        self.streltyp_id=streltyp_id
        self.relatedstore_id=relatedstore_id
        self.store_id=store_id
        self.sequence=sequence
        self.state=state
    
    def save(self):
        try:
            cursor.execute("""insert into storerel(streltyp_id,relatedstore_id,store_id,sequence,state)
            values(%s,%s,%s,%s,%s)on conflict(store_id,streltyp_id,relatedstore_id)do update set streltyp_id=%s,
            relatedstore_id=%s,store_id=%s,sequence=%s,state=%s returning store_id""",(self.streltyp_id,
            self.relatedstore_id,self.store_id,self.sequence,self.state,self.streltyp_id,self.relatedstore_id,
            self.store_id,self.sequence,self.state,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Storegrp:
    def __init__(self,storegrp_id,field1=None):
        self.storegrp_id=storegrp_id
        self.field1=field1

    def save(self):
        try:        
            cursor.execute("""insert into storegrp(storegrp_id,field1)values(%s,%s)
            on conflict(storegrp_id)do update set storegrp_id=%s,field1=%s returning storegrp_id""",
            (self.storegrp_id,self.field1,self.storegrp_id,self.field1,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError)as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Staddress:
    def __init__(self,nickname,member_id,address1=None,address2=None,address3=None,city=None,
    country=None,email1=None,email2=None,fax1=None,fax2=None,field1=None,field2=None,field3=None,
    phone1=None,phone2=None,state=None,zipcode=None,firstname=None,lastname=None,middlename=None,
    persontitle=None,businesstitle=None,shippinggeocode=None,taxgeocode=None,url=None):
        self.nickname=nickname
        self.member_id=member_id
        self.address1=address1
        self.address2=address2
        self.address3=address3
        self.city=city
        self.country=country
        self.email1=email1
        self.email2=email2
        self.fax1=fax1
        self.fax2=fax2
        self.field1=field1
        self.field2=field2
        self.field3=field3
        self.phone1=phone1
        self.phone2=phone2
        self.state=state
        self.zipcode=zipcode
        self.firstname=firstname
        self.lastname=lastname
        self.middlename=middlename
        self.persontitle=persontitle
        self.businesstitle=businesstitle
        self.shippinggeocode=shippinggeocode
        self.taxgeocode=taxgeocode
        self.url=url
    
    @staticmethod
    def read(staddress_id):
        cursor.execute("""select address1,member_id,address2,address3,city,country,email1,email2,fax1,fax2,field1,
        field2,field3,phone1,phone2,state,zipcode,firstname,lastname,middlename,persontitle,businesstitle,nickname,
        shippinggeocode,taxgeocode,url from staddress where staddress_id=%s""",(staddress_id,));res=cursor.fetchone()
        if len(res) <= 0:return dict(address1=None,member_id=None,address2=None,address3=None,city=None,country=None,
        email1=None,email2=None,fax1=None,fax2=None,field1=None,field2=None,field3=None,phone1=None,phone2=None,
        state=None,zipcode=None,firstname=None,lastname=None,middlename=None,persontitle=None,businesstitle=None,
        nickname=None,shippinggeocode=None,taxgeocode=None,url=None)
        elif len(res) > 0:return dict(address1=res[0],member_id=res[1],address2=res[2],address3=res[3],city=res[4],country=res[5],
        email1=res[6],email2=res[7],fax1=res[8],fax2=res[9],field1=res[10],field2=res[11],field3=res[12],phone1=res[13],phone2=res[14],
        state=res[15],zipcode=res[16],firstname=res[17],lastname=res[18],middlename=res[19],persontitle=res[20],businesstitle=res[21],
        nickname=res[22],shippinggeocode=res[23],taxgeocode=res[24],url=res[25])
    
    def save(self):
        try:
            cursor.execute("""insert into staddress(address1,member_id,address2,address3,city,country,email1,email2,
            fax1,fax2,field1,field2,field3,phone1,phone2,state,zipcode,firstname,lastname,middlename,persontitle,
            businesstitle,nickname,shippinggeocode,taxgeocode,url)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(member_id,nickname)do update set address1=%s,
            member_id=%s,address2=%s,address3=%s,city=%s,country=%s,email1=%s,email2=%s,fax1=%s,fax2=%s,field1=%s,
            field2=%s,field3=%s,phone1=%s,phone2=%s,state=%s,zipcode=%s,firstname=%s,lastname=%s,middlename=%s,
            persontitle=%s,businesstitle=%s,nickname=%s,shippinggeocode=%s,taxgeocode=%s,url=%s returning staddress_id""",
            (self.address1,self.member_id,self.address2,self.address3,self.city,self.country,self.email1,self.email2,
            self.fax1,self.fax2,self.field1,self.field2,self.field3,self.phone1,self.phone2,self.state,self.zipcode,
            self.firstname,self.lastname,self.middlename,self.persontitle,self.businesstitle,self.nickname,self.shippinggeocode,
            self.taxgeocode,self.url,self.address1,self.member_id,self.address2,self.address3,self.city,self.country,self.email1,self.email2,
            self.fax1,self.fax2,self.field1,self.field2,self.field3,self.phone1,self.phone2,self.state,self.zipcode,
            self.firstname,self.lastname,self.middlename,self.persontitle,self.businesstitle,self.nickname,self.shippinggeocode,
            self.taxgeocode,self.url,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Staddress.read(1))
class Curlist:
    def __init__(self,storeent_id,currstr):
        self.storeent_id=storeent_id
        self.currstr=currstr
    
    def save(self):
        try:
            cursor.execute("""insert into curlist(storeent_id,currstr)values(%s,%s)on conflict(currstr,storeent_id)
            do update set storeent_id=%s,currstr=%s returning currstr""",(self.storeent_id,self.currstr,self.storeent_id,
            self.currstr,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Storelang:
    def __init__(self,language_id,storeent_id,setccurr=None):
        self.storeent_id=storeent_id
        self.language_id=language_id
        self.setccurr=setccurr
    
    def save(self):
        try:
            cursor.execute("""insert into storelang(language_id,storeent_id,setccurr)values(%s,%s,%s)
            on conflict(language_id,storeent_id)do update set language_id=%s,storeent_id=%s,setccurr=%s
            returning language_id""",(self.language_id,self.storeent_id,self.setccurr,self.language_id,
            self.storeent_id,self.setccurr,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ffmcenter:
    def __init__(self,member_id,name=None,defaultshippingoffset=86400,markfordelete=0,
    extffmstorenum=None,inventoryopflags=0,maxnumpick=25,pickdelaymin=5,dropship='N'):
        self.member_id=member_id
        self.name=name
        self.defaultshippingoffset=defaultshippingoffset
        self.markfordelete=markfordelete
        self.extffmstorenum=extffmstorenum
        self.inventoryopflags=inventoryopflags
        self.maxnumpick=maxnumpick
        self.pickdelaymin=pickdelaymin
        self.dropship=dropship
    
    @staticmethod
    def read(mid):
        cursor.execute("""select ffmcenter_id,name,defaultshipoffset,markfordelete,extffmstorenum,
        inventoryopflags,maxnumpick,pickdelayinmin,dropship from ffmcenter where member_id=%s""",(mid,))
        res=cursor.fetchall()
        if len(res) <= 0:return [dict(ffmcenter_id=None,name=None,defaultshipoffset=None,markfordelete=None,
        extffmstorenum=None,inventoryopflags=None,maxnumpick=None,pickdelayinmin=None,dropship=None)]
        elif len(res) > 0:return [dict(ffmcenter_id=r[0],name=r[1],defaultshipoffset=r[2],markfordelete=r[3],
        extffmstorenum=r[4],inventoryopflags=r[5],maxnumpick=r[6],pickdelayinmin=r[7],dropship=r[8])
        for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into ffmcenter(member_id,name,defaultshipoffset,markfordelete,extffmstorenum,
            inventoryopflags,maxnumpick,pickdelayinmin,dropship)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(member_id,name)
            do update set member_id=%s,name=%s,defaultshipoffset=%s,markfordelete=%s,extffmstorenum=%s,
            inventoryopflags=%s,maxnumpick=%s,pickdelayinmin=%s,dropship=%s returning ffmcenter_id""",(self.member_id,
            self.name,self.defaultshippingoffset,self.markfordelete,self.extffmstorenum,self.inventoryopflags,
            self.maxnumpick,self.pickdelaymin,self.dropship,self.member_id,
            self.name,self.defaultshippingoffset,self.markfordelete,self.extffmstorenum,self.inventoryopflags,
            self.maxnumpick,self.pickdelaymin,self.dropship,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.commit()
            raise EntryException(str(e).strip().split('\n')[0])

class Ffmcentds:
    def __init__(self,ffmcenter_id,language_id,staddress_id=None,description=None,displayname=None):
        self.ffmcenter_id=ffmcenter_id
        self.language_id=language_id
        self.staddress_id=staddress_id
        self.description=description
        self.displayname=displayname
    
    def save(self):
        try:
            cursor.execute("""insert into ffmcentds(ffmcenter_id,language_id,staddress_id,description,
            displayname)values(%s,%s,%s,%s,%s)on conflict(ffmcenter_id,language_id)do update set
            ffmcenter_id=%s,language_id=%s,staddress_id=%s,description=%s,displayname=%s returning ffmcenter_id""",
            (self.ffmcenter_id,self.language_id,self.staddress_id,self.description,self.displayname,
            self.ffmcenter_id,self.language_id,self.staddress_id,self.description,self.displayname,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class StoresForMember:
    def __init__(self,mid):
        self.mid=mid
    
    def _execute(self):
        cursor.execute("select storeent_id,identifier from storeent where member_id=%s",(self.mid,))
        res=cursor.fetchall()
        if len(res) <=0:return [dict(store_id=None,identifier=None)]
        elif len(res) > 0:return [dict(store_id=x[0],identifier=x[1]) for x in res]

class VendorsForMember:    
    def _execute(self):
        cursor.execute("select vendor_id,vendorname from vendor")
        res=cursor.fetchall()
        if len(res) <= 0:return [dict(vendor_id=None,name=None)]
        elif len(res) > 0:return [dict(vendor_id=r[0],name=r[1]) for r in res]

from ops.trading.trading import Trading,Trddesc,Contract,Cntrname,Participnt,Storedef,Storecntr
from ops.helpers.functions import datetimestamp_forever,datetimestamp_now

class MDefaultContract:
    def __init__(self,owner_id,store_id):
        self.store_id=store_id
        self.trdtype_id=1
        self.state=1
        self.starttime=datetimestamp_now()
        self.endtime=datetimestamp_forever()
        self.timecreated=self.starttime
        self.member_id=owner_id
        self.origin=0
        self.cstate=3
        self.usage=0
        self.timedeployed=self.starttime
        self.member_id=owner_id
        self.participant_id=owner_id
        self.language_id=1
        self.storename=self.getstorename()
        self.name="{}, ID-{}, Default Trading Agreement".format(self.storename,self.store_id)
        self.comment="A unilateral arrangement between the owner and the participant allowing customers to purchase products from the store at a specified price for a specified time under specific conditions."
    
    def getstorename(self):
        cursor.execute("select identifier from storeent where storeent_id=%s",(self.store_id,))
        res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res[0]
    
    def _execute(self):
        trading_id=Trading(self.trdtype_id,state=self.state,starttime=self.starttime,endtime=self.endtime).save()
        Trddesc(trading_id,self.language_id,longdescription=self.comment,timecreated=self.timecreated).save()
        contract_id=Contract(trading_id,self.name,self.member_id,origin=self.origin,state=self.cstate,usage=self.usage,comments=self.comment,timecreated=self.starttime,timedeployed=self.starttime).save()
        Cntrname(self.name,self.member_id,self.origin).save()
        Participnt(self.participant_id,1,contract_id,timecreated=self.starttime).save()
        Storedef(self.store_id,contract_id).save()
        Storecntr(contract_id,self.store_id).save()

from ops.helpers.functions import textualize_datetime
class MStoreent:
    def __init__(self,owner_id,language_id):
        self.owner_id=owner_id
        self.language_id=language_id

    def storeids(self):
        cursor.execute("select storeent_id from storeent where member_id=%s",(self.owner_id,))
        res=cursor.fetchall()
        if res==None:return res
        elif res!=None:return [x for (x,) in res]

    def readstore(self,storeent_id):
        cursor.execute("""select storeent.storeent_id,storeent.identifier,storeent.type::text,
        storeent.setccurr,storeentds.staddress_id_loc,setcurrdsc.description from storeent inner join
        storeentds on storeent.storeent_id=storeentds.storeent_id left join setcurrdsc on storeent.setccurr=
        setcurrdsc.setccurr where storeent.member_id=%s and storeent.storeent_id=%s""",
        (self.owner_id,storeent_id,));res=cursor.fetchone()
        if res != None:
            data=dict(owner_id=self.owner_id,storeent_id=res[0],identifier=res[1],storetype=res[2],
            setccurr=res[3],staddress_id_loc=res[4],currency=res[5],type=Storeent.mapstoretype(res[2]))
            data.update(Storeent.addressinfo(data['staddress_id_loc']));return data
        elif res==None:return None

    def radetail(self,ra_id):
        cursor.execute("""select radetail.radetail_id,radetail.ffmcenter_id,ffmcenter.name,radetail.itemspc_id,
        radetail.qtyordered,radetail.qtyreceived,radetail.qtyremaining,radetail.qtyallocated,radetail.expecteddate,
        radetail.radetailcomment,radetail.lastupdate from radetail inner join ffmcenter on radetail.ffmcenter_id=
        ffmcenter.ffmcenter_id where radetail.ra_id=%s""",(ra_id,));res=cursor.fetchall()
        if len(res)<=0:return None
        elif len(res)>0:return [dict(radetail_id=r[0],ffmcenter_id=r[1],name=r[2],itemspc_id=r[3],qtyordered=r[4],
        qtyreceived=r[5],qtyremaining=r[6],qtyallocated=r[7],t_expecteddate=textualize_datetime(r[8]),
        h_expecteddate=humanize_date(r[8]),radetailcomment=r[9],t_lastupdate=textualize_datetime(r[10]),
        h_lastupdate=humanize_date(r[10])) for r in res]

    # def receipt(self,radetail_id,store_id):
    #     cursor.execute("""select receipt.receipt_id,receipt.versionspc_id,receipt.radetail_id,receipt.store_id,
    #     receipt.setccurr,receipt.ffmcenter_id,receipt.vendor_id,receipt.receiptdate,receipt.qtyreceived,
    #     receipt.qtyinprocess,receipt.qtyonhand,receipt,qtyinkits,receipt.cost,receipt.comment1,receipt.comment2,
    #     receipt.lastupdate,receipt.createtime,receipt.receipttype,receipt.rtnrcptdsp_id where receipt.radetail_id=
    #     %s and receipt.store_id=%s""",(radetail_id,store_id,));res=cursor.fetchall()
    #     if len(res)<=0:return None
    #     elif len(res) > 0:return [dict(receipt_id=r[0],versionspc_id=r[1],radetail_id=r[2],store_id=r[3],
    #     setccurr=r[4],ffmcenter_id=r[5],vendor_id=r[6],receiptdate=humanize_date(r[7]), )]

    def ra(self,store_id):
        cursor.execute("""select ra.ra_id,ra.vendor_id,vendor.vendorname,ra.orderdate,ra.openindicator,
        ra.dateclosed,ra.lastupdate,ra.externalid::text,ra.createtime from ra inner join vendor on ra.vendor_id=
        vendor.vendor_id where ra.store_id=%s""",(store_id,));res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return dict(ra_id=res[0],vendor_id=res[1],vendorname=res[2],
        h_orderdate=humanize_date(res[3]),t_orderdate=textualize_datetime(res[3]),openindicator=res[4],
        h_dateclosed=humanize_date(res[5]),t_dateclosed=textualize_datetime(res[5]),
        t_lastupdate=textualize_datetime(res[6]),h_lastupdate=humanize_date(res[6]),externalid=res[7],
        t_createtime=textualize_datetime(res[8]),h_createtime=humanize_date(res[8]),
        radetail=self.radetail(res[0]))
    
    def inventory(self,store_id):
        cursor.execute("""select inventory.catentry_id,catentdesc.name,inventory.quantity::float,inventory.store_id,
        storeent.identifier,inventory.ffmcenter_id,ffmcenter.name from inventory inner join catentdesc on 
        inventory.catentry_id=catentdesc.catentry_id inner join storeent on inventory.store_id=storeent.
        storeent_id inner join ffmcenter on inventory.ffmcenter_id=ffmcenter.ffmcenter_id where inventory.
        store_id=%s""",(store_id,));res=cursor.fetchall()
        if len(res)<=0:return None
        elif len(res) >0:return [dict(catentry_id=r[0],name=r[1],quantity=r[2],storeent_id=r[3],
        store=r[4],ffmcenter_id=r[5],warehouse=r[6]) for r in res]

