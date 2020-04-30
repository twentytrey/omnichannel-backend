from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","jmso","localhost","5432")
import  importlib
import pandas as pd
import numpy as np

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Distarrang:
    def __init__(self,merchantstore_id,baseitem_id,startdate,enddate,wholesalestore_id,lastupdate=None,pickingmethod=None,
    field1=None,field2=None,field3=None,):
        self.merchantstore_id=merchantstore_id
        self.baseitem_id=baseitem_id
        self.startdate=startdate
        self.enddate=enddate
        self.wholesalestore_id=wholesalestore_id
        self.lastupdate=lastupdate
        self.pickingmethod=pickingmethod
        self.field1=field1
        self.field2=field2
        self.field3=field3
    
    def save(self):
        try:
            cursor.execute("""insert into distarrang(merchantstore_id,pickingmethod,startdate,enddate,
            field1,field2,field3,wholesalestore_id,baseitem_id,lastupdate)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            on conflict(baseitem_id,merchantstore_id,wholesalestore_id,startdate,enddate)do update set 
            merchantstore_id=%s,pickingmethod=%s,startdate=%s,enddate=%s,field1=%s,field2=%s,field3=%s,
            wholesalestore_id=%s,baseitem_id=%s,lastupdate=%s returning distarrang_id""",
            (self.merchantstore_id,self.pickingmethod,self.startdate,self.enddate,self.field1,self.field2,
            self.field3,self.wholesalestore_id,self.baseitem_id,self.lastupdate,
            self.merchantstore_id,self.pickingmethod,self.startdate,self.enddate,self.field1,self.field2,
            self.field3,self.wholesalestore_id,self.baseitem_id,self.lastupdate,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError)as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Storeinv:
    def __init__(self,store_id,catentry_id,storequantity=None,quantitymeasure=None,c5=None):
        self.store_id=store_id
        self.catentry_id=catentry_id
        self.storequantity=storequantity
        self.quantitymeasure=quantitymeasure
        self.c5=c5
    
    def save(self):
        try:
            cursor.execute("""insert into storeinv(store_id,catentry_id,storequantity,quantitymeasure
            c5)values(%s,%s,%s,%s,%s)returning store_id""",(self.store_id,self.catentry_id,self.storequantity,
            self.quantitymeasure,self.c5,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Storeitem:
    def __init__(self,baseitem_id,storeent_id,trackinginventory='Y',forcebackorder='N',
    releaseseparately='N',foreignsku=None,foreignsystem=None,lastupdate=None,creditable='Y',
    backorderable='Y',returnnotdesired='N',minqtyforsplit=0):
        self.baseitem_id=baseitem_id
        self.storeent_id=storeent_id
        self.trackinginventory=trackinginventory
        self.forcebackorder=forcebackorder
        self.releaseseparately=releaseseparately
        self.foreignsku=foreignsku
        self.foreignsystem=foreignsystem
        self.lastupdate=lastupdate
        self.creditable=creditable
        self.backorderable=backorderable
        self.returnnotdesired=returnnotdesired
        self.minqtyforsplit=minqtyforsplit
    
    def save(self):
        try:
            cursor.execute("""insert into storeitem(baseitem_id,storeent_id,trackinginventory,
            forcebackorder,releaseseparately,foreignsku,foreignsystem,lastupdate,creditable,backorderable,
            returnnotdesired,minqtyforsplit)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict
            (baseitem_id,storeent_id)do update set baseitem_id=%s,storeent_id=%s,trackinginventory=%s,
            forcebackorder=%s,releaseseparately=%s,foreignsku=%s,foreignsystem=%s,lastupdate=%s,creditable=%s,
            backorderable=%s,returnnotdesired=%s,minqtyforsplit=%s returning baseitem_id""",
            (self.baseitem_id,self.storeent_id,self.trackinginventory,self.forcebackorder,self.releaseseparately,
            self.foreignsku,self.foreignsystem,self.lastupdate,self.creditable,self.backorderable,
            self.returnnotdesired,self.minqtyforsplit,
            self.baseitem_id,self.storeent_id,self.trackinginventory,self.forcebackorder,self.releaseseparately,
            self.foreignsku,self.foreignsystem,self.lastupdate,self.creditable,self.backorderable,
            self.returnnotdesired,self.minqtyforsplit,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rcptavail:
    def __init__(self,distarrang_id,receipt_id,precedence=None,lastupdate=None):
        self.distarrang_id=distarrang_id
        self.receipt_id=receipt_id
        self.precedence=precedence
        self.lastupdate=lastupdate
    
    def save(self):
        try:
            cursor.execute("""insert into rcptavail(distarrang_id,receipt_id,precedence,lastupdate)
            values(%s,%s,%s,%s,)on conflict(distarrang_id,receipt_id)do update set distarrang_id=%s,
            receipt_id=%s,precedence=%s,lastupdate=%s returning rcptavail_id""",(self.distarrang_id,
            self.receipt_id,self.precedence,self.lastupdate,self.distarrang_id,self.receipt_id,
            self.precedence,self.lastupdate,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Receipt:
    def __init__(self,versionspc_id,store_id,ffmcenter_id,receiptdate,createtime,cost=0,comment1=None,
    comment2=None,lastupdate=None,receipttype='ADHC',qtyreceived=0,qtyinprocess=0,qtyonhand=0,qtyinkits=0,
    vendor_id=None,setccurr=None,radetail_id=None,rtnrcptdsp_id=None):
        self.versionspc_id=versionspc_id
        self.store_id=store_id
        self.ffmcenter_id=ffmcenter_id
        self.receiptdate=receiptdate
        self.createtime=createtime
        self.cost=cost
        self.comment1=comment1
        self.comment2=comment2
        self.lastupdate=lastupdate
        self.receipttype=receipttype
        self.qtyreceived=qtyreceived
        self.qtyinprocess=qtyinprocess
        self.qtyonhand=qtyonhand
        self.qtyinkits=qtyinkits
        self.vendor_id=vendor_id
        self.setccurr=setccurr
        self.radetail_id=radetail_id
        self.rtnrcptdsp_id=rtnrcptdsp_id
    
    def save(self):
        try:
            cursor.execute("""insert into receipt(versionspc_id,radetail_id,store_id,setccurr,ffmcenter_id,vendor_id,
            receiptdate,qtyreceived,qtyinprocess,qtyonhand,qtyinkits,cost,comment1,comment2,lastupdate,createtime,
            receipttype,rtnrcptdsp_id)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on conflict
            (versionspc_id,ffmcenter_id,store_id,createtime)do update set versionspc_id=%s,radetail_id=%s,store_id=%s,
            setccurr=%s,ffmcenter_id=%s,vendor_id=%s,receiptdate=%s,qtyreceived=%s,qtyinprocess=%s,qtyonhand=%s,
            qtyinkits=%s,cost=%s,comment1=%s,comment2=%s,lastupdate=%s,createtime=%s,receipttype=%s,rtnrcptdsp_id=%s
            returning receipt_id""",(self.versionspc_id,self.radetail_id,self.store_id,self.setccurr,self.ffmcenter_id,
            self.vendor_id,self.receiptdate,self.qtyreceived,self.qtyinprocess,self.qtyonhand,self.qtyinkits,self.cost,
            self.comment1,self.comment2,self.lastupdate,self.createtime,self.receipttype,self.rtnrcptdsp_id,
            self.versionspc_id,self.radetail_id,self.store_id,self.setccurr,self.ffmcenter_id,
            self.vendor_id,self.receiptdate,self.qtyreceived,self.qtyinprocess,self.qtyonhand,self.qtyinkits,self.cost,
            self.comment1,self.comment2,self.lastupdate,self.createtime,self.receipttype,self.rtnrcptdsp_id,))
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rtnrcptdsp:
    def __init__(self,rtndspcode_id,rtnreceipt_id,rtnrcptdsp_id,quantity,dispositiondate,rtnreason_id=None,comments=None):
        self.rtndspcode_id=rtndspcode_id
        self.rtnreceipt_id=rtnreceipt_id
        self.rtnrcptdsp_id=rtnrcptdsp_id
        self.rtnreason_id=rtnreason_id
        self.quantity=quantity
        self.dispositiondate=dispositiondate
        self.comments=comments
    
    def save(self):
        try:
            cursor.execute("""insert into rtnrcptdsp(rtndspcode_id,rtnreceipt_id,rtnrcptdsp_id,rtnreason_id,
            quantity,dispositiondate,comments)values(%s,%s,%s,%s,%s,%s,%s)returning rtnrcptdsp_id""",
            (self.rtndspcode_id,self.rtnreceipt_id,self.rtnrcptdsp_id,self.rtnreason_id,self.quantity,
            self.dispositiondate,self.comments,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Itemffmctr:
    def __init__(self,itemspc_id,store_id,ffmcenter_id,qtybackordered=0,qtyallocbackorder=0,
    lastupdate=None,qtyreserved=0,restocktime=None):
        self.itemspc_id=itemspc_id
        self.store_id=store_id
        self.ffmcenter_id=ffmcenter_id
        self.qtybackordered=qtybackordered
        self.qtyallocbackorder=qtyallocbackorder
        self.lastupdate=lastupdate
        self.qtyreserved=qtyreserved
        self.restocktime=restocktime
    
    def save(self):
        try:
            cursor.execute("""insert into itemffmctr(itemspc_id,store_id,ffmcenter_id,qtybackordered,
            qtyallocbackorder,lastupdate,qtyreserved,restocktime)values(%s,%s,%s,%s,%s,%s,%s,%s)on
            conflict(itemspc_id,store_id,ffmcenter_id)do update set itemspc_id=%s,store_id=%s,ffmcenter_id=%s,
            qtybackordered=%s,qtyallocbackorder=%s,lastupdate=%s,qtyreserved=%s,restocktime=%s returning ffmcenter_id""",
            (self.itemspc_id,self.store_id,self.ffmcenter_id,self.qtybackordered,self.qtyallocbackorder,self.lastupdate,
            self.qtyreserved,self.restocktime,
            self.itemspc_id,self.store_id,self.ffmcenter_id,self.qtybackordered,self.qtyallocbackorder,self.lastupdate,
            self.qtyreserved,self.restocktime,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Invreserve:
    def __init__(self,invrsrvtyp_id,quantity=None,description=None,expiration=None,itemspc_id=None,
    lastupdate=None,store_id=None,ffmcenter_id=None):
        self.invrsrvtyp_id=invrsrvtyp_id
        self.quantity=quantity
        self.description=description
        self.expiration=expiration
        self.itemspc_id=itemspc_id
        self.lastupdate=lastupdate
        self.store_id=store_id
        self.ffmcenter_id=ffmcenter_id
    
    def save(self):
        try:
            cursor.execute("""insert into invreserve(invrsrvtyp_id,quantity,description,expiration,itemspc_id,
            lastupdate,store_id,ffmcenter_id)values(%s,%s,%s,%s,%s,%s,%s,%s)returning invreserve_id""",
            (self.invrsrvtyp_id,self.quantity,self.description,self.expiration,self.itemspc_id,self.lastupdate,
            self.store_id,self.ffmcenter_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Invrsrvtyp:
    def __init__(self):
        self.lastid=self.getlastid()
    
    def getlastid(self):
        cursor.execute("select invrsrvtyp_id from invrsrvtyp")
        res=cursor.fetchone()
        if res==None:return 1
        elif res != None:return res[0]+1
    
    def save(self):
        try:
            cursor.execute("""insert into invrsrvtyp(invrsrvtyp_id)values(%s)returning invrsrvtyp_id""",
            (self.lastid,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Invrsrvdsc:
    def __init__(self,invrsrvtyp_id,language_id,name=None,description=None):
        self.invrsrvtyp_id=invrsrvtyp_id
        self.language_id=language_id
        self.name=name
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into invrsrvdsc(invrsrvtyp_id,language_id,name,description)
            values(%s,%s,%s,%s)on conflict(invrsrvtyp_id,language_id)do update set invrsrvtyp_id=%s,
            language_id=%s,name=%s,description=%s returning invrsrvtyp_id""",(self.invrsrvtyp_id,
            self.language_id,self.name,self.description,self.invrsrvtyp_id,self.language_id,self.name,
            self.description,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Invitmvw:
    def __init__(self,itemspc_id,receiptquantity,qtyavailable):
        self.itemspc_id=itemspc_id
        self.receiptquantity=receiptquantity
        self.qtyavailable=qtyavailable
    
    def save(self):
        try:
            cursor.execute("""insert into invitmvw(itemspc_id,receiptquantity,qtyavailable)
            values(%s,%s,%s)returning itemspc_id""",(self.itemspc_id,self.receiptquantity,self.qtyavailable,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rcptitmvw:
    def __init__(self,itemspc_id,receiptquantity):
        self.itemspc_id=itemspc_id
        self.receiptquantity=receiptquantity
    
    def save(self):
        try:
            cursor.execute("""insert into rcptitmvw(itemspc_id,receiptquantity)
            values(%s,%s)returning itemspc_id""",(self.itemspc_id,self.receiptquantity,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Invstffmvw:
    def __init__(self,store_id,ffmcenter_id,itemspc_id,qtyavailable):
        self.store_id=store_id
        self.ffmcenter_id=ffmcenter_id
        self.itemspc_id=itemspc_id
        self.qtyavailable=qtyavailable
    
    def save(self):
        try:
            cursor.execute("""insert into invstffmvw(store_id,ffmcenter_id,itemspc_id,qtyavailable)
            values(%s,%s,%s,%s)returning itemspc_id""",(self.store_id,self.ffmcenter_id,self.itemspc_id,
            self.qtyavailable,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rcptstffvw:
    def __init__(self,itemspc_id,store_id,ffmcenter_id,receiptquantity):
        self.itemspc_id=itemspc_id
        self.store_id=store_id
        self.ffmcenter_id=ffmcenter_id
        self.receiptquantity=receiptquantity
    
    def save(self):
        try:
            cursor.execute("""insert into rcptstffvw(itemspc_id,store_id,ffmcenter_id,receiptquantity)
            values(%s,%s,%s,%s)returning itemspc_id""",(self.itemspc_id,self.store_id,self.ffmcenter_id,
            self.receiptquantity,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Invstvw:
    def __init__(self,store_id,itemspc_id,qtyavailable=None,quantitymeasure=None):
        self.store_id=store_id
        self.itemspc_id=itemspc_id
        self.qtyavailable=qtyavailable
        self.quantitymeasure=quantitymeasure

    def save(self):
        try:
            cursor.execute("""insert into invstvw(store_id,itemspc_id,qtyavailable,quantitymeasure)
            values(%s,%s,%s,%s)returning itemspc""",(self.store_id,self.itemspc_id,self.qtyavailable,
            self.quantitymeasure,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rcptstvw:
    def __init__(self,itemspc_id,store_id,receiptquantity):
        self.itemspc_id=itemspc_id
        self.store_id=store_id
        self.receiptquantity=receiptquantity
    
    def save(self):
        try:
            cursor.execute("""insert into rcptstvw(itemspc_id,store_id,receiptquantity)values(%s,%s,%s)
            returning itemspc_id""",(self.itemspc_id,self.store_id,self.receiptquantity,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Invadjust:
    def __init__(self,invadjustnum,invadjcode_id,receipt_id,adjustmentdate=None,quantity=None,
    adjustmentcomment=None,lastupdate=None):
        self.invadjustnum=invadjustnum
        self.invadjcode_id=invadjcode_id
        self.receipt_id=receipt_id
        self.adjustmentdate=adjustmentdate
        self.quantity=quantity
        self.adjustmentcomment=adjustmentcomment
        self.lastupdate=lastupdate
    
    def save(self):
        try:
            cursor.execute("""insert into invadjust(invadjustnum,invadjcode_id,receipt_id,adjustmentdate,quantity,
            adjustmentcomment,lastupdate)values(%s,%s,%s,%s,%s,%s,%s)returning invadjust_id""",(self.invadjustnum,
            self.invadjcode_id,self.receipt_id,self.adjustmentdate,self.quantity,self.adjustmentcomment,self.lastupdate,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Invadjcode:
    def __init__(self,adjustcode,storeent_id,markfordelete=0,lastupdate=None):
        self.adjustcode=adjustcode
        self.storeent_id=storeent_id
        self.markfordelete=markfordelete
        self.lastupdate=lastupdate
    
    def save(self):
        try:
            cursor.execute("""insert into invadjcode(adjustcode,lastupdate,storeent_id,markfordelete)
            values(%s,%s,%s,%s)on conflict(adjustcode,storeent_id)do update set adjustcode=%s,lastupdate=%s,
            storeent_id=%s,markfordelete=%s returning invadjcode_id""",(self.adjustcode,self.lastupdate,
            self.storeent_id,self.markfordelete,self.adjustcode,self.lastupdate,self.storeent_id,self.markfordelete,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Invadjdesc:
    def __init__(self,invadjcode_id,language_id,lastupdate=None,description=None,):
        self.invadjcode_id=invadjcode_id
        self.language_id=language_id
        self.lastupdate=lastupdate
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into invadjdesc(invadjcode_id,description,language_id,
            lastupdate)values(%s,%s,%s,%s)on conflict(invadjcode,language_id)do update set invadjcode_id=%s,
            description=%s,language_id=%s,lastupdate=%s returning invadjcode_id""",(self.invadjcode_id,
            self.description,self.language_id,self.lastupdate,self.invadjcode_id,self.description,
            self.language_id,self.lastupdate,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ra:
    def __init__(self,vendor_id,store_id,orderdate,createtime,openindicator=None,dateclosed=None,
    lastupdate=None,externalid=None,markfordelete=0):
        self.vendor_id=vendor_id
        self.store_id=store_id
        self.orderdate=orderdate
        self.createtime=createtime
        self.openindicator=openindicator
        self.dateclosed=dateclosed
        self.lastupdate=lastupdate
        self.externalid=externalid
        self.markfordelete=markfordelete
    
    def save(self):
        try:
            cursor.execute("""insert into ra(vendor_id,store_id,orderdate,openindicator,dateclosed,
            lastupdate,externalid,markfordelete,createtime)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            on conflict(store_id,vendor_id,createtime)do update set vendor_id=%s,store_id=%s,
            orderdate=%s,openindicator=%s,dateclosed=%s,lastupdate=%s,externalid=%s,markfordelete=%s,
            createtime=%s returning ra_id""",(self.vendor_id,self.store_id,self.orderdate,self.openindicator,
            self.dateclosed,self.lastupdate,self.externalid,self.markfordelete,self.createtime,
            self.vendor_id,self.store_id,self.orderdate,self.openindicator,
            self.dateclosed,self.lastupdate,self.externalid,self.markfordelete,self.createtime,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Radetail:
    def __init__(self,ra_id,itemspc_id,expecteddate,ffmcenter_id=None,qtyordered=0,qtyreceived=0,
    qtyremaining=0,qtyallocated=0,radetailcomment=None,lastupdate=None,markfordelete=0):
        self.ra_id=ra_id
        self.itemspc_id=itemspc_id
        self.expecteddate=expecteddate
        self.ffmcenter_id=ffmcenter_id
        self.qtyordered=qtyordered
        self.qtyreceived=qtyreceived
        self.qtyremaining=qtyremaining
        self.qtyallocated=qtyallocated
        self.radetailcomment=radetailcomment
        self.lastupdate=lastupdate
        self.markfordelete=markfordelete
    
    def save(self):
        try:
            cursor.execute("""insert into radetail(ra_id,ffmcenter_id,itemspc_id,qtyordered,qtyreceived,
            qtyremaining,qtyallocated,expecteddate,radetailcomment,lastupdate,markfordelete)values
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)returning radetail_id""",(self.ra_id,self.ffmcenter_id,
            self.itemspc_id,self.qtyordered,self.qtyreceived,self.qtyremaining,self.qtyallocated,
            self.expecteddate,self.radetailcomment,self.lastupdate,self.markfordelete,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rabackallo:
    def __init__(self,rabackallonum,radetail_id,itemspc_id,orderitems_id,qtyallocated=None,lastupdate=None):
        self.rabackallonum=rabackallonum
        self.radetail_id=radetail_id
        self.itemspc_id=itemspc_id
        self.orderitems_id=orderitems_id
        self.qtyallocated=qtyallocated
        self.lastupdate=lastupdate
    
    def save(self):
        try:
            cursor.execute("""insert into rabackallo(rabackallonum,radetail_id,itemspc_id,orderitems_id,
            qtyallocated,lastupdate)values(%s,%s,%s,%s,%s,%s)on conflict(orderitems_id,rabackallonum)do
            update set rabackallonum=%s,radetail_id=%s,itemspc_id=%s,orderitems_id=%s,qtyallocated=%s,
            lastupdate=%s returning radetail_id""",(self.rabackallonum,self.radetail_id,self.itemspc_id,
            self.orderitems_id,self.qtyallocated,self.lastupdate,self.rabackallonum,self.radetail_id,
            self.itemspc_id,self.orderitems_id,self.qtyallocated,self.lastupdate,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

