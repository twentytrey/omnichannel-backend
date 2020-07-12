from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","pronov","localhost","5432")

class ShippingMethods:
    def __init__(self,store_id,customer_id,gross):
        self.gross=gross
        self.calusage_id=2
        self.store_id=store_id
        self.customer_id=customer_id
        self.staddress_id,self.ffmcenter_id=self.getffmcenter()
        self.address_id,self.customercity,self.customerstate,self.customercountry=self.getcustomeraddress()
        self.jurstids,self.jurstgroupids=self.getjurst()
        self.calrule_id,self.calcode_id,self.calrule_id,self.calrulecalculate,self.calrulequalify=self.code_rules()
        self.calscale_id,self.calscalelookup_id=self.scale_rule()
        self.calrange_id,self.calmethod_id,self.rangestart=self.range()
        self.lookupvalue=self.lookup()
    
    def getffmcenter(self):
        cursor.execute("""select staddress_id from staddress inner join 
        storeentds on staddress.staddress_id=storeentds.staddress_id_loc 
        where storeentds.storeent_id=%s""",(self.store_id,))
        staddress_id=cursor.fetchone()[0]
        cursor.execute("select ffmcenter_id from ffmcentds where staddress_id=%s",(staddress_id,))
        ffmcenter_id=cursor.fetchone()[0]
        return staddress_id,ffmcenter_id

    def getcustomeraddress(self):
        cursor.execute("select address_id,city,state,country from address where member_id=%s",(self.customer_id,))
        res=cursor.fetchone()
        if res==None:return (None,None,None,None)
        elif res!=None:return res
    
    def getjurst(self):
        cursor.execute("select jurst_id from jurst where state=%s and country=%s",(self.customerstate,self.customercountry,))
        res=cursor.fetchall();jurstids=None;jurstgroupids=None
        if len(res) > 0:jurstids=[x for (x,) in res]
        elif len(res)<=0:jurstids=None
        cursor.execute("""select jurstgroup.jurstgroup_id from jurstgroup inner join jurstgprel on jurstgroup.jurstgroup_id=
        jurstgprel.jurstgroup_id where jurstgprel.jurst_id in %s""",(tuple(jurstids),));res=cursor.fetchall()
        if len(res)>0:jurstgroupids=[x for (x,) in res]
        elif len(res) <=0:jurstgroupids=None
        return jurstids,jurstgroupids

    def code_rules(self):
        cursor.execute("""select shpjcrule.calrule_id,calrule.calcode_id,calrule.calrule_id,calrule.calmethod_id,
        calrule.calmethod_id_qfy from shpjcrule inner join calrule on shpjcrule.calrule_id=calrule.calrule_id
        where shpjcrule.jurstgroup_id in %s and shpjcrule.ffmcenter_id=%s""",(tuple(self.jurstgroupids),
        self.ffmcenter_id,));res=cursor.fetchall()
        if len(res) <=0:return None
        elif len(res) > 0:return res[0]

    def scale_rule(self):
        cursor.execute("""select crulescale.calscale_id,calscale.calmethod_id from crulescale 
        inner join calscale on crulescale.calscale_id=calscale.calscale_id where crulescale.calrule_id=%s 
        and calscale.storeent_id=%s and calscale.calusage_id=%s""",(self.calrule_id,self.store_id,self.calusage_id,))
        res=cursor.fetchall()
        if len(res) <=0:return None
        elif len(res) > 0:return res[0]
    
    def range(self):
        cursor.execute("select calrange_id,calmethod_id,rangestart::float from calrange where calscale_id=%s",
        (self.calscale_id,));res=cursor.fetchall();crange=None
        if len(res)<=0:return None
        elif len(res) > 0:
            crange=[x for x in res if self.gross>=x[2]]
            if len(crange)>0:return crange[-1]
            return (None,None,None)
    
    def lookup(self):
        cursor.execute("select value::float from calrlookup where calrange_id=%s",(self.calrange_id,))
        res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]
