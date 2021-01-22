import psycopg2
def createcon(dbname,user,host,port):
    try:
        con=psycopg2.connect(database=dbname,user=user,password='f10aeb05',host=host,port=port)
    except:
        print('Unable to connect to the database')
    cursor=con.cursor()
    return con,cursor

con,cursor=createcon("retail","jmso","localhost","5432")
con.autocommit=True
