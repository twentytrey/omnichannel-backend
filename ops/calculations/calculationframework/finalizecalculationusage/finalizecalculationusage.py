from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","jmso","localhost","5432")

class finalizecalculationusage:
    def __init__(self):
        print("""finalizecalculationusage""")

