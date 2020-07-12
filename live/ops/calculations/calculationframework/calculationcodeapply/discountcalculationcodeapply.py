from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","pronov","localhost","5432")

class discountcalculationcodeapply:
    def __init__(self,amounts):
        print("""discountcalculationcodeapply""")
        self.amounts=amounts

    def _execute(self):return sum(self.amounts)
