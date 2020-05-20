from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os,importlib,inspect
con,cursor=createcon("retail","pronov","localhost","5432")

class calculationrulecalculate:
    def __init__(self,calrule_id,calcode_id,catentry_id,price,quantity,storeent_id):
        print("""calculationrulecalculate""")
        self.calrule_id=calrule_id
        self.calcode_id=calcode_id
        self.catentry_id=catentry_id
        self.price=price
        self.quantity=quantity
        self.storeent_id=storeent_id
        self.returns=self._execute()

    def getmodule(self,taskname):
        module=importlib.import_module(taskname)
        return module

    def getlookupmethod(self,scale_id):
        cursor.execute("""select calmethod.taskname from calmethod inner join calscale on calmethod.
        calmethod_id=calscale.calmethod_id where calscale.calscale_id=%s and calscale.storeent_id=%s""",
        (scale_id,self.storeent_id,));res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]

    def executetaskname(self,taskname,scale_id):
        mod=self.getmodule("ops.calculations.{}".format(taskname))
        lookupmethod=mod.nondiscountedpricecalculationscalelookup
        l=lookupmethod(self.calrule_id,self.calcode_id,self.catentry_id,self.price,self.quantity,self.storeent_id,scale_id)
        return l.returns

    def _execute(self):
        cursor.execute("select calscale_id from crulescale where calrule_id=%s",(self.calrule_id,))
        res=cursor.fetchone();scale_id=None
        if res==None:scale_id=res
        elif res!=None:scale_id=res[0]
        taskname=self.getlookupmethod(scale_id)
        return self.executetaskname(taskname,scale_id)
