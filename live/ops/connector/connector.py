import psycopg2
def evcon():
    try:
        con=psycopg2.connect(database='retail',user='pronov',password='f10aeb05',host='localhost',port='5432')
        cursor=con.cursor()
        return con,cursor
    except Exception as e:
        raise Exception('Connection Error {}'.format(str(e).strip()))
