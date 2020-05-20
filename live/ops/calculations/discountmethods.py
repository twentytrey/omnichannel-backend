from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","pronov","localhost","5432")


class DiscountMethods:
    def __init__(self,calcode_id,catentry_id,price,quantity,store_id,trading_id=None):
        self.calcode_id=calcode_id
        self.catentry_id=catentry_id
        self.price=price
        self.quantity=quantity
        self.store_id=store_id
        self.trading_id=trading_id
        self.calusage_id=self.usage()

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
        elif res !=None:return res

    def get_finalize(self):
        cursor.execute("""select stencalusg.calmethod_id_fin,calmethod.taskname from stencalusg inner join calmethod on
        stencalusg.calmethod_id_fin=calmethod.calmethod_id where stencalusg.storeent_id=%s and stencalusg.calusage_id=%s""",
        (self.store_id,self.calusage_id,));res=cursor.fetchone()
        if res==None:return None
        elif res != None:return res
