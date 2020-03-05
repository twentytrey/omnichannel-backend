import datetime,time,psycopg2,locale

def createcon(dbname,user,host,port):
    try:
        con=psycopg2.connect(database=dbname,user=user,password='f10aeb05',host=host,port=port)
    except:
        print('Unable to connect to the database')
    cursor=con.cursor()
    return con,cursor

con,cursor=createcon('retail','jmso','localhost','5432')

def timestamp_now():
    now=time.time()
    formatted=datetime.datetime.fromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S")
    return formatted

def timestamp_forever():
	forever=datetime.datetime.max
	formatted=forever.strftime("%Y-%m-%d %H:%M:%S")
	return formatted

def defaultlanguage():
    cursor.execute("select language_id from languageds where description='English (Nigeria)'")
    return cursor.fetchone()[0]

def humanize_date(d):
	if d==None:return None
	else:return d.strftime("%d %b, %Y")

def textualize_datetime(d):
	if d is None:return None
	else:return d.strftime("%Y-%m-%d %H:%M:%S")

class CurrencyHelper:
    def __init__(self,language_id):
        self.language_id=language_id
        self.localename=self.getlocalename()
        self.setlocalename()
        self.intsymbol=self.getintsymbol()
        self.currsymbol=self.getcurrsymbol()
    
    def getlocalename(self):
        cursor.execute("select localename::text from language where language_id=%s",(self.language_id,))
        localename=cursor.fetchone()[0];return localename
    
    def setlocalename(self):
        locale.setlocale(locale.LC_ALL,self.localename)
    
    def getintsymbol(self):
        return locale.localeconv()['int_curr_symbol']
    
    def getcurrsymbol(self):
        return locale.localeconv()['currency_symbol']

# c=CurrencyHelper(1)
# print(c.currsymbol)
# print(c.intsymbol)
