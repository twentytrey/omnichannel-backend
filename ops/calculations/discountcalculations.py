# from .db_con import createcon
from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","jmso","localhost","5432")
import  importlib
import pandas as pd
import numpy as np
# from ops import textualize_datetime,humanize_date

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class DiscountCalculations:
    def __init__(self,calcode_id,catentry_id,store_id,trading_id=None):
        self.catentry_id=catentry_id
        self.store_id=store_id
        self.trading_id=trading_id
        self.calcode_id=calcode_id
        self.calusage_id=self.usage()
        self.startdate=self.getstartdate()
        self.enddate=self.getenddate()

        self.initializecalculationusage=self.get_init()
        self.applycalculationusage=self.get_apply()
        self.calculationcodecombine=self.get_codecombine()
        self.calculationcodequalify=self.getcalmethod_qfy()
        self.calculationcodecalculate=self.getcalmethod()
        self.calculationrulecombine=self.get_rulecombine()
        self.calculationcodeapply=self.getcalmethod_app()
        self.summarizecalculationusage=self.get_summarize()
        self.finalizecalculationusage=self.get_finalize()

    def getstartdate(self):
        cursor.execute("select startdate from calcode where calcode_id=%s",(self.calcode_id,))
        res=cursor.fetchone()
        if res==None:return None
        elif res != None:return res[0]
    
    def getenddate(self):
        cursor.execute("select enddate from calcode where calcode_id=%s",(self.calcode_id,))
        res=cursor.fetchone()
        if res==None:return None
        elif res !=None:return res[0]
    
    def usage(self):
        cursor.execute("select calusage_id from calcode where calcode_id=%s and storeent_id=%s",
        (self.calcode_id,self.store_id,));res=cursor.fetchone()
        if res==None:return None
        elif res != None:return res[0]

    def get_init(self):
        cursor.execute("""select stencalusg.calmethod_id_ini,calmethod.taskname from stencalusg inner join
        calmethod on stencalusg.calmethod_id_ini=calmethod.calmethod_id where stencalusg.calusage_id=%s and 
        stencalusg.storeent_id=%s""",(self.calusage_id,self.store_id,));res=cursor.fetchone()
        if res==None:return None
        elif res != None:return res
    
    def get_apply(self):
        cursor.execute("""select stencalusg.calmethod_id_app,calmethod.taskname from stencalusg inner join
        calmethod on stencalusg.calmethod_id_app=calmethod.calmethod_id where stencalusg.calusage_id=%s and 
        stencalusg.storeent_id=%s""",(self.calusage_id,self.store_id,));res=cursor.fetchone()
        if res==None:return None
        elif res != None:return res
    
    def get_codecombine(self):
        cursor.execute("""select stencalusg.atcc_calmethod_id,calmethod.taskname from stencalusg inner join
        calmethod on stencalusg.atcc_calmethod_id=calmethod.calmethod_id where stencalusg.calusage_id=%s and
        stencalusg.storeent_id=%s""",(self.calusage_id,self.store_id,));res=cursor.fetchone()
        if res==None:return None
        elif res != None:return res

    def getcalmethod_qfy(self):
        cursor.execute("""select calcode.calmethod_id_qfy,calmethod.taskname from calcode inner join calmethod on
        calcode.calmethod_id_qfy=calmethod.calmethod_id where calcode.storeent_id=%s and calcode.calcode_id=%s""",
        (self.store_id,self.calcode_id,));res=cursor.fetchone()
        if res==None:return None
        elif res != None:return res

    def getcalmethod(self):
        cursor.execute("""select calcode.calmethod_id,calmethod.taskname from calcode inner join calmethod on
        calcode.calmethod_id=calmethod.calmethod_id where calcode.storeent_id=%s and calcode.calcode_id=%s""",
        (self.store_id,self.calcode_id,));res=cursor.fetchone()
        if res==None:return None
        elif res != None:return res

    def get_rulecombine(self):
        cursor.execute("""select stencalusg.atrc_calmethod_id,calmethod.taskname from stencalusg inner join
        calmethod on stencalusg.atrc_calmethod_id=calmethod.calmethod_id where stencalusg.calusage_id=%s and
        stencalusg.storeent_id=%s""",(self.calusage_id,self.store_id,));res=cursor.fetchone()
        if res==None:return None
        elif res != None:return res

    def getcalmethod_app(self):
        cursor.execute("""select calcode.calmethod_id_app,calmethod.taskname from calcode inner join calmethod on
        calcode.calmethod_id_app=calmethod.calmethod_id where calcode.storeent_id=%s and calcode.calcode_id=%s""",
        (self.store_id,self.calcode_id,));res=cursor.fetchone()
        if res==None:return None
        elif res != None:return res

    def get_summarize(self):
        cursor.execute("""select stencalusg.calmethod_id_sum,calmethod.taskname from stencalusg inner join calmethod on
        stencalusg.calmethod_id_sum=calmethod.calmethod_id where stencalusg.storeent_id=%s and stencalusg.calusage_id=%s""",
        (self.store_id,self.calusage_id,));res=cursor.fetchone()
        if res==None:return None
        elif res !=None:return res[0]
    
    def get_finalize(self):
        cursor.execute("""select stencalusg.calmethod_id_fin,calmethod.taskname from stencalusg inner join calmethod on
        stencalusg.calmethod_id_fin=calmethod.calmethod_id where stencalusg.storeent_id=%s and stencalusg.calusage_id=%s""",
        (self.store_id,self.calusage_id,));res=cursor.fetchone()
        if res==None:return None
        elif res != None:return res[0]
    
    def getmodule(self,taskname):
        module=importlib.import_module(taskname)
        return module
    
    def _execute(self):
        # INITIALIZEUSAGE
        initializeusage=self.getmodule(self.initializecalculationusage[1])
        initializeusage.initializecalculationusage()

        # CODECOMBINATION
        codecombination=self.getmodule(self.calculationcodecombine[1]).calculationcodecombine
        # CODEQUALIFICATION
        # codequalification=self.getmodule(self.calculationcodequalify[1]).calculationcodequalify
        # CODECALCULATION
        # codecalculation=self.getmodule(self.calculationcodecalculate[1]).calculationcodecalculate
        # RULECOMBINATION
        # rulecombination=self.getmodule(self.calculationrulecombine[1]).calculationrulecombine

        # APPLYUSAGE
        applycalculationusage=self.getmodule(self.applycalculationusage[1])
        applycalculationusage.applycalculationusage(codecombination,self.calusage_id,self.catentry_id,self.calcode_id,self.store_id,self.trading_id)

# d=DiscountCalculations(3,9,1,20)
# d._execute()

# modstring='calculationframework.initializecalculationusage.initializecalculationusage'
# mod=importlib.import_module(modstring)
# print(mod)

