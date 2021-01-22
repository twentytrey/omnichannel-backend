# from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os,importlib
# con,cursor=createcon("retail","jmso","localhost","5432")
from ops.connector.connector import evcon
con,cursor=evcon()


class nondiscountedpricecalculationscalelookup:
    def __init__(self,calrule_id,calcode_id,catentry_id,price,quantity,storeent_id,calscale_id):
        print("""nondiscountedpricecalculationscalelookup""")
        self.calrule_id=calrule_id
        self.calcode_id=calcode_id
        self.catentry_id=catentry_id
        self.price=price
        self.quantity=quantity
        self.storeent_id=storeent_id
        self.calscale_id=calscale_id
        self.calrange_id,self.taskname,self.calmethod_id,self.rangestart=self.getcalrange()
        self.returns=self._execute()
    
    def _execute(self):
        mod=self.getmodule("ops.calculations.{}".format(self.taskname))
        rangemet=mod.percentagecalculationrange
        if self.quantity*self.price >= self.rangestart:
            return rangemet(self.catentry_id,self.price,self.quantity,self.calrange_id).returns

    def getmodule(self,taskname):
        module=importlib.import_module(taskname)
        return module
    
    def getcalrange(self):
        cursor.execute("""select calrange.calrange_id,calmethod.taskname,calrange.calmethod_id,calrange.rangestart::float 
        from calrange inner join calmethod on calrange.calmethod_id=calmethod.calmethod_id where calrange.calscale_id=%s""",
        (self.calscale_id,));res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res

