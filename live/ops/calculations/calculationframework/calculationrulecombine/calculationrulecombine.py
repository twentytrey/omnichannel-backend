# from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os,importlib
# con,cursor=createcon("retail","jmso","localhost","5432")
from ops.connector.connector import evcon
con,cursor=evcon()


class calculationrulecombine:
    def __init__(self,calcode_id,catentry_id,price,quantity,store_id):
        print("""calculationrulecombine""")
        self.calcode_id=calcode_id
        self.catentry_id=catentry_id
        self.price=price
        self.quantity=quantity
        self.store_id=store_id
        self.calrule_id,self.rulecalculate_id,self.rulequalify_id=self.getcalrulemethods()
        self.rulecalculate=self.gettaskname(self.rulecalculate_id)
        self.rulequalify=self.gettaskname(self.rulequalify_id)
        self.rulecalculate=self.getmodule("ops.calculations.{}".format(self.rulecalculate)).calculationrulecalculate
        self.rulequalify=self.getmodule("ops.calculations.{}".format(self.rulequalify)).discountcalculationrulequalify
        self.rulequalify();self.returns=self._execute()

    def _execute(self):
        return self.rulecalculate(self.calrule_id,self.calcode_id,self.catentry_id,self.price,self.quantity,
        self.store_id).returns

    def getmodule(self,taskname):
        module=importlib.import_module(taskname)
        return module

    def gettaskname(self,mid):
        cursor.execute("select taskname from calmethod where calmethod_id=%s",(mid,))
        res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res[0]

    def getcalrulemethods(self):
        cursor.execute("select calrule_id,calmethod_id,calmethod_id_qfy from calrule where calcode_id=%s",
        (self.calcode_id,));res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res
