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

class Orders:
    def __init__(self,member_id,storeent_id,field1=None,providerordernum=None,shipascomplete='Y',field3=None,totaladjustment=0,
    ordchnltyp_id=None,comments=None,notificationid=None,type=None,editor_id=None,buschn_id=None,sourceid=None,expiredate=None,
    blocked=0,opsystem_id=None,transferstatus=None,buyerpo_id=None,currency=None,locked=None,timeplaced=None,lastupdate=None,
    sequence=0,status=None,orgentity_id=None,ormorder=None,totalproduct=0,totaltax=0,totalshipping=0,description=None,
    totaltaxshipping=0,field2=None,address_id=None):
        self.member_id=member_id
        self.storeent_id=storeent_id
        self.field1=field1
        self.address_id=address_id
        self.totaltaxshipping=totaltaxshipping
        self.field2=field2
        self.providerordernum=providerordernum
        self.shipascomplete=shipascomplete
        self.field3=field3
        self.totaladjustment=totaladjustment
        self.ordchnltyp_id=ordchnltyp_id
        self.comments=comments
        self.notificationid=notificationid
        self.type=type
        self.editor_id=editor_id
        self.buschn_id=buschn_id
        self.sourceid=sourceid
        self.expiredate=expiredate
        self.blocked=blocked
        self.opsystem_id=opsystem_id
        self.transferstatus=transferstatus
        self.buyerpo_id=buyerpo_id
        self.currency=currency
        self.locked=locked
        self.timeplaced=timeplaced
        self.lastupdate=lastupdate
        self.sequence=sequence
        self.status=status
        self.orgentity_id=orgentity_id
        self.ormorder=ormorder
        self.totalproduct=totalproduct
        self.totaltax=totaltax
        self.totalshipping=totalshipping
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into orders(ormorder,orgentity_id,totalproduct,totaltax,totalshipping,
            totaltaxshipping,description,storeent_id,currency,locked,timeplaced,lastupdate,sequence,status,
            member_id,field1,address_id,field2,providerordernum,shipascomplete,field3,totaladjustment,
            ordchnltyp_id,comments,notificationid,type,editor_id,buschn_id,sourceid,expiredate,blocked,
            opsystem_id,transferstatus,buyerpo_id)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)returning orders_id""",
            (self.ormorder,self.orgentity_id,self.totalproduct,self.totaltax,self.totalshipping,
            self.totaltaxshipping,self.description,self.storeent_id,self.currency,self.locked,self.timeplaced,self.lastupdate,self.sequence,self.status,
            self.member_id,self.field1,self.address_id,self.field2,self.providerordernum,self.shipascomplete,self.field3,self.totaladjustment,
            self.ordchnltyp_id,self.comments,self.notificationid,self.type,self.editor_id,self.buschn_id,self.sourceid,self.expiredate,self.blocked,
            self.opsystem_id,self.transferstatus,self.buyerpo_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Orderitems:
    def __init__(self,storeent_id,orders_id,member_id,status,quantity,taxamount=None,totaladjustment=0,shiptaxamount=None,
    estavailtime=None,field1=None,description=None,field2=None,allocationgroup=None,shipcharge=None,baseprice=None,
    basecurrency=None,tracknumber=None,trackdate=None,prepareflags=0,correlationgroup=None,promisedavailtime=None,
    shippingoffset=0,neededquantity=0,allocquantity=0,allocffmc_id=None,ordreleasenum=None,configurationid=None,supplierdata=None,
    supplierpartnumber=None,availaquantity=None,isexpedited='N',requestedshipdate=None,tiecode=None,outputq_id=None,
    inventorystatus='NALC',lastcreate=None,lastupdate=None,fulfillmentstatus='INT',lastallocupdate=None,offer_id=None,
    timereleased=None,timeshipped=None,currency=None,totalproduct=0,address_id=None,allocaddress_id=None,price=None,
    lineitemtype=None,termcond_id=None,trading_id=None,itemspc_id=None,catentry_id=None,partnum=None,shipmode_id=None,
    ffmcenter_id=None,comments=None):
        self.storeent_id=storeent_id;self.orders_id=orders_id;self.member_id=member_id
        self.status=status;self.quantity=quantity;self.taxamount=taxamount;self.totaladjustment=totaladjustment
        self.shiptaxamount=shiptaxamount;self.estavailtime=estavailtime;self.field1=field1;self.description=description
        self.field2=field2;self.allocationgroup=allocationgroup;self.shipcharge=shipcharge;self.baseprice=baseprice
        self.basecurrency=basecurrency;self.tracknumber=tracknumber;self.trackdate=trackdate;self.prepareflags=prepareflags
        self.correlationgroup=correlationgroup;self.promisedavailtime=promisedavailtime;self.shippingoffset=shippingoffset
        self.neededquantity=neededquantity;self.allocquantity=allocquantity;self.allocffmc_id=allocffmc_id
        self.ordreleasenum=ordreleasenum;self.configurationid=configurationid;self.supplierdata=supplierdata
        self.supplierpartnumber=supplierpartnumber;self.availaquantity=availaquantity;self.isexpedited=isexpedited
        self.requestedshipdate=requestedshipdate;self.tiecode=tiecode;self.outputq_id=outputq_id
        self.inventorystatus=inventorystatus;self.lastcreate=lastcreate;self.lastupdate=lastupdate
        self.fulfillmentstatus=fulfillmentstatus;self.lastallocupdate=lastallocupdate
        self.offer_id=offer_id;self.timereleased=timereleased;self.timeshipped=timeshipped
        self.currency=currency;self.totalproduct=totalproduct;self.address_id=address_id;self.allocaddress_id=allocaddress_id
        self.price=price;self.lineitemtype=lineitemtype;self.termcond_id=termcond_id;self.trading_id=trading_id
        self.itemspc_id=itemspc_id;self.catentry_id=catentry_id;self.partnum=partnum;self.shipmode_id=shipmode_id
        self.ffmcenter_id=ffmcenter_id;self.comments=comments
    
    def save(self):
        try:
            cursor.execute("""insert into orderitems(storeent_id,orders_id,termcond_id,trading_id,itemspc_id,
            catentry_id,partnum,shipmode_id,ffmcenter_id,member_id,address_id,allocaddress_id,price,lineitemtype,
            status,outputq_id,inventorystatus,lastcreate,fulfillmentstatus,lastallocupdate,offer_id,timereleased,
            timeshipped,currency,comments,totalproduct,quantity,taxamount,totaladjustment,shiptaxamount,estavailtime,
            field1,description,field2,allocationgroup,shipcharge,baseprice,basecurrency,tracknumber,trackdate,
            prepareflags,correlationgroup,promisedavailtime,shippingoffset,neededquantity,allocquantity,allocffmc_id,
            ordreleasenum,configurationid,supplierdata,supplierpartnumber,availaquantity,isexpedited,requestedshipdate,
            tiecode)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)returning orderitems_id""",
            (self.storeent_id,self.orders_id,self.termcond_id,self.trading_id,self.itemspc_id,self.catentry_id,
            self.partnum,self.shipmode_id,self.ffmcenter_id,self.member_id,self.address_id,self.allocaddress_id,
            self.price,self.lineitemtype,self.status,self.outputq_id,self.inventorystatus,self.lastcreate,
            self.fulfillmentstatus,self.lastallocupdate,self.offer_id,self.timereleased,self.timeshipped,self.currency,
            self.comments,self.totalproduct,self.quantity,self.taxamount,self.totaladjustment,self.shiptaxamount,self.estavailtime,
            self.field1,self.description,self.field2,self.allocationgroup,self.shipcharge,self.baseprice,self.basecurrency,
            self.tracknumber,self.trackdate,self.prepareflags,self.correlationgroup,self.promisedavailtime,self.shippingoffset,
            self.neededquantity,self.allocquantity,self.allocffmc_id,self.ordreleasenum,self.configurationid,self.supplierdata,
            self.supplierpartnumber,self.availaquantity,self.isexpedited,self.requestedshipdate,self.tiecode,))
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordrelease:
    def __init__(self,orders_id,ffmacknowledgement=None,status=None,customerconfirm=None,field1=None,field2=None,
    field3=None,pickbatch_id=None,timeplaced=None,lastupdate=None,packslip=None,capturedate=None,extordnum=None,
    extref=None,ffmcenter_id=None,isexpedited=None,shipmode_id=None,address_id=None,member_id=None,
    storeent_id=None):
        self.orders_id=orders_id
        self.ffmacknowledgement=ffmacknowledgement
        self.status=status
        self.customerconfirm=customerconfirm
        self.field1=field1
        self.field2=field2
        self.field3=field3
        self.pickbatch_id=pickbatch_id
        self.timeplaced=timeplaced
        self.lastupdate=lastupdate
        self.packslip=packslip
        self.capturedate=capturedate
        self.extordnum=extordnum
        self.extref=extref
        self.ffmcenter_id=ffmcenter_id
        self.isexpedited=isexpedited
        self.shipmode_id=shipmode_id
        self.address_id=address_id
        self.member_id=member_id
        self.storeent_id=storeent_id
    
    def save(self):
        try:
            cursor.execute("""insert into ordrelease(orders_id,ffmacknowledgement,status,customerconfirm,field1,
            field2,field3,pickbatch_id,timeplaced,lastupdate,packslip,capturedate,extordnum,extref,ffmcenter_id,
            isexpedited,shipmode_id,address_id,member_id,storeent_id)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s)returning ordreleasenum""",(self.orders_id,self.ffmacknowledgement,self.status,
            self.customerconfirm,self.field1,self.field2,self.field3,self.pickbatch_id,self.timeplaced,self.lastupdate,
            self.packslip,self.capturedate,self.extordnum,self.extref,self.ffmcenter_id,self.isexpedited,self.shipmode_id,
            self.address_id,self.member_id,self.storeent_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Manifest:
    def __init__(self,manifest_id,ordreleasenum,shippingcosts,dateshipped,orders_id,weightmeasure=None,
    setccurr=None,shipmode_id=None,weight=None,manifeststatus='S',field1=None,lastupdate=None,packageid=None,
    trackingid=None,pickuprecordid=None):
        self.manifest_id=manifest_id
        self.ordreleasenum=ordreleasenum
        self.weightmeasure=weightmeasure
        self.setccurr=setccurr
        self.shipmode_id=shipmode_id
        self.weight=weight
        self.manifeststatus=manifeststatus
        self.shippingcosts=shippingcosts
        self.dateshipped=dateshipped
        self.field1=field1
        self.lastupdate=lastupdate
        self.packageid=packageid
        self.trackingid=trackingid
        self.pickuprecordid=pickuprecordid
        self.orders_id=orders_id
    
    def save(self):
        try:
            cursor.execute("""insert into manifest(ordreleasenum,weightmeasure,setccurr,shipmode_id,weight,
            manifeststatus,shippingcosts,dateshipped,field1,lastupdate,packageid,trackingid,pickuprecordid,
            orders_id)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)returning manifest_id""",(self.ordreleasenum,
            self.weightmeasure,self.setccurr,self.shipmode_id,self.weight,self.manifeststatus,self.shippingcosts,
            self.dateshipped,self.field1,self.lastupdate,self.packageid,self.trackingid,self.pickuprecordid,
            self.orders_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordshiphst:
    def __init__(self,orderitems_id,versionspc_id,receipt_id=None,qtyshipped=None,dateshipped=None,
    lastupdate=None,qtyreturned=0):
        self.orderitems_id=orderitems_id
        self.versionspc_id=versionspc_id
        self.receipt_id=receipt_id
        self.qtyshipped=qtyshipped
        self.dateshipped=dateshipped
        self.lastupdate=lastupdate
        self.qtyreturned=qtyreturned
    
    def save(self):
        try:
            cursor.execute("""insert into ordshiphst(orderitems_id,versionspc_id,receipt_id,qtyshipped,dateshipped,
            lastupdate,qtyreturned)values(%s,%s,%s,%s,%s,%s,%s) returning ordshiphstnum""",(self.orderitems_id,
            self.versionspc_id,self.receipt_id,self.qtyshipped,self.dateshipped,self.lastupdate,self.qtyreturned,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordpickhst:
    def __init__(self,ordpickhstnum,orderitems_id,versionspc_id,receipt_id=None,qtypicked=None,
    datepicked=None,orderpickingtype=None,lastupdate=None):
        self.ordpickhstnum=ordpickhstnum
        self.orderitems_id=orderitems_id
        self.versionspc_id=versionspc_id
        self.receipt_id=receipt_id
        self.qtypicked=qtypicked
        self.datepicked=datepicked
        self.orderpickingtype=orderpickingtype
        self.lastupdate=lastupdate
    
    def save(self):
        try:
            cursor.execute("""insert into ordpickhst(orderitems_id,versionspc_id,receipt_id,qtypicked,datepicked,
            orderpickingtype,lastupdate)values(%s,%s,%s,%s,%s,%s,%s)returning ordpickhstnum""",(self.orderitems_id,
            self.versionspc_id,self.receipt_id,self.qtypicked,self.datepicked,self.orderpickingtype,self.lastupdate,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Pickbatch:
    def __init__(self,ffmcenter_id,lastupdate=None,member_id=None,pickslip=None,field1=None,field2=None,field3=None,date1=None,date2=None,):
        self.ffmcenter_id=ffmcenter_id
        self.lastupdate=lastupdate
        self.member_id=member_id
        self.pickslip=pickslip
        self.field1=field1
        self.field2=field2
        self.field3=field3
        self.date1=date1
        self.date2=date2
    
    def save(self):
        try:
            cursor.execute("""insert into pickbatch(lastupdate,ffmcenter_id,member_id,pickslip,field1,field2,
            field3,date1,date2)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)returning pickbatch_id""",(self.lastupdate,
            self.ffmcenter_id,self.member_id,self.pickslip,self.field1,self.field2,self.field3,self.date1,self.date2,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Storitmffc:
    def __init__(self,baseitem_id,storeent_id,ffmcenter_id,shippingoffset=86400,):
        self.baseitem_id=baseitem_id
        self.storeent_id=storeent_id
        self.ffmcenter_id=ffmcenter_id
        self.shippingoffset=shippingoffset
    
    def save(self):
        try:
            cursor.execute("""insert into storitmffc(baseitem_id,storeent_id,ffmcenter_id,shippingoffset)
            values(%s,%s,%s,%s)on conflict(baseitem_id,storeent_id,ffmcenter_id)do update set baseitem_id=%s,
            storeent_id=%s,ffmcenter_id=%s,shippingoffset=%s returning baseitem_id""",(self.baseitem_id,
            self.storeent_id,self.ffmcenter_id,self.shippingoffset,self.baseitem_id,self.storeent_id,
            self.ffmcenter_id,self.shippingoffset,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Bkorditem:
    def __init__(self,orderitems_id,dateexpected=None,lastupdate=None):
        self.orderitems_id=orderitems_id
        self.dateexpected=dateexpected
        self.lastupdate=lastupdate
    
    def save(self):
        try:
            cursor.execute("""insert into bkorditem(orderitems_id,dateexpected,lastupdate)
            values(%s,%s,%s)returning orderitems_id""",(self.orderitems_id,self.dateexpected,
            self.lastupdate,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Bkordalloc:
    def __init__(self,orderitems_id,itemspc_id,qtyneeded=None,qtyavailable=None,qtyallocated=None,lastupdate=None):
        self.orderitems_id=orderitems_id
        self.itemspc_id=itemspc_id
        self.qtyneeded=qtyneeded
        self.qtyavailable=qtyavailable
        self.qtyallocated=qtyallocated
        self.lastupdate=lastupdate
    
    def save(self):
        try:
            cursor.execute("""insert into bkordalloc(orderitems_id,itemspc_id,qtyneeded,qtyavailable,
            qtyallocated,lastupdate)values(%s,%s,%s,%s,%s,%s)returning bkordnum""",(self.orderitems_id,
            self.itemspc_id,self.qtyneeded,self.qtyavailable,self.qtyallocated,self.lastupdate,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordpaymthd:
    def __init__(self,paymethod,orders_id,paydevice=None,startdate=None,refundnumber=0,trading_id=None,account_id=None,
    rma_id=None,policy_id=None,paysummary_id=None,enddate=None,buyerpo_id=None,maxamount=None,creditline_id=None,
    actualamount=None,chargeamount=None,chargetime=None,chargeamtcurr=None,stringfield1=None,stringfield2=None,
    stringfield3=None,stringfield4=None,status=None,bigintfield1=None,bigintfield2=None,bigintfield3=None,
    decimalfield1=None,decimalfield2=None,decimalfield3=None,paymentdata=None):
        self.paymethod=paymethod
        self.orders_id=orders_id
        self.paydevice=paydevice
        self.startdate=startdate
        self.refundnumber=refundnumber
        self.trading_id=trading_id
        self.account_id=account_id
        self.rma_id=rma_id
        self.policy_id=policy_id
        self.paysummary_id=paysummary_id
        self.enddate=enddate
        self.buyerpo_id=buyerpo_id
        self.maxamount=maxamount
        self.creditline_id=creditline_id
        self.actualamount=actualamount
        self.chargeamount=chargeamount
        self.chargetime=chargetime
        self.chargeamtcurr=chargeamtcurr
        self.paymentdata=paymentdata
        self.stringfield1=stringfield1
        self.stringfield2=stringfield2
        self.stringfield3=stringfield3
        self.stringfield4=stringfield4
        self.status=status
        self.bigintfield1=bigintfield1
        self.bigintfield2=bigintfield2
        self.bigintfield3=bigintfield3
        self.decimalfield1=decimalfield1
        self.decimalfield2=decimalfield2
        self.decimalfield3=decimalfield3
    
    def save(self):
        try:
            cursor.execute("""insert into ordpaymthd(paymethod,orders_id,paydevice,startdate,refundnumber,
            trading_id,account_id,rma_id,policy_id,paysummary_id,enddate,buyerpo_id,maxamount,creditline_id,
            actualamount,chargeamount,chargetime,chargeamtcurr,paymentdata,stringfield1,stringfield2,
            stringfield3,stringfield4,status,bigintfield1,bigintfield2,bigintfield3,decimalfield1,
            decimalfield2,decimalfield3)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(orders_id,paymethod,refundnumber)do update set
            paymethod=%s,orders_id=%s,paydevice=%s,startdate=%s,refundnumber=%s,trading_id=%s,account_id=%s,
            rma_id=%s,policy_id=%s,paysummary_id=%s,enddate=%s,buyerpo_id=%s,maxamount=%s,creditline_id=%s,
            actualamount=%s,chargeamount=%s,chargetime=%s,chargeamtcurr=%s,paymentdata=%s,stringfield1=%s,
            stringfield2=%s,stringfield3=%s,stringfield4=%s,status=%s,bigintfield1=%s,bigintfield2=%s,
            bigintfield3=%s,decimalfield1=%s,decimalfield2=%s,decimalfield3=%s returning orders_id""",
            (self.paymethod,self.orders_id,self.paydevice,self.startdate,self.refundnumber,self.trading_id,
            self.account_id,self.rma_id,self.policy_id,self.paysummary_id,self.enddate,self.buyerpo_id,
            self.maxamount,self.creditline_id,self.actualamount,self.chargeamount,self.chargetime,self.chargeamtcurr,
            self.paymentdata,self.stringfield1,self.stringfield2,self.stringfield3,self.stringfield4,
            self.status,self.bigintfield1,self.bigintfield2,self.bigintfield3,self.decimalfield1,self.decimalfield2,
            self.decimalfield3,
            self.paymethod,self.orders_id,self.paydevice,self.startdate,self.refundnumber,self.trading_id,
            self.account_id,self.rma_id,self.policy_id,self.paysummary_id,self.enddate,self.buyerpo_id,
            self.maxamount,self.creditline_id,self.actualamount,self.chargeamount,self.chargetime,self.chargeamtcurr,
            self.paymentdata,self.stringfield1,self.stringfield2,self.stringfield3,self.stringfield4,
            self.status,self.bigintfield1,self.bigintfield2,self.bigintfield3,self.decimalfield1,self.decimalfield2,
            self.decimalfield3,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Creditline:
    def __init__(self,setccurr=None,account_id=0,timecreated=None,timeupdated=None,creditlimit=None,decimalfield1=None,decimalfield2=None):
        self.setccurr=setccurr
        self.account_id=account_id
        self.timecreated=timecreated
        self.timeupdated=timeupdated
        self.creditlimit=creditlimit
        self.decimalfield1=decimalfield1
        self.decimalfield2=decimalfield2
    
    def save(self):
        try:
            cursor.execute("""insert into creditline(setccurr,account_id,timecreated,timeupdated,creditlimit,
            decimalfield1,decimalfield2)values(%s,%s,%s,%s,%s,%s,%s)returning creditline_id""",(self.setccurr,
            self.account_id,self.timecreated,self.timeupdated,self.creditlimit,self.decimalfield1,self.decimalfield2,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Orcomment:
    def __init__(self,orders_id,lastupdate=None,comments=None,ordchgrsn_id=None,servicerep_id=None,buschn_id=None,
    orderversion=None,field1=None,field2=None,field3=None):
        self.orders_id=orders_id
        self.lastupdate=lastupdate
        self.comments=comments
        self.ordchgrsn_id=ordchgrsn_id
        self.servicerep_id=servicerep_id
        self.buschn_id=buschn_id
        self.orderversion=orderversion
        self.field1=field1
        self.field2=field2
        self.field3=field3
    
    def save(self):
        try:
            cursor.execute("""insert into orcomment(orders_id,lastupdate,comments,ordchgrsn_id,servicerep_id,
            buschn_id,orderversion,field1,field2,field3)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)returning orcomment_id""",
            (self.orders_id,self.lastupdate,self.comments,self.ordchgrsn_id,self.servicerep_id,self.buschn_id,
            self.orderversion,self.field1,self.field2,self.field3,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Buschn:
    def __init__(self,buschn_id,name,state):
        self.buschn_id=buschn_id
        self.name=name
        self.state=state
    
    def save(self):
        try:
            cursor.execute("""insert into buschn(buschn_id,name,state)values(%s,%s,%s)
            returning buschn_id""",(self.buschn_id,self.name,self.state,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Buyerpo:
    def __init__(self,ponumber,buyerpotyp_id,state=0,amount=None,setccurr=None,account_id=None,):
        self.ponumber=ponumber
        self.buyerpotyp_id=buyerpotyp_id
        self.state=state
        self.amount=amount
        self.setccurr=setccurr
        self.account_id=account_id
    
    def save(self):
        try:
            cursor.execute("""insert into buyerpo(ponumber,buyerpotyp_id,state,amount,setccurr,account_id)
            values(%s,%s,%s,%s,%s,%s)returning buyerpo_id""",(self.ponumber,self.buyerpotyp_id,self.state,
            self.amount,self.setccurr,self.account_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordusers:
    def __init__(self,orders_id,creator=None,submitter=None):
        self.orders_id=orders_id
        self.creator=creator
        self.submitter=submitter
    
    def save(self):
        try:
            cursor.execute("""insert into ordusers(orders_id,creator,submitter)values(%s,%s,%s)
            on conflict(orders_id)do update set orders_id=%s,creator=%s,submitter=%s returning
            orders_id""",(self.orders_id,self.creator,self.submitter,self.orders_id,self.creator,
            self.submitter,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Orderhist:
    def __init__(self,orders_id,orderversion,lastupdate,orderdata,field1,field2,field3):
        self.orders_id=orders_id
        self.orderversion=orderversion
        self.lastupdate=lastupdate
        self.orderdata=orderdata
        self.field1=field1
        self.field2=field2
        self.field3=field3
    
    def save(self):
        try:
            cursor.execute("""insert into orderhist(orders_id,orderversion,lastupdate,orderdata,
            field1,field2,field3)values(%s,%s,%s,%s,%s,%s,%s)on conflict(orders_id,orderversion)
            do update set orders_id=%s,orderversion=%s,lastupdate=%s,orderdata=%s,field1=%s,field2=%s,
            field3=%s returning orders_id""",(self.orders_id,self.orderversion,self.lastupdate,
            self.orderdata,self.field1,self.field2,self.field3,self.orders_id,self.orderversion,
            self.lastupdate,self.orderdata,self.field1,self.field2,self.field3,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordpayinfo:
    def __init__(self,orders_id,name,value):
        self.orders_id=orders_id
        self.name=name
        self.value=value

    def save(self):
        try:
            cursor.execute("""insert into ordpayinfo(orders_id,name,value)values(%s,%s,%s)
            returning ordpayinfo_id""",(self.orders_id,self.name,self.value,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordoptions:
    def __init__(self,orders_id,notifymerchant=None,notifyshopper=None):
        self.orders_id=orders_id
        self.notifymerchant=notifymerchant
        self.notifyshopper=notifyshopper
    
    def save(self):
        try:
            cursor.execute("""insert into ordoptions(orders_id,notifymerchant,notifyshopper)
            values(%s,%s,%s)on conflict(orders_id)do update set orders_id=%s,notifymerchant=%s
            notifyshopper=%s returning orders_id""",(self.orders_id,self.notifymerchant,
            self.notifyshopper,self.orders_id,self.notifymerchant,self.notifyshopper,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Cpendorder:
    def __init__(self,storeent_id,orders_id,member_id,field1=None,field2=None):
        self.storeent_id=storeent_id
        self.orders_id=orders_id
        self.member_id=member_id
        self.field1=field1
        self.field2=field2
    
    def save(self):
        try:
            cursor.execute("""insert into cpendorder(storeent_id,orders_id,member_id,field1,field2)
            values(%s,%s,%s,%s,%s)on conflict(orders_id,member_id)do update set storeent_id=%s,
            orders_id=%s,member_id=%s,field1=%s,field2=%s""",(self.storeent_id,self.orders_id,
            self.member_id,self.field1,self.field2,self.storeent_id,self.orders_id,
            self.member_id,self.field1,self.field2,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordtax:
    def __init__(self,orders_id,taxcgry_id,taxamount,lastupdate=None):
        self.orders_id=orders_id
        self.taxcgry_id=taxcgry_id
        self.taxamount=taxamount
        self.lastupdate=lastupdate
    
    def save(self):
        try:
            cursor.execute("""insert into ordtax(orders_id,taxcgry_id,taxamount,lastupdate)values
            (%s,%s,%s,%s)on conflict(orders_id,taxcgry_id)do update set orders_id=%s,taxcgry_id=%s,
            taxamount=%s,lastupdate=%s returning orders_id""",(self.orders_id,self.taxcgry_id,
            self.taxamount,self.lastupdate,self.orders_id,self.taxcgry_id,self.taxamount,self.lastupdate,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Blkrsncode:
    def __init__(self,blockreasontype,manualblock,markfordelete=0,field1=None,field2=None):
        self.blockreasontype=blockreasontype
        self.manualblock=manualblock
        self.markfordelete=markfordelete
        self.field1=field1
        self.field2=field2
    
    def save(self):
        try:
            cursor.execute("""insert into blkrsncode(blockreasontype,manualblock,markfordelete,field1,field2)
            values(%s,%s,%s,%s,%s)returning blkrsncode_id""",(self.blockreasontype,self.manualblock,
            self.markfordelete,self.field1,self.field2,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Blkrsndesc:
    def __init__(self,blkrsncode_id,language_id,description):
        self.blkrsncode_id=blkrsncode_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into blkrsndesc(blkrsncode_id,language_id,description)
            values(%s,%s,%s)on conflict(blkrsncode_id,language_id)do update set blkrsncode_id=%s,
            language_id=%s,description=%s returning blkrsncode_id""",(self.blkrsncode_id,
            self.language_id,self.description,self.blkrsncode_id,self.language_id,self.description,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Orderblk:
    def __init__(self,orders_id,blkrsncode_id,timeblocked,resolved,field1,field2):
        self.orders_id=orders_id
        self.blkrsncode_id=blkrsncode_id
        self.timeblocked=timeblocked
        self.resolved=resolved
        self.field1=field1
        self.field2=field2
    
    def save(self):
        try:
            cursor.execute("""insert into orderblk(orders_id,blkrsncode_id,timeblocked,resolved,
            field1,field2)values(%s,%s,%s,%s,%s,%s)returning orderblk_id""",(self.orders_id,
            self.blkrsncode_id,self.timeblocked,self.resolved,self.field1,self.field2,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Suborders:
    def __init__(self,orders_id,address_id=None,country=None,totalproduct=0,totaltax=0,
    totalshipping=0,currency=None,field1=None,field2=None,field3=None,totaladjustment=0):
        self.orders_id=orders_id
        self.address_id=address_id
        self.country=country
        self.totalproduct=totalproduct
        self.totaltax=totaltax
        self.totalshipping=totalshipping
        self.currency=currency
        self.field1=field1
        self.field2=field2
        self.field3=field3
        self.totaladjustment=totaladjustment

    def save(self):
        try:
            cursor.execute("""insert into suborders(orders_id,address_id,country,totalproduct,totaltax,
            totalshipping,currency,field1,field2,field3,totaladjustment)values(%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s)returning suborder_id""",(self.orders_id,self.address_id,self.country,self.totalproduct,
            self.totaltax,self.totalshipping,self.currency,self.field1,self.field2,self.field3,self.totaladjustment,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordadjust:
    def __init__(self,orders_id,calcode_id=None,calusage_id=None,amount=None,displaylevel=0):
        self.orders_id=orders_id
        self.calcode_id=calcode_id
        self.calusage_id=calusage_id
        self.amount=amount
        self.displaylevel=displaylevel
    
    def save(self):
        try:
            cursor.execute("""insert into ordadjust(orders_id,calcode_id,calusage_id,amount,displaylevel)
            values(%s,%s,%s,%s,%s)returning ordadjust_id""",(self.orders_id,self.calcode_id,self.calusage_id,
            self.amount,self.displaylevel,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordiadjust:
    def __init__(self,ordadjust_id,orderitems_id,amount=0):
        self.ordadjust_id=ordadjust_id
        self.orderitems_id=orderitems_id
        self.amount=amount
    
    def save(self):
        try:
            cursor.execute("""insert into ordiadjust(ordadjust_id,orderitems_id,amount)values
            (%s,%s,%s)returning ordiadjust_id""",(self.ordadjust_id,self.orderitems_id,self.amount,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordadjtxex:
    def __init__(self,ordadjust_id,taxcgry_id):
        self.ordadjust_id=ordadjust_id
        self.taxcgry_id=taxcgry_id
    
    def save(self):
        try:
            cursor.execute("""insert into ordadjtxex(ordadjust_id,taxcgry_id)values(%s,%s)
            returning ordadjust_id""",(self.ordadjust_id,self.taxcgry_id,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordadjdsc:
    def __init__(self,ordadjust_id,language_id,description):
        self.ordadjust_id=ordadjust_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into ordadjdsc(ordadjust_id,language_id,description)
            values(%s,%s,%s)returning ordadjust_id""",(self.ordadjust_id,self.language_id,self.description,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rmaiadjcrd:
    def __init__(self,rmaitem_id,ordadjust_id,amount=0):
        self.rmaitem_id=rmaitem_id
        self.ordadjust_id=ordadjust_id
        self.amount=amount
    
    def save(self):
        try:
            cursor.execute("""insert into rmaiadjcrd(rmaitem_id,ordadjust_id,amount)values(%s,%s,%s)
            returning rmaiadjcrd_id""",(self.rmaitem_id,self.ordadjust_id,self.amount,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rmaitem:
    def __init__(self,rma_id,catentry_id,member_id,itemspc_id,rtnreason_id,refundorreplace,quantity,currency,
    orderitems_id=None,comments=None,taxamount=None,adjustmentcredit=0,adjustment=0,lastupdate=None,
    totalcredit=0,invquantity=0,creditdate=None,status='PND',creditamount=0):
        self.rma_id=rma_id
        self.catentry_id=catentry_id
        self.member_id=member_id
        self.itemspc_id=itemspc_id
        self.rtnreason_id=rtnreason_id
        self.refundorreplace=refundorreplace
        self.quantity=quantity
        self.currency=currency
        self.orderitems_id=orderitems_id
        self.comments=comments
        self.taxamount=taxamount
        self.adjustmentcredit=adjustmentcredit
        self.adjustment=adjustment
        self.lastupdate=lastupdate
        self.totalcredit=totalcredit
        self.invquantity=invquantity
        self.creditdate=creditdate
        self.status=status
        self.creditamount=creditamount
    
    def save(self):
        try:
            cursor.execute("""insert into rmaitem(rma_id,catentry_id,member_id,orderitems_id,itemspc_id,
            rtnreason_id,refundorreplace,creditamount,quantity,creditdate,status,currency,comments,
            taxamount,adjustmentcredit,adjustment,lastupdate,totalcredit,invquantity)values(%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)returning rmaitem_id""",(self.rma_id,self.catentry_id,
            self.member_id,self.orderitems_id,self.itemspc_id,self.rtnreason_id,self.refundorreplace,self.creditamount,
            self.quantity,self.creditdate,self.status,self.currency,self.comments,self.taxamount,self.adjustmentcredit,
            self.adjustment,self.lastupdate,self.totalcredit,self.invquantity,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
    
    class Rma:
        def __init__(self,store_id,member_id,rmadate,orgentity_id=None,policy_id=None,trading_id=None,
        ffmcenter_id=None,totalcredit=0,status='PRC',comments=None,lastupdate=None,refundagainstordid=None,
        inuse='N',currency=None,prepared='N'):
            self.store_id=store_id
            self.member_id=member_id
            self.rmadate=rmadate
            self.orgentity_id=orgentity_id
            self.policy_id=policy_id
            self.trading_id=trading_id
            self.ffmcenter_id=ffmcenter_id
            self.totalcredit=totalcredit
            self.status=status
            self.comments=comments
            self.lastupdate=lastupdate
            self.refundagainstordid=refundagainstordid
            self.inuse=inuse
            self.currency=currency
            self.prepared=prepared
        
        def save(self):
            try:
                cursor.execute("""insert into rma(store_id,orgentity_id,policy_id,member_id,trading_id,ffmcenter_id,
                rmadate,totalcredit,status,comments,lastupdate,refundagainstordid,inuse,currency,prepared)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)returning rma_id""",(self.store_id,
                self.orgentity_id,self.policy_id,self.member_id,self.trading_id,self.ffmcenter_id,
                self.rmadate,self.totalcredit,self.status,self.comments,self.lastupdate,self.refundagainstordid,
                self.inuse,self.currency,self.prepared,));con.commit();return cursor.fetchone()[0]
            except(Exception,psycopg2.DatabaseError) as e:
                if con is not None:con.rollback()
                raise EntryException(str(e).strip().split('\n')[0])

class Rmacharge:
    def __init__(self,chargetype_id,rma_id,amount,currency,rmaitem_id):
        self.chargetype_id=chargetype_id
        self.rma_id=rma_id
        self.amount=amount
        self.currency=currency
        self.rmaitem_id=rmaitem_id
    
    def save(self):
        try:
            cursor.execute("""insert into rmacharge(rmaitem_id,chargetype_id,rma_id,amount,currency)
            values(%s,%s,%s,%s,%s)returning rmacharge_id""",(self.rmaitem_id,self.chargetype_id,self.rma_id,
            self.amount,self.currency,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rmatax:
    def __init__(self,rma_id,taxcgry_id,taxamount,lastupdate):
        self.rma_id=rma_id
        self.taxcgry_id=taxcgry_id
        self.taxamount=taxamount
        self.lastupdate=lastupdate
    
    def save(self):
        try:
            cursor.execute("""insert into rmatax(rma_id,taxcgry_id,taxamount,lastupdate)values
            (%s,%s,%s,%s)returning rma_id""",(self.rma_id,self.taxcgry_id,self.taxamount,self.lastupdate,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Chargetype:
    def __init__(self,storeent_id,displayaggregated,code,markfordelete=0):
        self.storeent_id=storeent_id
        self.displayaggregated=displayaggregated
        self.code=code
        self.markfordelete=markfordelete
    
    def save(self):
        try:
            cursor.execute("""insert into chargetype(storeent_id,markfordelete,displayaggregated,code)
            values(%s,%s,%s,%s)returning chargetype_id""",(self.storeent_id,self.markfordelete,self.displayaggregated,
            self.code,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Chrgtypdsc:
    def __init__(self,chargetype_id,language_id,description):
        self.chargetype_id=chargetype_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into chrgtypdsc(chargetype_id,language_id,description)
            values(%s,%s,%s)on conflict(chargetype_id,language_id)do update set chargetype_id=%s,
            language_id=%s,description=%s returning chargetype_id""",(self.chargetype_id,self.language_id,
            self.description,self.chargetype_id,self.language_id,self.description,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rtnreason:
    def __init__(self,storeent_id,code,markfordelete=0,reasontype='B'):
        self.storeent_id=storeent_id
        self.code=code
        self.markfordelete=markfordelete
        self.reasontype=reasontype
    
    def save(self):
        try:
            cursor.execute("""insert into rtnreason(reasontype,storeent_id,markfordelete,code)values
            (%s,%s,%s,%s)returning rtnreason_id""",(self.reasontype,self.storeent_id,self.markfordelete,
            self.code,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rtnrsndesc:
    def __init__(self,rtnreason_id,language_id,description):
        self.rtnreason_id=rtnreason_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into rtnrsndesc(rtnreason_id,language_id,description)values
            (%s,%s,%s)returning rtnreason_id""",(self.rtnreason_id,self.language_id,self.description,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rtndspdesc:
    def __init__(self,rtndspcode_id,language_id,description=None):
        self.rtndspcode_id=rtndspcode_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into rtndspdesc(rtndspcode_id,language_id,description)
            values(%s,%s,%s)on conflict(rtndspcode_id,language_id)do update set rtndspcode_id,
            language_id=%s,description=%s returning rtndspcode_id""",(self.rtndspcode_id,
            self.language_id,self.description,self.rtndspcode_id,self.language_id,self.description,))
            con.commit();return cursor.fetchone()
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rtndspcode:
    def __init__(self,storeent_id,code,markfordelete=0,returntoinventory='Y'):
        self.storeent_id=storeent_id
        self.code=code
        self.markfordelete=markfordelete
        self.returntoinventory=returntoinventory
    
    def save(self):
        try:
            cursor.execute("""insert into rtndspcode(returntoinventory,storeent_id,code,markfordelete)values
            (%s,%s,%s,%s)on conflict(code,storeent_id)do update set returntoinventory=%s,storeent_id=%s,
            code=%s,markfordelete=%s returning rtndspcode_id""",(self.returntoinventory,self.storeent_id,
            self.code,self.markfordelete,self.returntoinventory,self.storeent_id,self.code,self.markfordelete,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rtnrcptdsp:
    def __init__(self,rtndspcode_id,rtnreceipt_id,rtnrcptdsp_id,dispositiondate,quantity,rtnreason_id,comments):
        self.rtndspcode_id=rtndspcode_id
        self.rtnreceipt_id=rtnreceipt_id
        self.rtnrcptdsp_id=rtnrcptdsp_id
        self.dispositiondate=dispositiondate
        self.quantity=quantity
        self.rtnreason_id=rtnreason_id
        self.comments=comments
    
    def save(self):
        try:
            cursor.execute("""insert into rtnrcptdsp(rtndspcode_id,rtnreceipt_id,rtnrcptdsp_id,rtnreason_id,
            quantity,dispositiondate,comments)values(%s,%s,%s,%s,%s,%s,%s)on conflict(rtnreceipt_id,rtnrcptdsp_id)
            do update set rtndspcode_id=%s,rtnreceipt_id=%s,rtnrcptdsp_id=%s,rtnreason_id=%s,quantity=%s,
            dispositiondate=%s,comments=%s returning rtndspcode_id""",(self.rtndspcode_id,self.rtnreceipt_id,
            self.rtnrcptdsp_id,self.rtnreason_id,self.quantity,self.dispositiondate,self.comments,
            self.rtndspcode_id,self.rtnreceipt_id,
            self.rtnrcptdsp_id,self.rtnreason_id,self.quantity,self.dispositiondate,self.comments,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rtnreceipt:
    def __init__(self,rma_id,versionspc_id,rmaitemcmp_id,lastupdate,quantity,datereceived,dispocitiondqty=0):
        self.rma_id=rma_id
        self.versionspc_id=versionspc_id
        self.rmaitemcmp_id=rmaitemcmp_id
        self.lastupdate=lastupdate
        self.quantity=quantity
        self.datereceived=datereceived
        self.dispocitiondqty=dispocitiondqty
    
    def save(self):
        try:
            cursor.execute("""insert into rtnreceipt(rma_id,versionspc_id,rmaitemcmp_id,lastupdate,quantity,
            datereceived,dispocitiondqty)values(%s,%s,%s,%s,%s,%s,%s)returning rtnreceipt_id""",(self.rma_id,
            self.versionspc_id,self.rmaitemcmp_id,self.lastupdate,self.quantity,self.datereceived,self.dispocitiondqty,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rmaitemcmp:
    def __init__(self,rmaitem_id,itemspc_id,quantity,shouldreceive='Y',invquantity=0,catentry_id=None,):
        self.rmaitem_id=rmaitem_id
        self.itemspc_id=itemspc_id
        self.quantity=quantity
        self.shouldreceive=shouldreceive
        self.invquantity=invquantity
        self.catentry_id=catentry_id
    
    def save(self):
        try:
            cursor.execute("""insert into rmaitemcmp(rmaitem_id,catentry_id,itemspc_id,quantity,
            shouldreceive,invquantity)values(%s,%s,%s,%s,%s,%s)returning rmaitemcmp_id""",
            (self.rmaitem_id,self.catentry_id,self.itemspc_id,self.quantity,self.shouldreceive,self.invquantity,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Exchgorders:
    def __init__(self,rma_id,cross_ship='N'):
        self.rma_id=rma_id
        self.cross_ship=cross_ship
    
    def save(self):
        try:
            cursor.execute("""insert into exchgorders(rma_id,cross_ship)values(%s,%s)
            returning ex_ord_id""",(self.rma_id,self.cross_ship,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rmaauthlog:
    def __init__(self,authnoticedate,rma_id):
        self.authnoticedate=authnoticedate
        self.rma_id=rma_id
    
    def save(self):
        try:
            cursor.execute("""insert into rmaauthlog(authnoticedate,rma_id)values(authnoticedate,rma_id)
            do update set authnoticedate=%s,rma_id=%s returning rmaauthlog_id""",(self.authnoticedate,
            self.rma_id,self.authnoticedate,self.rma_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rmaitemserial:
    def __init__(self,rmaitem_id,receivedquantity,creation_timestamp,lastupdate,quantity,serialnumber,rmaitemcmp_id):
        self.rmaitem_id=rmaitem_id
        self.receivedquantity=receivedquantity
        self.creation_timestamp=creation_timestamp
        self.lastupdate=lastupdate
        self.quantity=quantity
        self.serialnumber=serialnumber
        self.rmaitemcmp_id=rmaitemcmp_id
    
    def save(self):
        try:
            cursor.execute("""insert into rmaitemserial(rmaitem_id,rmaitemcmp_id,serialnumber,quantity,
            receivedquantity,creation_timestamp,lastupdate)values(%s,%s,%s,%s,%s,%s,%s)values
            (%s,%s,%s,%s,%s,%s,%s)returning rmaitemserial_id""",(self.rmaitem_id,self.rmaitemcmp_id,
            self.serialnumber,self.quantity,self.receivedquantity,self.creation_timestamp,self.lastupdate,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rtndnyrsndesc:
    def __init__(self,rtndnyrsn_id,language_id,description):
        self.rtndnyrsn_id=rtndnyrsn_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into rtndnyrsndesc(rtndnyrsn_id,language_id,description)values
            (%s,%s,%s)on conflict(rtndnyrsn_id,language_id)do update set rtndnyrsn_id=%s,language_id=%s,
            description=%s returning rtndnyrsn_id""",(self.rtndnyrsn_id,self.language_id,self.description,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rtndnyrsn:
    def __init__(self,storeent_id,code,markfordelete=0):
        self.storeent_id=storeent_id
        self.code=code
        self.markfordelete=markfordelete
    
    def save(self):
        try:
            cursor.execute("""insert into rtndnyrsn(storeent_id,code,markfordelete)values
            (%s,%s,%s)returning rtndnyrsn_id""",(self.storeent_id,self.code,self.markfordelete,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Rmaidnyrsn:
    def __init__(self,rmaitem_id,rtndnyrsn_id):
        self.rmaitem_id=rmaitem_id
        self.rtndnyrsn_id=rtndnyrsn_id
    
    def save(self):
        try:
            cursor.execute("""insert into rmaidnyrsn(rmaitem_id,rtndnyrsn_id)values(%s,%s)
            returning rmaitem_id""",(self.rmaitem_id,self.rtndnyrsn_id,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Orditax:
    def __init__(self,orderitems_id,taxcgry_id,taxamount,taxcgry_dsc=None):
        self.orderitems_id=orderitems_id
        self.taxcgry_id=taxcgry_id
        self.taxamount=taxamount
        self.taxcgry_dsc=taxcgry_dsc
    
    def save(self):
        try:
            cursor.execute("""insert into orditax(orderitems_id,taxcgry_id,taxamount,taxcgry_dsc)
            values(%s,%s,%s,%s)on conflict(orderitems_id,taxcgry_id)do update set orderitems_id=%s,
            taxcgry_id=%s,taxamount=%s,taxcgry_dsc=%s returning orderitems_id""",(self.orderitems_id,
            self.taxcgry_id,self.taxamount,self.taxcgry_dsc,self.orderitems_id,self.taxcgry_id,
            self.taxamount,self.taxcgry_dsc,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Subordtax:
    def __init__(self,suborder_id,taxcgry_id,taxamount):
        self.suborder_id=suborder_id
        self.taxcgry_id=taxcgry_id
        self.taxamount=taxamount
    
    def save(self):
        try:
            cursor.execute("""insert into subordtax(suborder_id,taxcgry_id,taxamount)values(%s,%s,%s)
            on conflict(suborder_id,taxcgry_id)do update set suborder_id=%s,taxcgry_id=%s,taxamount=%s
            returning suborder_id""",(self.suborder_id,self.taxcgry_id,self.taxamount,self.suborder_id,
            self.taxcgry_id,self.taxamount,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Paysummary:
    def __init__(self,periodstarttime,periodendtime,totalcharge,storeent_id,setccurr=None,creditline_id=None,
    policy_id=None,paysummarydata=None,status=None,account_id=None):
        self.periodstarttime=periodstarttime
        self.periodendtime=periodendtime
        self.totalcharge=totalcharge
        self.storeent_id=storeent_id
        self.setccurr=setccurr
        self.creditline_id=creditline_id
        self.policy_id=policy_id
        self.paysummarydata=paysummarydata
        self.status=status
        self.account_id=account_id
    
    def save(self):
        try:
            cursor.execute("""insert into paysummary(account_id,setccurr,creditline_id,storeent_id,policy_id,
            periodstarttime,periodendtime,totalcharge,paysummarydata,status)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            returning paysummary_id""",(self.account_id,self.setccurr,self.creditline_id,self.storeent_id,
            self.policy_id,self.periodstarttime,self.periodendtime,self.totalcharge,self.paysummarydata,
            self.status,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Trdrefamt:
    def __init__(self,orders_id,rma_id,trading_id,amount,setccurr):
        self.orders_id=orders_id
        self.rma_id=rma_id
        self.trading_id=trading_id
        self.amount=amount
        self.setccurr=setccurr
    
    def save(self):
        try:
            cursor.execute("""insert into trdrefamt(orders_id,setccurr,rma_id,trading_id,amount)values
            (%s,%s,%s,%s,%s)returning trdrefamt_id""",(self.orders_id,self.setccurr,self.rma_id,self.trading_id,
            self.amount,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Trddepamt:
    def __init__(self,orders_id,trading_id,amount,setccurr=None,orderitems_id=None):
        self.orders_id=orders_id
        self.trading_id=trading_id
        self.amount=amount
        self.setccurr=setccurr
        self.orderitems_id=orderitems_id
    
    def save(self):
        try:
            cursor.execute("""insert into trddepamt(orderitems_id,orders_id,trading_id,setccurr,
            amount)values(%s,%s,%s,%s,%s)on conflict(trading_id,orders_id,orderitems_id)do update set
            orderitems_id=%s,orders_id=%s,trading_id=%s,setccurr=%s,amount=%s returning trddepamt_id""",
            (self.orderitems_id,self.orders_id,self.trading_id,self.setccurr,self.amount,
            self.orderitems_id,self.orders_id,self.trading_id,self.setccurr,self.amount,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Trdpuramt:
    def __init__(self,trading_id,amount,orders_id,setccurr=None,orderitems_id=None,):
        self.trading_id=trading_id
        self.amount=amount
        self.orders_id=orders_id
        self.setccurr=setccurr
        self.orderitems_id=orderitems_id
    
    def save(self):
        try:
            cursor.execute("""insert into trdpuramt(trading_id,setccurr,orderitems_id,
            amount,orders_id)values(%s,%s,%s,%s,%s)returning trdpuramt_id""",(self.trading_id,
            self.setccurr,self.orderitems_id,self.amount,self.orders_id,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Orditrd:
    def __init__(self,orderitems_id,trading_id):
        self.orderitems_id=orderitems_id
        self.trading_id=trading_id
        
    def save(self):
        try:
            cursor.execute("""insert into orditrd(orderitems_id,trading_id)values(%s,%s)
            on conflict(orderitems_id,trading_id)do update set orderitems_id=%s,trading_id=%s
            returning trading_id""",(self.orderitems_id,self.trading_id,self.orderitems_id,self.trading_id,))
            con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordquotrel:
    def __init__(self,parent_id,reltype,displaysequence=0,flags=0,child_id=None,childstore_id=None,
    trading_id=None,timeouttime=None,):
        self.parent_id=parent_id
        self.reltype=reltype
        self.displaysequence=displaysequence
        self.flags=flags
        self.child_id=child_id
        self.childstore_id=childstore_id
        self.trading_id=trading_id
        self.timeouttime=timeouttime
    
    def save(self):
        try:
            cursor.execute("""insert into ordquotrel(parent_id,child_id,childstore_id,trading_id,
            reltype,timeouttime,displaysequence,flags)values(%s,%s,%s,%s,%s,%s,%s,%s)returning ordquotrel_id""",
            (self.parent_id,self.child_id,self.childstore_id,self.trading_id,self.reltype,self.timeouttime,
            self.displaysequence,self.flags,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Ordrlsttls:
    def __init__(self,orders_id,ordreleasenum,chargetype,amount=None,lastcreated=None,field1=None,field2=None,field3=None):
        self.orders_id=orders_id
        self.ordreleasenum=ordreleasenum
        self.chargetype=chargetype
        self.amount=amount
        self.lastcreated=lastcreated
        self.field1=field1
        self.field2=field2
        self.field3=field3
    
    def save(self):
        try:
            cursor.execute("""insert into ordrlsttls(orders_id,ordreleasenum,chargetype,amount,lastcreated,
            field1,field2,field3)values(%s,%s,%s,%s,%s,%s,%s,%s)on conflict(orders_id,ordreleasenum,chargetype)
            do update set orders_id=%s,ordreleasenum=%s,chargetype=%s,amount=%s,lastcreated=%s,field1=%s,field2=%s,
            field3=%s returning orders_id""",(self.orders_id,self.ordreleasenum,self.chargetype,self.amount,
            self.lastcreated,self.field1,self.field2,self.field3,
            self.orders_id,self.ordreleasenum,self.chargetype,self.amount,
            self.lastcreated,self.field1,self.field2,self.field3,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Orditemconf:
    def __init__(self,orderitems_id,ordreleasenum,quantity,confirmtype,lastupdate,creation=None,
    serialnumber=None,manifest_id=None,oicomplist_id=None,):
        self.orderitems_id=orderitems_id
        self.ordreleasenum=ordreleasenum
        self.quantity=quantity
        self.confirmtype=confirmtype
        self.lastupdate=lastupdate
        self.creation=creation
        self.serialnumber=serialnumber
        self.manifest_id=manifest_id
        self.oicomplist_id=oicomplist_id
    
    def save(self):
        try:
            cursor.execute("""insert into orditemconf(orderitems_id,oicomplist_id,serialnumber,manifest_id,
            ordreleasenum,quantity,confirmtype,creation,lastupdate)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            returning orditemconf_id""",(self.orderitems_id,self.oicomplist_id,self.serialnumber,self.manifest_id,
            self.ordreleasenum,self.quantity,self.confirmtype,self.creation,self.lastupdate,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
