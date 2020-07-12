import datetime,time,psycopg2,locale
from decimal import Decimal
BASE_URL="http://127.0.0.1:5000"
#BASE_URL="https://pronovapp.com"

def createcon(dbname,user,host,port):
    try:
        con=psycopg2.connect(database=dbname,user=user,password='f10aeb05',host=host,port=port)
    except:
        print('Unable to connect to the database')
    cursor=con.cursor()
    return con,cursor

con,cursor=createcon('retail','pronov','localhost','5432')

def timestamp_now():
    now=time.time()
    formatted=datetime.datetime.fromtimestamp(now).strftime("%Y-%m-%d ")
    return formatted

def datetimestamp_now():
    now=time.time()
    formatted=datetime.datetime.fromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S")
    return formatted

def todayplusdelta(delta):
    now=time.time()
    dnow=datetime.datetime.now()
    dt=dnow+datetime.timedelta(days=delta)
    return dt.strftime("%Y-%m-%d")

def timesplits():
    splits=datetimestamp_now().split(' ')
    l=splits[0].replace('-','')
    r=splits[1].replace(':','')
    return l+r[2:]

def timestamp_forever():
	forever=datetime.datetime.max
	formatted=forever.strftime("%Y-%m-%d")
	return formatted

def datetimestamp_forever():
	forever=datetime.datetime.max
	formatted=forever.strftime("%Y-%m-%d %H:%M:%S")
	return formatted

def defaultlanguage():
    cursor.execute("select language_id from languageds where description='English (Nigeria)'")
    return cursor.fetchone()[0]

def month(d):
    if d==None:return None
    else:return d.strftime("%b")

def humanize_date(d):
	if d==None:return None
	else:return d.strftime("%d %b, %Y")

def textualize_datetime(d):
	if d is None:return None
	else:return d.strftime("%Y-%m-%d %H:%M:%S")

def regularize(imageurl):
	if imageurl==None:return None
    # http://127.0.0.1:5000//static/profileuploads/paul-morris-116514-unsplash.jpg
    # http://127.0.0.1:5000//static/profileuploads/paul-morris-116514-unsplash.jpg
    # http://127.0.0.1:5000/static/profileuploads/paul-morris-116514-unsplash.jpg
	elif imageurl.startswith('static/'):return '{0}/{1}'.format(BASE_URL,imageurl)
	else:return imageurl

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
    
    def formatamount(self,amount):
        def f(d):return '{0:n}'.format(d)
        if amount==None:return f(Decimal(str(0.00)))
        else:return f(Decimal(str(amount)))

# c=CurrencyHelper(1)
# print(c.formatamount(2000))