from .db_con import createcon
# from db_con import createcon
import psycopg2
con,cursor=createcon('retail','pronov','localhost','5432')
import pandas as pd
import numpy as np
import os,re
from ops import CurrencyHelper,humanize_date,timestamp_forever,timestamp_now

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Catalog:
    def __init__(self,member_id,identifier,description=None):
        self.member_id=member_id
        self.identifier=identifier
        self.description=description
    
    @staticmethod
    def attachedtostore(sid,cid):
        cursor.execute("select catalog_id=%s from storecat where storeent_id=%s and catalog_id=%s",
        (cid,sid,cid,));res=cursor.fetchone()
        if res == None:return False
        elif res != None:return True
    
    @staticmethod
    def catgroupforcatalog(catalog_id):
        cursor.execute("""select cattogrp.catgroup_id,catgroup.identifier from cattogrp left join
        catgroup on catgroup.catgroup_id=cattogrp.catgroup_id where cattogrp.catalog_id=%s""",(catalog_id,))
        res=cursor.fetchall();return [dict(zip(["value","text"],r)) for r in res]
    
    @staticmethod
    def readcatalogs(mid,lid):
        cursor.execute("""select catalog.catalog_id,catalog.identifier,catalogdsc.shortdescription from catalog
        left join catalogdsc on catalog.catalog_id=catalogdsc.catalog_id where catalog.member_id=%s and 
        catalogdsc.language_id=%s""",(mid,lid,));res=cursor.fetchall()
        return [dict(zip(["catalog_id","name","description"],r)) for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into catalog(member_id,identifier,description)values(%s,%s,%s)
            on conflict(member_id,identifier)do update set member_id=%s,identifier=%s,description=%s
            returning catalog_id""",(self.member_id,self.identifier,self.description,self.member_id,self.identifier,
            self.description,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Catalog.catgroupforcatalog(1))
class Catalogdsc:
    def __init__(self,catalog_id,language_id,name,shortdescription=None,longdescription=None,thumbnaiol=None,fullimage=None):
        self.catalog_id=catalog_id
        self.language_id=language_id
        self.name=name
        self.shortdescription=shortdescription
        self.longdescription=longdescription
        self.thumbnaiol=thumbnaiol
        self.fullimage=fullimage
    
    def save(self):
        try:
            cursor.execute("""insert into catalogdsc(catalog_id,language_id,name,shortdescription,longdescription,
            thumbnaiol,fullimage)values(%s,%s,%s,%s,%s,%s,%s)on conflict(language_id,catalog_id)do update set 
            catalog_id=%s,language_id=%s,name=%s,shortdescription=%s,longdescription=%s,thumbnaiol=%s,fullimage=%s 
            returning catalog_id""",(self.catalog_id,self.language_id,self.name,self.shortdescription,self.longdescription,
            self.thumbnaiol,self.fullimage,self.catalog_id,self.language_id,self.name,self.shortdescription,self.longdescription,
            self.thumbnaiol,self.fullimage,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Storedefcat:
    def __init__(self,storeent_id,catalog_id,field1=None,field2=None,field3=None):
        self.storeent_id=storeent_id
        self.catalog_id=catalog_id
        self.field1=field1
        self.field2=field2
        self.field3=field3
    
    def save(self):
        try:
            cursor.execute("""insert into storedefcat(storeent_id,catalog_id,field1,field2,field3)values(%s,%s,%s,%s,%s)
            returning storedefcat_id""",(self.storeent_id,self.catalog_id,self.field1,self.field2,self.field3,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Storecat:
    def __init__(self,catalog_id,storeent_id,mastercatalog=None,lastupdate=None):
        self.catalog_id=catalog_id
        self.storeent_id=storeent_id
        self.mastercatalog=mastercatalog
        self.lastupdate=lastupdate
        
    def save(self):
        try:
            cursor.execute("""insert into storecat(catalog_id,storeent_id,mastercatalog,lastupdate)values(%s,%s,%s,%s)
            on conflict(catalog_id,storeent_id)do update set catalog_id=%s,storeent_id=%s,mastercatalog=%s,
            lastupdate=%s returning catalog_id""",(self.catalog_id,self.storeent_id,self.mastercatalog,self.lastupdate,
            self.catalog_id,self.storeent_id,self.mastercatalog,self.lastupdate,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catgroup:
    def __init__(self,member_id,identifier,markfordelete=0,lastupdate=None,field1=None,field2=None,rank=None,dynamic=None):
        self.member_id=member_id
        self.identifier=identifier
        self.markfordelete=markfordelete
        self.lastupdate=lastupdate
        self.field1=field1
        self.field2=field2
        self.rank=rank
        self.dynamic=dynamic
    
    @staticmethod
    def attachedtostore(sid,cid):
        cursor.execute("select catgroup_id=%s from storecgrp where storeent_id=%s and catgroup_id=%s",
        (cid,sid,cid,));res=cursor.fetchone()
        if res == None:return False
        elif res != None:return res[0]
    
    @staticmethod
    def productcount(catgroup_id):
        if catgroup_id==None:return 0
        elif catgroup_id != None:
            cursor.execute("select count(catentry_id)from catgpenrel where catgroup_id=%s",(catgroup_id,))
            res=cursor.fetchone()
            if res == None:return 0
            elif res != None:return res[0]

    @staticmethod
    def readcatgroups(mid,lid):
        cursor.execute("""select catgroup.catgroup_id,catgroup.identifier,catgrpdesc.shortdescription from catgroup
        left join catgrpdesc on catgroup.catgroup_id=catgrpdesc.catgroup_id where catgroup.member_id=%s and 
        catgrpdesc.language_id=%s""",(mid,lid,));res=cursor.fetchall()
        if len(res) <= 0:return [dict(catgroup_id=None,identifier=None,description=None)]
        elif len(res) > 0:return [dict(catgroup_id=r[0],identifier=r[1],description=r[2],count=Catgroup.productcount(r[0]))
        for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into catgroup(member_id,identifier,markfordelete,lastupdate,field1,field2,rank,dynamic)
            values(%s,%s,%s,%s,%s,%s,%s,%s)on conflict(identifier,member_id)do update set member_id=%s,identifier=%s,
            markfordelete=%s,lastupdate=%s,field1=%s,field2=%s,rank=%s,dynamic=%s returning catgroup_id""",
            (self.member_id,self.identifier,self.markfordelete,timestamp_now(),self.field1,self.field2,self.rank,self.dynamic,
            self.member_id,self.identifier,self.markfordelete,timestamp_now(),self.field1,self.field2,self.rank,self.dynamic,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Catgroup.attachedtostore(1,4))
class Catgrpdesc:
    def __init__(self,language_id,catgroup_id,name,published,shortdescription=None,longdescription=None,thumbnail=None,
    fullimage=None,display=None,note=None):
        self.language_id=language_id
        self.catgroup_id=catgroup_id
        self.name=name
        self.published=published
        self.shortdescription=shortdescription
        self.longdescription=longdescription
        self.thumbnail=thumbnail
        self.fullimage=fullimage
        self.display=display
        self.note=note
    
    def save(self):
        try:
            cursor.execute("""insert into catgrpdesc(language_id,catgroup_id,name,shortdescription,longdescription,
            thumbnail,fullimage,published,display,note)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(catgroup_id,language_id)
            do update set language_id=%s,catgroup_id=%s,name=%s,shortdescription=%s,longdescription=%s,thumbnail=%s,fullimage=%s,
            published=%s,display=%s,note=%s returning catgroup_id""",(self.language_id,self.catgroup_id,self.name,self.shortdescription,
            self.longdescription,self.thumbnail,self.fullimage,self.published,self.display,self.note,self.language_id,self.catgroup_id,
            self.name,self.shortdescription,self.longdescription,self.thumbnail,self.fullimage,self.published,self.display,self.note,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Cattogrp:
    def __init__(self,catalog_id,catgroup_id,lastupdate=None,sequence=None,catalog_id_link=None):
        self.catalog_id=catalog_id
        self.catgroup_id=catgroup_id
        self.lastupdate=lastupdate
        self.sequence=sequence
        self.catalog_id_link=catalog_id_link
    
    def save(self):
        try:
            cursor.execute("""insert into cattogrp(catalog_id,catgroup_id,lastupdate,sequence,catalog_id_link)
            values(%s,%s,%s,%s,%s)on conflict(catalog_id,catgroup_id)do update set catalog_id=%s,catgroup_id=%s,
            lastupdate=%s,sequence=%s,catalog_id_link=%s returning catalog_id""",(self.catalog_id,self.catgroup_id,
            timestamp_now(),self.sequence,self.catalog_id_link,self.catalog_id,self.catgroup_id,timestamp_now(),
            self.sequence,self.catalog_id_link,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catgrprel:
    def __init__(self,catgroup_id_parent,catgroup_id_child,catalog_id,rule=None,sequence=0,lastupdate=None,catalog_id_link=None):
        self.catgroup_id_parent=catgroup_id_parent
        self.catgroup_id_child=catgroup_id_child
        self.catalog_id=catalog_id
        self.rule=rule
        self.sequence=sequence
        self.lastupdate=lastupdate
        self.catalog_id_link=catalog_id_link
    
    def save(self):
        try:
            cursor.execute("""insert into catgrprel(catgroup_id_parent,catgroup_id_child,catalog_id,rule,sequence,lastupdate,
            catalog_id_link)values(%s,%s,%s,%s,%s,%s,%s)on conflict(catgroup_id_child,catgroup_id_parent,catalog_id)do update set
            catgroup_id_parent=%s,catgroup_id_child=%s,catalog_id=%s,rule=%s,sequence=%s,lastupdate=%s,catalog_id_link=%s
            returning catgroup_id_parent""",(self.catgroup_id_parent,self.catgroup_id_child,self.catalog_id,self.rule,self.sequence,
            self.lastupdate,self.catalog_id_link,self.catgroup_id_parent,self.catgroup_id_child,self.catalog_id,self.rule,self.sequence,
            self.lastupdate,self.catalog_id_link,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catgpenrel:
    def __init__(self,catgroup_id,catalog_id,catentry_id,rule=None,sequence=0,lastupdate=None,field1=None,field2=None,field3=None):
        self.catgroup_id=catgroup_id
        self.catalog_id=catalog_id
        self.catentry_id=catentry_id
        self.rule=rule
        self.sequence=sequence
        self.lastupdate=lastupdate
        self.field1=field1
        self.field2=field2
        self.field3=field3
    
    def save(self):
        try:
            cursor.execute("""insert into catgpenrel(catgroup_id,catalog_id,catentry_id,rule,sequence,lastupdate,field1,field2,field3)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(catgroup_id,catentry_id,catalog_id)do update set catgroup_id=%s,
            catalog_id=%s,catentry_id=%s,rule=%s,sequence=%s,lastupdate=%s,field1=%s,field2=%s,field3=%s returning catgroup_id""",
            (self.catgroup_id,self.catalog_id,self.catentry_id,self.rule,self.sequence,self.lastupdate,self.field1,self.field2,
            self.field3,self.catgroup_id,self.catalog_id,self.catentry_id,self.rule,self.sequence,self.lastupdate,self.field1,
            self.field2,self.field3,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catgrpps:
    def __init__(self,catalog_id,catgroup_id,productset_id,usage=None):
        self.catalog_id=catalog_id
        self.catgroup_id=catgroup_id
        self.productset_id=productset_id
        self.usage=usage
    
    def save(self):
        try:
            cursor.execute("""insert into catgrpps(catalog_id,catgroup_id,productset_id,usage)values(%s,%s,%s,%s)
            on conflict(catalog_id,catgroup_id,productset_id)do update set catalog_id=%s,catgroup_id=%s,productset_id=%s,
            usage=%s returning catgroup_id""",(self.catalog_id,self.catgroup_id,self.productset_id,self.usage,
            self.catalog_id,self.catgroup_id,self.productset_id,self.usage,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Storecgrp:
    def __init__(self,storeent_id,catgroup_id):
        self.storeent_id=storeent_id
        self.catgroup_id=catgroup_id
    
    def save(self):
        try:
            cursor.execute("""insert into storecgrp(storeent_id,catgroup_id)values(%s,%s)on conflict(storeent_id,
            catgroup_id)do update set storeent_id=%s,catgroup_id=%s returning catgroup_id""",(self.storeent_id,
            self.catgroup_id,self.storeent_id,self.catgroup_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catgrptpc:
    def __init__(self,catalog_id,catgroup_id,tradeposcn_id,store_id):
        self.catalog_id=catalog_id
        self.catgroup_id=catgroup_id
        self.tradeposcn_id=tradeposcn_id
        self.store_id=store_id
    
    def save(self):
        try:
            cursor.execute("""insert into catgrptpc(catalog_id,catgroup_id,tradeposcn_id,store_id)values(%s,%s,%s,%s)
            on conflict(catalog_id,catgroup_id,tradeposcn_id,store_id)do update set catalog_id=%s,catgroup_id=%s,
            tradeposcn_id=%s,store_id=%s returning catalog_id""",(self.catalog_id,self.catgroup_id,self.tradeposcn_id,
            self.store_id,self.catalog_id,self.catgroup_id,self.tradeposcn_id,self.store_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Massoc:
    def __init__(self,massoc_id,description=None,oid=None):
        # massoc_id:identifier of the semantic specifier. for example, the semantic specifier may be "REQUIRED","NONE","TEMP"
        # or "COMES WITH". Other types of specifier can be added.
        self.massoc_id=massoc_id
        self.description=description
        self.oid=oid
    
    def save(self):
        try:
            cursor.execute("""insert into massoc(massoc_id,description,oid)values(%s,%s,%s)on conflict(massoc_id)
            do update set massoc_id=%s,description=%s,oid=%s returning massoc_id""",(self.massoc_id,self.description,
            self.oid,self.massoc_id,self.description,self.oid,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Massoccece:
    def __init__(self,massoctype_id,catentry_id_from,catentry_id_to,massoc_id,rank=None,quantity=None,rule=None,groupname=None,
    field1=None,field2=None,field3=None,oid=None,date1=None,store_id=None):
        self.massoctype_id=massoctype_id
        self.catentry_id_from=catentry_id_from
        self.catentry_id_to=catentry_id_to
        self.massoc_id=massoc_id
        self.rank=rank
        self.quantity=quantity
        self.rule=rule
        self.groupname=groupname
        self.field1=field1
        self.field2=field2
        self.field3=field3
        self.oid=oid
        self.date1=date1
        self.store_id=store_id
    
    def save(self):
        try:
            cursor.execute("""insert into massoccece(massoctype_id,catentry_id_from,catentry_id_to,massoc_id,rank,
            quantity,rule,groupname,field1,field2,field3,oid,date1,store_id)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s)on conflict(store_id,massoctype_id,massoc_id,catentry_id_from,catentry_id_to)do update set 
            massoctype_id=%s,catentry_id_from=%s,catentry_id_to=%s,massoc_id=%s,rank=%s,quantity=%s,rule=%s,groupname=%s,
            field1=%s,field2=%s,field3=%s,oid=%s,date1=%s,store_id=%s returning massoccece_id""",(self.massoctype_id,
            self.catentry_id_from,self.catentry_id_to,self.massoc_id,self.rank,self.quantity,self.rule,self.groupname,
            self.field1,self.field2,self.field3,self.oid,self.date1,self.store_id,self.massoctype_id,self.catentry_id_from,
            self.catentry_id_to,self.massoc_id,self.rank,self.quantity,self.rule,self.groupname,self.field1,self.field2,
            self.field3,self.oid,self.date1,self.store_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Massocgpgp:
    def __init__(self,catgroup_id_to,catgroup_id_from,massoctype_id,massoc_id,rank=None,quantity=None,rule=None,
    groupname=None,field1=None,field2=None,field3=None,date1=None,store_id=0):
        self.catgroup_id_to=catgroup_id_to
        self.catgroup_id_from=catgroup_id_from
        self.massoctype_id=massoctype_id
        self.massoc_id=massoc_id
        self.rank=rank
        self.quantity=quantity
        self.rule=rule
        self.groupname=groupname
        self.field1=field1
        self.field2=field2
        self.field3=field3
        self.date1=date1
        self.store_id=store_id
    
    def save(self):
        try:
            cursor.execute("""insert into massocgpgp(catgroup_id_to,catgroup_id_from,massoctype_id,rank,massoc_id,quantity,
            rule,groupname,field1,field2,field3,date1,store_id)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict
            (store_id,massoctype_id,massoc_id,catgroup_id_from,catgroup_id_to)do update set catgroup_id_to=%s,
            catgroup_id_from=%s,massoctype_id=%s,rank=%s,massoc_id=%s,quantity=%s,rule=%s,groupname=%,field1=%s,field2=%s,
            field3=%s,date1=%s,store_id=%s returning massocgpgp_id""",(self.catgroup_id_to,self.catgroup_id_from,
            self.massoctype_id,self.rank,self.massoc_id,self.quantity,self.rule,self.groupname,self.field1,self.field2,
            self.field3,self.date1,self.store_id,self.catgroup_id_to,self.catgroup_id_from,self.massoctype_id,self.rank,
            self.massoc_id,self.quantity,self.rule,self.groupname,self.field1,self.field2,self.field3,self.date1,self.store_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Massoctype:
    def __init__(self,massoctype_id,description=None,field1=None,oid=None,field2=None,field3=None):
        self.massoctype_id=massoctype_id
        self.description=description
        self.field1=field1
        self.oid=oid
        self.field2=field2
        self.field3=field3
    
    def save(self):
        try:
            cursor.execute("""insert into massoctype(massoctype_id,description,field1,oid,field2,field3)values(%s,%s,%s,%s,%s,%s)
            on conflict(massoctype_id)do update set massoctype_id=%s,description=%s,field1=%s,oid=%s,field2=%s,field3=%s
            returning massoctype_id""",(self.massoctype_id,self.description,self.field1,self.oid,self.field2,self.field3,
            self.massoctype_id,self.description,self.field1,self.oid,self.field2,self.field3,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catentry:
    def __init__(self,member_id,catenttype_id,partnumber,name,itemspc_id=None,mfpartnumber=None,mfname=None,markfordelete=0,url=None,
    field1=None,field2=None,lastupdate=None,field3=None,onspecial=None,onauction=None,field4=None,field5=None,buyable=None,
    baseitem_id=None,state=None,startdate=None,enddate=None,rank=None,availabilitydate=None,lastorderdate=None,endofservicedate=None,
    discontinuedate=None):
        self.member_id=member_id
        self.catenttype_id=catenttype_id
        self.partnumber=partnumber
        self.itemspc_id=itemspc_id
        self.mfpartnumber=mfpartnumber
        self.name=name
        self.mfname=mfname
        self.markfordelete=markfordelete
        self.url=url
        self.field1=field1
        self.field2=field2
        self.lastupdate=lastupdate
        self.field3=field3
        self.onspecial=onspecial
        self.onauction=onauction
        self.field4=field4
        self.field5=field5
        self.buyable=buyable
        self.baseitem_id=baseitem_id
        self.state=state
        self.startdate=startdate
        self.enddate=enddate
        self.rank=rank
        self.availabilitydate=availabilitydate
        self.lastorderdate=lastorderdate
        self.endofservicedate=endofservicedate
        self.discontinuedate=discontinuedate
    
    def partprebuild(self,name):
        splits=name.lower().strip().split(' ')
        return ''.join([''.join([x[0].upper(),x[-1].upper()])for x in splits])
    
    def initialpart(self):
        return '{0}-{1}-{2}'.format(self.member_id,self.catenttype_id[:2].upper(),self.partprebuild(self.name))
    
    @staticmethod
    def updatepart(catentry_id):
        cursor.execute("select partnumber from catentry where catentry_id=%s",(catentry_id,))
        existing=cursor.fetchone()[0];new='{0}-{1}'.format('-'.join(existing.split('-')[:-1]),catentry_id)
        cursor.execute("update catentry set partnumber=%s where catentry_id=%s returning partnumber",
        (new,catentry_id,));con.commit();return cursor.fetchone()[0]

    @staticmethod
    def update_itemspc(itemspc_id,catentry_id):
        try:
            cursor.execute("update catentry set itemspc_id=%s where catentry_id=%s returning catentry_id",
            (itemspc_id,catentry_id,));con.commit();return cursor.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split("\n")[0])
    
    @staticmethod
    def readcontainers(mid,lid):
        cursor.execute("""select catentry.catentry_id,catentdesc.name from catentry left join catentdesc on
        catentry.catentry_id=catentdesc.catentry_id where catentry.member_id=%s and catentdesc.language_id=%s
        and catentry.catenttype_id='Bundle'""",(mid,lid,));res=cursor.fetchall()
        if len(res) <= 0:return [dict(catentry_id=None,name=None)]
        elif len(res) > 0:return [dict(catentry_id=r[0],name=r[1]) for r in res]

    @staticmethod
    def readcatentry(mid,lid):
        cursor.execute("""select catentry.catentry_id,catentdesc.name from catentry left join catentdesc
        on catentry.catentry_id=catentdesc.catentry_id where catentry.member_id=%s and catentdesc.language_id=%s""",
        (mid,lid,));res=cursor.fetchall();return [dict(zip(["catentry_id","name"],r)) for r in res]
    
    @staticmethod
    def read(mid,lid):
        cursor.execute("""select catentry.catentry_id,catentry.member_id,catentry.itemspc_id,catentry.catenttype_id,
        catentry.partnumber,catentry.mfpartnumber,catentry.mfname,catentry.url,catentry.field1,catentry.field2,
        catentry.lastupdate,catentry.field3,catentry.onspecial,catentry.onauction,catentry.field4,catentry.field5,catentry.buyable,
        catentry.baseitem_id,catentry.state,catentry.startdate,catentry.enddate,catentry.rank,catentry.availabilitydate,
        catentry.lastorderdate,catentry.endofservicedate,catentry.discontinuedate,catentdesc.name,catentdesc.shortdesciption,
        catentdesc.longdesctiption,catentdesc.thumbnail,catentdesc.auxdescription1,catentdesc.fullimage,catentdesc.auxdescription2,
        catentdesc.avaialble,catentdesc.published,catentdesc.availabilitydate,listprice.currency,listprice.listprice::float,
        catgpenrel.catgroup_id,catgroup.identifier from catentry inner join catentdesc on catentry.catentry_id=catentdesc.catentry_id 
        inner join listprice on catentry.catentry_id=listprice.catentry_id inner join catgpenrel on catentry.catentry_id=catgpenrel.
        catentry_id inner join catgroup on catgroup.catgroup_id=catgpenrel.catgroup_id where catentry.member_id=%s and catentdesc.language_id=%s""",(mid,lid,))
        res=cursor.fetchall()
        if len(res) <= 0:return [dict()]
        elif len(res) > 0:return [dict(catentry_id=r[0],member_id=r[1],itemspc_id=r[2],catenttype_id=r[3],
        partnumber=r[4],mfpartnumber=r[5],mfname=r[6],url=r[7],field1=r[8],field2=r[9],lastupdate=humanize_date(r[10]),
        field3=r[11],onspecial=r[12],onauction=r[13],field4=r[14],field5=r[15],buyable=r[16],baseitem_id=r[17],
        state=r[18],startdate=humanize_date(r[19]),enddate=humanize_date(r[20]),rank=r[21],availabilitydate=humanize_date(r[22]),
        lastorderdate=humanize_date(r[23]),endofservicedate=humanize_date(r[24]),discontinuedate=humanize_date(r[25]),name=r[26],
        shortdescription=r[27],longdescription=r[28],thumbnail=r[29],auxdescription1=r[30],fullimage=r[31],auxdescription2=r[32],
        available=r[33],published=r[34],availabilitydate2=humanize_date(r[35]),currency=r[36],price=r[37],
        symbol=CurrencyHelper(lid).getcurrsymbol(),catgroup_id=r[38],category=r[39]) for r in res]
    
    def save(self):
        try:
            cursor.execute("""insert into catentry(member_id,itemspc_id,catenttype_id,partnumber,mfpartnumber,mfname,
            markfordelete,url,field1,field2,lastupdate,field3,onspecial,onauction,field4,field5,buyable,baseitem_id,state,
            startdate,enddate,rank,availabilitydate,lastorderdate,endofservicedate,discontinuedate)values(%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(partnumber,member_id)do update set member_id=%s,
            itemspc_id=%s,catenttype_id=%s,partnumber=%s,mfpartnumber=%s,mfname=%s,markfordelete=%s,url=%s,field1=%s,field2=%s,
            lastupdate=%s,field3=%s,onspecial=%s,onauction=%s,field4=%s,field5=%s,buyable=%s,baseitem_id=%s,state=%s,
            startdate=%s,enddate=%s,rank=%s,availabilitydate=%s,lastorderdate=%s,endofservicedate=%s,discontinuedate=%s returning
            catentry_id""",(self.member_id,self.itemspc_id,self.catenttype_id,self.partnumber,self.mfpartnumber,self.mfname,
            self.markfordelete,self.url,self.field1,self.field2,timestamp_now(),self.field3,self.onspecial,self.onauction,
            self.field4,self.field5,self.buyable,self.baseitem_id,self.state,self.startdate,self.enddate,self.rank,self.availabilitydate,
            self.lastorderdate,self.endofservicedate,self.discontinuedate,self.member_id,self.itemspc_id,self.catenttype_id,self.partnumber,
            self.mfpartnumber,self.mfname,self.markfordelete,self.url,self.field1,self.field2,timestamp_now(),self.field3,self.onspecial,
            self.onauction,self.field4,self.field5,self.buyable,self.baseitem_id,self.state,self.startdate,self.enddate,self.rank,
            self.availabilitydate,self.lastorderdate,self.endofservicedate,self.discontinuedate,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Catentry.read(1,1))
class Catentdesc:
    def __init__(self,catentry_id,language_id,published,name=None,shortdescription=None,longdescription=None,
    thumbnail=None,auxdescription1=None,fullimage=None,auxdescription2=None,available=None,availabilitydate=None):
        self.catentry_id=catentry_id
        self.language_id=language_id
        self.published=published
        self.name=name
        self.shortdescription=shortdescription
        self.longdescription=longdescription
        self.thumbnail=thumbnail
        self.auxdescription1=auxdescription1
        self.fullimage=fullimage
        self.auxdescription2=auxdescription2
        self.available=available
        self.availabilitydate=availabilitydate
    
    def save(self):
        try:
            cursor.execute("""insert into catentdesc(catentry_id,language_id,name,shortdesciption,longdesctiption,
            thumbnail,auxdescription1,fullimage,auxdescription2,avaialble,published,availabilitydate)values(%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(catentry_id,language_id)do update set catentry_id=%s,language_id=%s,name=%s,
            shortdesciption=%s,longdesctiption=%s,thumbnail=%s,auxdescription1=%s,fullimage=%s,auxdescription2=%s,avaialble=%s,
            published=%s,availabilitydate=%s returning catentry_id""",(self.catentry_id,self.language_id,self.name,
            self.shortdescription,self.longdescription,self.thumbnail,self.auxdescription1,self.fullimage,self.auxdescription2,
            self.available,self.published,self.availabilitydate,self.catentry_id,self.language_id,self.name,self.shortdescription,
            self.longdescription,self.thumbnail,self.auxdescription1,self.fullimage,self.auxdescription2,self.available,
            self.published,self.availabilitydate,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Listprice:
    def __init__(self,catentry_id,currency,listprice,oid=None):
        self.catentry_id=catentry_id
        self.currency=currency
        self.listprice=listprice
        self.oid=oid
    
    @staticmethod
    def propercode(desc):
        cursor.execute("select setccurr from setcurrdsc where description=%s",(desc,))
        return cursor.fetchone()[0]

    def save(self):
        try:
            cursor.execute("""insert into listprice(catentry_id,currency,listprice,oid)values(%s,%s,%s,%s)
            on conflict(currency,catentry_id)do update set catentry_id=%s,currency=%s,listprice=%s,oid=%s
            returning catentry_id""",(self.catentry_id,self.currency,self.listprice,self.oid,self.catentry_id,
            self.currency,self.listprice,self.oid,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catentship:
    def __init__(self,catentry_id,weight=None,weightmeasure=None,length=None,width=None,height=None,
    sizemeasure=None,nominalquantity=None,quantitymultiple=None,quantitymeasure=None):
        self.catentry_id=catentry_id
        self.weight=weight
        self.weightmeasure=weightmeasure
        self.length=length
        self.width=width
        self.height=height
        self.sizemeasure=sizemeasure
        self.nominalquantity=nominalquantity
        self.quantitymultiple=quantitymultiple
        self.quantitymeasure=quantitymeasure
    
    def save(self):
        try:
            cursor.execute("""insert into catentship(catentry_id,weight,weightmeasure,length,width,height,sizemeasure,
            nominalquantity,quantitymultiple,quantitymeasure)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(catentry_id)
            do update set catentry_id=%s,weight=%s,weightmeasure=%s,length=%s,width=%s,height=%s,sizemeasure=%s,
            nominalquantity=%s,quantitymultiple=%s,quantitymeasure=%s returning catentry_id""",(self.catentry_id,self.weight,
            self.weightmeasure,self.length,self.width,self.height,self.sizemeasure,self.nominalquantity,self.quantitymultiple,
            self.quantitymeasure,self.catentry_id,self.weight,self.weightmeasure,self.length,self.width,self.height,self.sizemeasure,
            self.nominalquantity,self.quantitymultiple,self.quantitymeasure,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catreltype:
    def __init__(self,catreltype_id,description=None,field1=None,field2=None,field3=None):
        self.catreltype_id=catreltype_id
        self.description=description
        self.field1=field1
        self.field2=field2
        self.field3=field3
    
    def save(self):
        try:
            cursor.execute("""insert into catreltype(catreltype_id,description,field1,field2,field3)values(%s,%s,%s,%s,%s)
            on conflict(catreltype_id)do update set catreltype_id=%s,description=%s,field1=%s,field2=%s,field3=%s
            returning catreltype_id""",(self.catreltype_id,self.description,self.field1,self.field2,self.field3,
            self.catreltype_id,self.description,self.field1,self.field2,self.field3,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catenttype:
    def __init__(self,catenttype_id,description=None):
        self.catenttype_id=catenttype_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into catenttype(catenttype_id,description)values(%s,%s)on conflict(catenttype_id)
            do update set catenttype_id=%s,description=%s returning catenttype_id""",(self.catenttype_id,self.description,
            self.catenttype_id,self.description,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catentattr:
    def __init__(self,language_id,catentry_id,name,value,description=None,field1=None,field2=None,field3=None):
        self.language_id=language_id
        self.catentry_id=catentry_id
        self.name=name
        self.value=value
        self.description=description
        self.field1=field1
        self.field2=field2
        self.field3=field3
    
    def save(self):
        try:
            cursor.execute("""insert into catentattr(language_id,catentry_id,name,value,description,field1,field2,field3)
            values(%s,%s,%s,%s,%s,%s,%s,%s)on conflict(catentry_id,language_id,name)do update set language_id=%s,
            catentry_id=%s,name=%s,value=%s,description=%s,field1=%s,field2=%s,field3=%s returning catentattr_id""",
            (self.language_id,self.catentry_id,self.name,self.value,self.description,self.field1,self.field2,self.field3,
            self.language_id,self.catentry_id,self.name,self.value,self.description,self.field1,self.field2,self.field3,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Storecent:
    def __init__(self,storeent_id,catentry_id):
        self.storeent_id=storeent_id
        self.catentry_id=catentry_id
    
    def save(self):
        try:
            cursor.execute("""insert into storecent(storeent_id,catentry_id)values(%s,%s)on conflict(storeent_id,catentry_id)
            do update set storeent_id=%s,catentry_id=%s returning catentry_id""",(self.storeent_id,self.catentry_id,
            self.storeent_id,self.catentry_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Baseitem:
    def __init__(self,baseitem_name,member_id,itemtype_id,partnumber,quantitymeasure='C62',lastupdate=None,
    markfordelete=0,quantitymultiple=1.0):
        self.baseitem_name=baseitem_name
        self.member_id=member_id
        self.itemtype_id=itemtype_id
        self.partnumber=partnumber
        self.quantitymeasure=quantitymeasure
        self.lastupdate=lastupdate
        self.markfordelete=markfordelete
        self.quantitymultiple=quantitymultiple
    
    def save(self):
        try:
            cursor.execute("""insert into baseitem(baseitem_name,member_id,itemtype_id,quantitymeasure,
            lastupdate,markfordelete,partnumber,quantitymultiple)values(%s,%s,%s,%s,%s,%s,%s,%s)on conflict
            (member_id,baseitem_name)do update set baseitem_name=%s,member_id=%s,itemtype_id=%s,quantitymeasure=%s,
            lastupdate=%s,markfordelete=%s,partnumber=%s,quantitymultiple=%s returning baseitem_id""",
            (self.baseitem_name,self.member_id,self.itemtype_id,self.quantitymeasure,self.lastupdate,
            self.markfordelete,self.partnumber,self.quantitymultiple,self.baseitem_name,self.member_id,
            self.itemtype_id,self.quantitymeasure,self.lastupdate,self.markfordelete,self.partnumber,
            self.quantitymultiple,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Itemspc:
    def __init__(self,member_id,partnumber,markfordelete=0,lastupdate=None,baseitem_id=None,discontinued='N'):
        self.member_id=member_id
        self.partnumber=partnumber
        self.markfordelete=markfordelete
        self.lastupdate=lastupdate
        self.baseitem_id=baseitem_id
        self.discontinued=discontinued
    
    def save(self):
        try:
            cursor.execute("""insert into itemspc(lastupdate,member_id,markfordelete,baseitem_id,discontinued,partnumber)
            values(%s,%s,%s,%s,%s,%s)on conflict(partnumber,member_id)do update set lastupdate=%s,member_id=%s,
            markfordelete=%s,baseitem_id=%s,discontinued=%s,partnumber=%s returning itemspc_id""",(timestamp_now(),
            self.member_id,self.markfordelete,self.baseitem_id,self.discontinued,self.partnumber,timestamp_now(),
            self.member_id,self.markfordelete,self.baseitem_id,self.discontinued,self.partnumber,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Attrtype:
    def __init__(self,attrtype_id,description=None,oid=None):
        self.attrtype_id=attrtype_id
        self.description=description
        self.oid=oid
    
    @staticmethod
    def read():
        cursor.execute("select attrtype_id::text,description::text from attrtype")
        res=cursor.fetchall()
        if len(res) <= 0:return [dict(text=None,value=None)]
        elif len(res) > 0:return [dict(value=x[0],text=x[1])for x in res]
    
    def save(self):
        try:
            cursor.execute("""insert into attrtype(attrtype_id,description,oid)values(%s,%s,%s)on conflict(attrtype_id)
            do update set attrtype_id=%s,description=%s,oid=%s returning attrtype_id""",(self.attrtype_id,self.description,
            self.oid,self.attrtype_id,self.description,self.oid,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
# print(Attrtype.read())
class Attrvalue:
    def __init__(self,language_id,attribute_id,attrtype_id,catentry_id,stringvalue=None,operator_id=None,sequence=0,
    integervalue=None,floatvalue=None,name=None,field1=None,image1=None,image2=None,field2=None,field3=None,
    qtyunit_id=None,attachment_id=None):
        self.language_id=language_id
        self.attribute_id=attribute_id
        self.attrtype_id=attrtype_id
        self.catentry_id=catentry_id
        self.stringvalue=stringvalue
        self.operator_id=operator_id
        self.sequence=sequence
        self.integervalue=integervalue
        self.floatvalue=floatvalue
        self.name=name
        self.field1=field1
        self.image1=image1
        self.image2=image2
        self.field2=field2
        self.field3=field3
        self.qtyunit_id=qtyunit_id
        self.attachment_id=attachment_id
    
    def save(self):
        try:
            cursor.execute("""insert into attrvalue(language_id,attribute_id,attrtype_id,stringvalue,operator_id,sequence,
            integervalue,floatvalue,catentry_id,name,field1,image1,image2,field2,field3,qtyunit_id,attachment_id)values(%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(attribute_id,catentry_id,language_id,name)do update 
            set language_id=%s,attribute_id=%s,attrtype_id=%s,stringvalue=%s,operator_id=%s,sequence=%s,integervalue=%s,
            floatvalue=%s,catentry_id=%s,name=%s,field1=%s,image1=%s,image2=%s,field2=%s,field3=%s,qtyunit_id=%s,
            attachment_id=%s returning attrvalue_id""",(self.language_id,self.attribute_id,self.attrtype_id,self.stringvalue,
            self.operator_id,self.sequence,self.integervalue,self.floatvalue,self.catentry_id,self.name,self.field1,self.image1,
            self.image2,self.field2,self.field3,self.qtyunit_id,self.attachment_id,self.language_id,self.attribute_id,self.attrtype_id,
            self.stringvalue,self.operator_id,self.sequence,self.integervalue,self.floatvalue,self.catentry_id,self.name,self.field1,
            self.image1,self.image2,self.field2,self.field3,self.qtyunit_id,self.attachment_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Attribute:
    def __init__(self,language_id,attrtype_id,sequence=0,name=None,description=None,catentry_id=None,field1=None,
    usage=None,qtyunit_id=None,groupname=None,noteinfo=None,multitype=None):
        self.language_id=language_id
        self.attrtype_id=attrtype_id
        self.sequence=sequence
        self.name=name
        self.description=description
        self.catentry_id=catentry_id
        self.field1=field1
        self.usage=usage
        self.qtyunit_id=qtyunit_id
        self.groupname=groupname
        self.noteinfo=noteinfo
        self.multitype=multitype
    
    def save(self):
        try:
            cursor.execute("""insert into attribute(language_id,attrtype_id,name,sequence,description,catentry_id,
            field1,usage,qtyunit_id,groupname,noteinfo,multitype)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            on conflict(catentry_id,language_id,name)do update set language_id=%s,attrtype_id=%s,name=%s,
            sequence=%s,description=%s,catentry_id=%s,field1=%s,usage=%s,qtyunit_id=%s,groupname=%s,noteinfo=%s,multitype=%s
            returning attribute_id""",(self.language_id,self.attrtype_id,self.name,self.sequence,self.description,
            self.catentry_id,self.field1,self.usage,self.qtyunit_id,self.groupname,self.noteinfo,self.multitype,self.language_id,
            self.attrtype_id,self.name,self.sequence,self.description,self.catentry_id,self.field1,self.usage,self.qtyunit_id,
            self.groupname,self.noteinfo,self.multitype,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catentrel:
    def __init__(self,catentry_id_parent,catreltype_id,catentry_id_child,sequence=0,quantity=None,groupname=None,
    field1=None,field2=None,field3=None,mandatory=None):
        self.catentry_id_parent=catentry_id_parent
        self.catreltype_id=catreltype_id
        self.catentry_id_child=catentry_id_child
        self.sequence=sequence
        self.quantity=quantity
        self.groupname=groupname
        self.field1=field1
        self.field2=field2
        self.field3=field3
        self.mandatory=mandatory
    
    @staticmethod
    def propername(name):
        cursor.execute("select catentry_id from catentdesc where name=%s",(name,))
        return cursor.fetchone()[0]
    
    def save(self):
        try:
            cursor.execute("""insert into catentrel(catentry_id_parent,catreltype_id,catentry_id_child,sequence,quantity,
            groupname,field1,field2,field3,mandatory)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(catreltype_id,
            catentry_id_parent,catentry_id_child)do update set catentry_id_parent=%s,catreltype_id=%s,catentry_id_child=%s,
            sequence=%s,quantity=%s,groupname=%s,field1=%s,field2=%s,field3=%s,mandatory=%s returning catentry_id_parent""",
            (self.catentry_id_parent,self.catreltype_id,self.catentry_id_child,self.sequence,self.quantity,
            self.groupname,self.field1,self.field2,self.field3,self.mandatory,self.catentry_id_parent,self.catreltype_id,
            self.catentry_id_child,self.sequence,self.quantity,self.groupname,self.field1,self.field2,self.field3,
            self.mandatory,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Pkgattr:
    def __init__(self,attribute_id,language_id,catentry_id=None,oid=None):
        self.attribute_id=attribute_id
        self.language_id=language_id
        self.catentry_id=catentry_id
        self.oid=oid
    
    def save(self):
        try:
            cursor.execute("""insert into pkgattr(attribute_id,language_id,catentry_id,oid)values(%s,%s,%s,%s)
            on conflict(catentry_id,language_id,attribute_id)do update set attribute_id=%s,language_id=%s,
            catentry_id=%s,oid=%s returning pkgattr_id""",(self.attribute_id,self.language_id,self.catentry_id,
            self.oid,self.attribute_id,self.language_id,self.catentry_id,self.oid,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Pkgattrval:
    def __init__(self,attrvalue_id,language_id,catentry_id,oid=None):
        self.attrvalue_id=attrvalue_id
        self.language_id=language_id
        self.catentry_id=catentry_id
        self.oid=oid
    
    def save(self):
        try:
            cursor.execute("""insert into pkgattrval(attrvalue_id,language_id,catentry_id,oid)values(%s,%s,%s,%s)
            on conflict(catentry_id,language_id,attrvalue_id)do update set attrvalue_id=%s,language_id=%s,catentry_id=%s,
            oid=%s returning pkgattrval_id""",(self.attrvalue_id,self.language_id,self.catentry_id,self.oid,
            self.attrvalue_id,self.language_id,self.catentry_id,self.oid,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class CatreltypeDefaults:
    def __init__(self):
        self.types=[('Product_Item','Product-Item Relationship',None,None,None),('Package_Component','Package-Component Relationship',None,None,None),
        ('Bundle_Component','Bundle-Component Relationship',None,None,None),('Dynamic_Kit_Component','Dynamic Kit-Component Relationship',None,None,None)]
    
    def isfilled(self):
        cursor.execute("select count(catreltype_id) from catreltype")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False
    
    def enter(self):[Catreltype(*reltype).save() for reltype in self.types]

class AttrtypeDefaults:
    def __init__(self):
        self.types=[('Integer','Integer',None),('String','String',None),('Float','Float',None),
        ('Datetime','Datetime',None),('BigInt','Big Integer',None)]
    
    def isfilled(self):
        cursor.execute("select count(attrtype_id)from attrtype")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False
    
    def enter(self):[Attrtype(*attrtype).save() for attrtype in self.types]

class CatenttypeDefaults:
    def __init__(self):
        self.types=[
            ('Product','A template for a group of items (or SKUs) that show the same attributes.'),
            ('Item','An item is a tangible unit of merchandise with specific and differentiating attributes.'),
            ('Package','A package is an atomic collection of catalog entries. They include items that cannot be sold separately.'),
            ('Bundle','A bundle is a collection of catalog entries to allow customers to buy multiple items at one time.\
                They comprise SKUs that are usually resolved separately during sales.')]
    
    @staticmethod
    def enter(catenttype_id,description):
        try:
            cursor.execute("""insert into catenttype(catenttype_id,description)values(%s,%s)on conflict(catenttype_id)
            do update set catenttype_id=%s,description=%s returning catenttype_id""",(catenttype_id,description,catenttype_id,
            description,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

    def isfilled(self):
        cursor.execute("select count(catenttype_id)from catenttype")
        res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False
    
    def save(self):[self.enter(*i) for i in self.types]

class Attrdict:
    def __init__(self,storeent_id,field1=None,field2=None,field3=None):
        self.storeent_id=storeent_id
        self.field1=field1
        self.field2=field2
        self.field3=field3
    
    def save(self):
        try:
            cursor.execute("""insert into attrdict(storeent_id,field1,field2,field3)values(%s,%s,%s,%s)
            returning attrdict_id""",(self.storeent_id,self.field1,self.field2,self.field3,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Attr:
    def __init__(self,identifier,attrtype_id,storeent_id=None,attrdict_id=None,sequence=0,displayable=None,
    searchable=None,comparable=None,field1=None,field2=None,field3=None,attrusage=None,storedisplay=None,
    facetable=0,merchandisable=None,swatchable=0):
        self.identifier=identifier
        self.attrtype_id=attrtype_id
        self.storeent_id=storeent_id
        self.attrdict_id=attrdict_id
        self.sequence=sequence
        self.displayable=displayable
        self.searchable=searchable
        self.comparable=comparable
        self.field1=field1
        self.field2=field2
        self.field3=field3
        self.attrusage=attrusage
        self.storedisplay=storedisplay
        self.facetable=facetable
        self.merchandisable=merchandisable
        self.swatchable=swatchable
    
    @staticmethod
    def read(lid):
        cursor.execute("""select attr.attr_id,attr.identifier,attr.attrtype_id,attrdesc.name,
        attrdesc.description from attr inner join attrdesc on attr.attr_id=attrdesc.attr_id 
        where attrdesc.language_id=%s""",(lid,));res=cursor.fetchall()
        if len(res) <= 0:return [dict(attr_id=None,identifier=None,attrtype_id=None,attriute_type=None,
        name=None,description=None)]
        elif len(res) > 0:return [dict(attr_id=r[0],identifier=r[1],attrtype_id=r[2],attribute_type=r[2],
        name=r[3],description=r[4]) for r in res]

    def save(self):
        try:
            cursor.execute("""insert into attr(identifier,attrtype_id,attrdict_id,storeent_id,sequence,
            displayable,searchable,comparable,field1,field2,field3,attrusage,storedisplay,facetable,
            merchandisable,swatchable)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict
            (identifier)do update set identifier=%s,attrtype_id=%s,attrdict_id=%s,storeent_id=%s,
            sequence=%s,displayable=%s,searchable=%s,comparable=%s,field1=%s,field2=%s,field3=%s,attrusage=%s,
            storedisplay=%s,facetable=%s,merchandisable=%s,swatchable=%s returning attr_id""",
            (self.identifier,self.attrtype_id,self.attrdict_id,self.storeent_id,self.sequence,self.displayable,
            self.searchable,self.comparable,self.field1,self.field2,self.field3,self.attrusage,self.storedisplay,
            self.facetable,self.merchandisable,self.swatchable,
            self.identifier,self.attrtype_id,self.attrdict_id,self.storeent_id,self.sequence,self.displayable,
            self.searchable,self.comparable,self.field1,self.field2,self.field3,self.attrusage,self.storedisplay,
            self.facetable,self.merchandisable,self.swatchable,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Attrdesc:
    def __init__(self,attr_id,language_id,attrtype_id,name=None,description=None,description2=None,
    field1=None,groupname=None,qtyunit_id=None,noteinfo=None):
        self.attr_id=attr_id
        self.language_id=language_id
        self.attrtype_id=attrtype_id
        self.name=name
        self.description=description
        self.description2=description2
        self.field1=field1
        self.groupname=groupname
        self.qtyunit_id=qtyunit_id
        self.noteinfo=noteinfo
    
    def save(self):
        try:
            cursor.execute("""insert into attrdesc(attr_id,language_id,attrtype_id,name,description,description2,
            field1,groupname,qtyunit_id,noteinfo)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(attr_id,
            language_id)do update set attr_id=%s,language_id=%s,attrtype_id=%s,name=%s,description=%s,
            description2=%s,field1=%s,groupname=%s,qtyunit_id=%s,noteinfo=%s returning attr_id""",
            (self.attr_id,self.language_id,self.attrtype_id,self.name,self.description,self.description2,
            self.field1,self.groupname,self.qtyunit_id,self.noteinfo,
            self.attr_id,self.language_id,self.attrtype_id,self.name,self.description,self.description2,
            self.field1,self.groupname,self.qtyunit_id,self.noteinfo,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Attrval:
    def __init__(self,attr_id,identifier=None,valusage=None,storeent_id=None,field1=None,field2=None,field3=None):
        self.atttr_id=attr_id
        self.identifier=identifier
        self.valusage=valusage
        self.storeent_id=storeent_id
        self.field1=field1
        self.field2=field2
        self.field3=field3
    
    def save(self):
        try:
            cursor.execute("""insert into attrval(attr_id,identifier,valusage,storeent_id,field1,field2,field3)
            values(%s,%s,%s,%s,%s,%s,%s)on conflict(attr_id,identifier)do update set attr_id=%s,identifier=%s,
            valusage=%s,storeent_id=%s,field1=%s,field2=%s,field3=%s returning attrval_id""",
            (self.atttr_id,self.identifier,self.valusage,self.storeent_id,self.field1,self.field2,self.field3,
            self.atttr_id,self.identifier,self.valusage,self.storeent_id,self.field1,self.field2,self.field3,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Attrvaldesc:
    def __init__(self,attrval_id,language_id,attr_id,value=None,valusage=None,sequence=None,
    stringvalue=None,integervalue=None,floatvalue=None,datetimevalue=None,qtyunit_id=None,image1=None,
    image2=None,field1=None,field2=None,field3=None):
        self.attrval_id=attrval_id
        self.language_id=language_id
        self.attr_id=attr_id
        self.value=value
        self.valusage=valusage
        self.sequence=sequence
        self.stringvalue=stringvalue
        self.integervalue=integervalue
        self.floatvalue=floatvalue
        self.datetimevalue=datetimevalue
        self.qtyunit_id=qtyunit_id
        self.image1=image1
        self.image2=image2
        self.field1=field1
        self.field2=field2
        self.field3=field3
    
    def save(self):
        try:
            cursor.execute("""insert into attrvaldesc(attrval_id,language_id,attr_id,value,valusage,
            sequence,stringvalue,integervalue,floatvalue,qtyunit_id,image1,image2,field1,field2,field3,datetimevalue)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(attrval_id,language_id)do update
            set attrval_id=%s,language_id=%s,attr_id=%s,value=%s,valusage=%s,sequence=%s,stringvalue=%s,integervalue=%s,
            floatvalue=%s,qtyunit_id=%s,image1=%s,image2=%s,field1=%s,field2=%s,field3=%s,datetimevalue=%s returning attrval_id""",
            (self.attrval_id,self.language_id,self.attr_id,self.value,self.valusage,self.sequence,self.stringvalue,
            self.integervalue,self.floatvalue,self.qtyunit_id,self.image1,self.image2,self.field1,self.field2,
            self.field3,self.datetimevalue,self.attrval_id,self.language_id,self.attr_id,self.value,self.valusage,self.sequence,self.stringvalue,
            self.integervalue,self.floatvalue,self.qtyunit_id,self.image1,self.image2,self.field1,self.field2,
            self.field3,self.datetimevalue,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Catentryattr:
    def __init__(self,catentry_id,attr_id,attrval_id,usage,sequence=None,field1=None,field2=None,field3=None):
        self.catentry_id=catentry_id
        self.attr_id=attr_id
        self.attrval_id=attrval_id
        self.usage=usage
        self.sequence=sequence
        self.field1=field1
        self.field2=field2
        self.field3=field3
        
    def save(self):
        try:
            cursor.execute("""insert into catentryattr(catentry_id,attr_id,attrval_id,usage,sequence,
            field1,field2,field3)values(%s,%s,%s,%s,%s,%s,%s,%s)on conflict(catentry_id,attr_id,attrval_id)
            do update set catentry_id=%s,attr_id=%s,attrval_id=%s,usage=%s,sequence=%s,field1=%s,
            field2=%s,field3=%s returning attr_id""",(self.catentry_id,self.attr_id,self.attrval_id,
            self.usage,self.sequence,self.field1,self.field2,self.field3,self.catentry_id,self.attr_id,
            self.attrval_id,self.usage,self.sequence,self.field1,self.field2,self.field3,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

# print(Catentryattr.read(1))