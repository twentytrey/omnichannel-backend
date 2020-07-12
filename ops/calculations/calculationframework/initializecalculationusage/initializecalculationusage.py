# from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
# con,cursor=createcon("retail","jmso","localhost","5432")
from ops.connector.connector import evcon
con,cursor=evcon()


class initializecalculationusage:
    def __init__(self):
        print( """initializecalculationusage""" )
