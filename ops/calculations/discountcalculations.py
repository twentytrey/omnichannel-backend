from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","jmso","localhost","5432")
import  importlib
import pandas as pd
import numpy as np
import datetime
from ops.calculations.discountmethods import DiscountMethods

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class DiscountCalculations:
    def __init__(self,calcode_id,catentry_id,price,quantity,store_id,trading_id=None):
        self.catentry_id=catentry_id
        self.price=price
        self.quantity=quantity
        self.store_id=store_id
        self.trading_id=trading_id
        self.calcode_id=calcode_id
        self.startdate=self.getstartdate()
        self.enddate=self.getenddate()

        dmethods=DiscountMethods(calcode_id,catentry_id,price,quantity,store_id,trading_id)
        self.calusage_id=dmethods.usage()

        self.initializecalculationusage=dmethods.get_init()
        self.applycalculationusage=dmethods.get_apply()
        self.calculationcodecombine=dmethods.get_codecombine()
        self.calculationcodequalify=dmethods.getcalmethod_qfy()
        self.calculationcodecalculate=dmethods.getcalmethod()
        self.calculationrulecombine=dmethods.get_rulecombine()
        self.calculationcodeapply=dmethods.getcalmethod_app()
        self.summarizecalculationusage=dmethods.get_summarize()
        self.finalizecalculationusage=dmethods.get_finalize()

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
    
    def getmodule(self,taskname):
        module=importlib.import_module(taskname)
        return module
    
    def _execute(self):
        init=self.getmodule("ops.calculations.{}".format(self.initializecalculationusage[1]))
        init.initializecalculationusage()

        codecombine=self.getmodule("ops.calculations.{}".format(self.calculationcodecombine[1]))
        codecombine=codecombine.calculationcodecombine

        codecalculate=self.getmodule("ops.calculations.{}".format(self.calculationcodecalculate[1]))
        codecalculate=codecalculate.calculationcodecalculate

        rulecombine=self.getmodule("ops.calculations.{}".format(self.calculationrulecombine[1]))
        rulecombine=rulecombine.calculationrulecombine

        codeapply=self.getmodule("ops.calculations.{}".format(self.calculationcodeapply[1]))
        codeapply=codeapply.discountcalculationcodeapply

        summarize=self.getmodule("ops.calculations.{}".format(self.summarizecalculationusage[1]))
        summarize=summarize.summarizecalculationusage

        finalize=self.getmodule("ops.calculations.{}".format(self.finalizecalculationusage[1]))
        finalize=finalize.finalizecalculationusage

        app=self.getmodule("ops.calculations.{}".format(self.applycalculationusage[1]))
        return app.applycalculationusage(self.calcode_id,self.catentry_id,self.price,self.quantity,self.store_id,
        codecombine,codecalculate,rulecombine,codeapply,summarize,finalize).amount
