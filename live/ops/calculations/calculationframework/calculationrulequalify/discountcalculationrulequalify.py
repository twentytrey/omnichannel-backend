from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os,importlib
con,cursor=createcon("retail","pronov","localhost","5432")

class discountcalculationrulequalify:
    def __init__(self):
        print("""discountcalculationrulequalify""")


