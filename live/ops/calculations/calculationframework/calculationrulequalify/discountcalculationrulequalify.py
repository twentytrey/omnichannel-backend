# from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os,importlib
# con,cursor=createcon("retail","jmso","localhost","5432")
from ops.connector.connector import evcon
con,cursor=evcon()


class discountcalculationrulequalify:
    def __init__(self):
        print("""discountcalculationrulequalify""")


