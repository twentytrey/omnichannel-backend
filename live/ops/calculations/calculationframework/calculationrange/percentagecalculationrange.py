from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os,importlib
con,cursor=createcon("retail","pronov","localhost","5432")

class percentagecalculationrange:
    def __init__(self,catentry_id,price,quantity,calrange_id):
        print("""percentagecalculationrange""")
        self.catentry_id=catentry_id
        self.quantity=quantity
        self.price=price
        self.calrange_id=calrange_id
        self.returns=self._execute()
    
    def _execute(self):
        cursor.execute("select value::float from calrlookup where calrange_id=%s order by calrlookup_id desc limit 1",
        (self.calrange_id,));res=cursor.fetchall();values=list()
        if len(res) <= 0:values=values
        elif len(res) > 0:values=[x for (x,) in res]
        return [ (x/100)*(self.quantity*self.price) for x in values ]
