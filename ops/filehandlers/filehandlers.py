import pandas as pd
import numpy as np
import os
# from .db_con import createcon
# from db_con import createcon
import psycopg2
# con,cursor=createcon('retail','jmso','localhost','5432')
from ops.connector.connector import evcon
con,cursor=evcon()

from ops.catalog.catalog import Catalog,Catalogdsc,Catgroup,Catgrpdesc,Cattogrp,Catentry,Itemspc,Catentdesc,Catgpenrel,Listprice,EntryException
from ops.helpers.functions import timestamp_forever,timestamp_now,datetimestamp_now
import time


class InstallCatalogs:
    def __init__(self,fname,member_id):
        self.fname=fname
        self.member_id=member_id

    def defaultlang(self):
        cursor.execute("""select language_id from languageds where description='English (Nigeria)'""")
        return cursor.fetchone()[0]
    
    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            df['language_id']=pd.Series([self.defaultlang()]*df.shape[0])
            df['member_id']=pd.Series([self.member_id]*df.shape[0])
            catalogs=df.values
            # name,desc,lang,member
            catalogids=[Catalog(catalogs[i][3],catalogs[i][0],catalogs[i][1]).save() for i in range(len(catalogs))]
            [Catalogdsc(catalogids[i],catalogs[i][2],catalogs[i][0],shortdescription=catalogs[i][1]).save()
            for i in range(len(catalogs))]


class InstallCatgroups:
    def __init__(self,fname,member_id):
        self.fname=fname
        self.member_id=member_id

    def defaultlang(self):
        cursor.execute("""select language_id from languageds where description='English (Nigeria)'""")
        return cursor.fetchone()[0]
    
    def getcatalogid(self,name):
        cursor.execute("select catalog_id from catalog where identifier=%s",(name,))
        res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            df['language_id']=pd.Series([self.defaultlang()]*df.shape[0])
            df['member_id']=pd.Series([self.member_id]*df.shape[0])
            catgroups=df.values
            # name,catalog,language,member
            categoryids=[Catgroup(catgroups[i][3],catgroups[i][0]).save() for i in range(len(catgroups))]
            [Catgrpdesc(catgroups[i][2],categoryids[i],catgroups[i][0],1,shortdescription=catgroups[i][0]).save() 
            for i in range(len(catgroups))]
            [Cattogrp(self.getcatalogid(catgroups[i][1]),categoryids[i],datetimestamp_now(),).save() 
            for i in range(len(categoryids)) ]

class InstallCatentries:
    def __init__(self,fname,member_id,catenttype_id='Item',currency='NGN',published=1):
        self.fname=fname
        self.member_id=member_id
        self.catenttype_id=catenttype_id
        self.currency=currency
        self.published=published

    def defaultlang(self):
        cursor.execute("""select language_id from languageds where description='English (Nigeria)'""")
        return cursor.fetchone()[0]
    
    def getcatalogid(self,name,member_id):
        cursor.execute("select catalog_id from catalog where identifier=%s and member_id=%s",(name,member_id,))
        res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def getcatgroupid(self,name,member_id):
        cursor.execute("select catgroup_id from catgroup where identifier=%s and member_id=%s",(name,member_id,))
        res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
    
    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            df['language_id']=pd.Series([self.defaultlang()]*df.shape[0])
            df['member_id']=pd.Series([self.member_id]*df.shape[0])
            df['catenttype_id']=pd.Series([self.catenttype_id]*df.shape[0])
            df['currency']=pd.Series([self.currency]*df.shape[0])
            df['published']=pd.Series([self.published]*df.shape[0])
            # df.dropna(subset=['Price'],inplace=True)
            df['Price'].fillna(0,inplace=True)
            # product,price,catalog,category,language_id,member_id,catenttype_id,currency,published
            catentries=df.values
            for entry in catentries:
                try:
                    c=Catentry(entry[5],entry[6],None,entry[0],itemspc_id=None,lastupdate=datetimestamp_now())
                    nameexists=c.name_exists(entry[0],entry[5])
                    if nameexists:print( {"msg":"A product with that name already exists."} );continue
                    elif nameexists==False:
                        oldpart=c.initialpart()
                        c.partnumber=oldpart
                        catentry_id=c.save()
                        newpart=c.updatepart(catentry_id,oldpart)

                        print(oldpart,newpart)
                        if oldpart==newpart:
                            print("item seen before")
                            print("member_id {}, catentry_id {}".format(entry[5],catentry_id))
                            break

                        itemspc_id=Itemspc(entry[5],newpart,baseitem_id=catentry_id,lastupdate=datetimestamp_now()).save()
                        c.update_itemspc(itemspc_id,catentry_id)
                        Catentdesc(catentry_id,entry[4],entry[8],name=entry[0],shortdescription=entry[0]).save()
                        catgroup_id=Catgpenrel(self.getcatgroupid(entry[3],entry[5]),self.getcatalogid(entry[2],entry[5]),catentry_id).save()
                        print(catgroup_id)
                        Listprice(catentry_id,entry[7],entry[1]).save()
                        time.sleep(3)
                except EntryException as e:
                    print( {"msg":"Error {}".format(e.message)} )
                    print(entry)
                    # con.rollback()
                    continue
