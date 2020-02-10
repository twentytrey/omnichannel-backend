from .db_con import createcon
# from db_con import createcon
import psycopg2
con,cursor=createcon('retail','jmso','localhost','5432')
import pandas as pd
import numpy as np
import os

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Numbrusg:
    def __init__(self,numbrusg_id,code):
        self.numbrusg_id=numbrusg_id
        self.code=code
    
    def save(self):
        try:
            cursor.execute("""insert into numbrusg(numbrusg_id,code)values(%s,%s)on conflict(code)
            do update set numbrusg_id=%s,code=%s returning numbrusg_id""",(self.numbrusg_id,self.code,
            self.numbrusg_id,self.code,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split()[0])

class Numbrusgds:
    def __init__(self,numbrusg_id,language_id,description=None):
        self.numbrusg_id=numbrusg_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into numbrusgds(numbrusg_id,language_id,description)values(%s,%s,%s)
            on conflict(numbrusg_id,language_id)do update set numbrusg_id=%s,language_id=%s,description=%s
            returning numbrusg_id""",(self.numbrusg_id,self.language_id,self.description,self.numbrusg_id,
            self.language_id,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Curformat:
    def __init__(self,storeent_id,setccurr,roundingmultiple=1,numbrusg_id=0,roundingmethod='R',
    decimalplaces=2,minapproveammount=None):
        self.storeent_id=storeent_id
        self.setccurr=setccurr
        self.roundingmultiple=roundingmultiple
        self.numbrusg_id=numbrusg_id
        self.roundingmethod=roundingmethod
        self.decimalplaces=decimalplaces
        self.minapproveammount=minapproveammount
    
    def save(self):
        try:
            cursor.execute("""insert into curformat(storeent_id,setccurr,roundingmultiple,numbrusg_id,roundingmethod,decimalplaces,
            minapproveamount)values(%s,%s,%s,%s,%s,%s,%s)on conflict(storeent_id,setccurr,numbrusg_id)do update set
            storeent_id=%s,setccurr=%s,roundingmultiple=%s,numbrusg_id=%s,roundingmethod=%s,decimalplaces=%s,minapproveamount=%s
            returning numbrusg_id""",(self.storeent_id,self.setccurr,self.roundingmultiple,self.numbrusg_id,self.roundingmethod,self.decimalplaces,self.minapproveammount,
            self.storeent_id,self.setccurr,self.roundingmultiple,self.numbrusg_id,self.roundingmethod,self.decimalplaces,self.minapproveammount,))
            con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Curfmtdesc:
    def __init__(self,storeent_id,setccurr,language_id,numbrusg_id=0,currencysymbol=None,customizedcurrstr=None,
    currencyprefixpos=None,currencysuffixpos=None,displaylocale=None,currencyprefixneg=None,currencysuffixneg=None,
    radixpoint=None,groupingchar=None,numberpattern=None,description=None):
        self.storeent_id=storeent_id
        self.setccurr=setccurr
        self.language_id=language_id
        self.numbrusg_id=numbrusg_id
        self.currencysymbol=currencysymbol
        self.customizedcurrstr=customizedcurrstr
        self.currencyprefixpos=currencyprefixpos
        self.currencysuffixpos=currencysuffixpos
        self.displaylocale=displaylocale
        self.currencyprefixneg=currencyprefixneg
        self.currencysuffixneg=currencysuffixneg
        self.radixpoint=radixpoint
        self.groupingchar=groupingchar
        self.numberpattern=numberpattern
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into curfmtdesc(storeent_id,numbrusg_id,setccurr,language_id,currencysymbol,
            customizedcurrstr,currencyprefixpos,currencysuffixpos,displaylocale,currencyprefixneg,currencysuffixneg,
            radixpoint,groupingchar,numberpattern,description)values('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            on conflict(numbrusg_id,storeent_id,setccurr,language_id)do update set storeent_id=%s,numbrusg_id=%s,
            setccurr=%s,language_id=%s,currencysymbol=%s,customizedcurrstr=%s,currencyprefixpos=%s,currencysuffixpos=%s,
            displaylocale=%s,currencyprefixneg=%s,currencysuffixneg=%s,radixpoint=%s,groupingchar=%s,numberpattern=%s,
            description=%s returning numbrusg_id""",(self.storeent_id,self.numbrusg_id,self.setccurr,self.language_id,
            self.currencysymbol,self.customizedcurrstr,self.currencyprefixpos,self.currencysuffixpos,self.displaylocale,
            self.currencyprefixneg,self.currencysuffixneg,self.radixpoint,self.groupingchar,self.numberpattern,self.description,
            self.storeent_id,self.numbrusg_id,self.setccurr,self.language_id,
            self.currencysymbol,self.customizedcurrstr,self.currencyprefixpos,self.currencysuffixpos,self.displaylocale,
            self.currencyprefixneg,self.currencysuffixneg,self.radixpoint,self.groupingchar,self.numberpattern,self.description,))
            con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Setcurr:
    def __init__(self,setccurr,setccode,setcexp,setcnote):
        self.setccurr=setccurr
        self.setccode=setccode
        self.setcexp=setcexp
        self.setcnote=setcnote
    
    def save(self):
        try:
            cursor.execute("""insert into setcurr(setccurr,setccode,setcexp,setcnote)values(%s,%s,%s,%s)
            on conflict(setccurr)do update set setccurr=%s,setccode=%s,setcexp=%s,setcnote=%s returning
            setccurr""",(self.setccurr,self.setccode,self.setcexp,self.setcnote,self.setccurr,self.setccode,
            self.setcexp,self.setcnote,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Setcurrdsc:
    def __init__(self,setccurr,language_id,description=None):
        self.setccurr=setccurr
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into setcurrdsc(setccurr,language_id,description)values(%s,%s,%s)
            on conflict(setccurr,language_id)do update set setccurr=%s,language_id=%s,description=%s 
            returning setccurr""",(self.setccurr,self.language_id,self.description,self.setccurr,
            self.language_id,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Curconvert:
    def __init__(self,storeent_id,fromcurr,tocurr,factor=1,multiplyordivide='M',bidirectional='N',updatable='Y'):
        self.storeent_id=storeent_id
        self.fromcurr=fromcurr
        self.tocurr=tocurr
        self.factor=factor
        self.multiplyordivide=multiplyordivide
        self.bidirectional=bidirectional
        self.updatable=updatable
    
    def save(self):
        try:
            cursor.execute("""insert into curconvert(storeent_id,fromcurr,tocurr,factor,multiplyordivide,bidirectional,
            updatable)values(%s,%s,%s,%s,%s,%s,%s)on conflict(fromcurr,tocurr,storeent_id)do update set storeent_id=%s,
            fromcurr=%s,tocurr=%s,factor=%s,multiplyordivide=%s,bidirectional=%s,updatable=%s returning curconvert_id""",
            (self.storeent_id,self.fromcurr,self.tocurr,self.factor,self.multiplyordivide,self.bidirectional,
            self.updatable,self.storeent_id,self.fromcurr,self.tocurr,self.factor,self.multiplyordivide,self.bidirectional,
            self.updatable,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Curcvlist:
    def __init__(self,storeent_id,currstr,countervaluecurr,displayseq=0):
        self.storeent_id=storeent_id
        self.currstr=currstr
        self.countervaluecurr=countervaluecurr
        self.displayseq=displayseq
    
    def save(self):
        try:
            cursor.execute("""insert into curcvlist(storeent_id,currstr,countervaluecurr,displayseq)values(%s,%s,%s,%s)
            on conflict(countervaluecurr,currstr,storeent_id,displayseq)do update set storeent_id=%s,currstr=%s,
            countervaluecurr=%s,displayseq=%s returning currstr""",(self.storeent_id,self.currstr,self.countervaluecurr,
            self.displayseq,self.storeent_id,self.currstr,self.countervaluecurr,self.displayseq,));con.commit()
            return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Curlist:
    def __init__(self,storeent_id,currstr):
        self.storeent_id=storeent_id
        self.currstr=currstr
    
    def save(self):
        try:
            cursor.execute("""insert into curlist(storeent_id,currstr)values(%s,%s)on conflict(currstr,storeent_id)
            do update set storeent_id=%s,currstr=%s returning storeent_id""",(self.storeent_id,self.currstr,
            self.storeent_id,self.currstr,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class CurrencyDefaults:
    def __init__(self,fname):
        self.fname=fname
    
    def isfilled(self):
        cursor.execute("""select count(setcurr.setccurr)from setcurr left join setcurrdsc on
        setcurr.setccurr=setcurrdsc.setccurr""");res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False
    
    def defaultlang(self):
        cursor.execute("""select language_id from languageds where description='English (Nigeria)'""")
        return cursor.fetchone()[0]
    
    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl);df.dropna(subset=['MinorUnit'],inplace=True)
            df['MinorUnit'].replace('-',np.nan,inplace=True)
            df.dropna(subset=['MinorUnit'],inplace=True)
            df=df.astype({'MinorUnit':'int32'})
            df=df.astype({'NumericCode':'int32'})
            currencies=df.values[:,[2,3,4]]
            currencies=[np.append(n,None)for n in currencies]
            [Setcurr(*c).save() for c in currencies]
            df['language_id']=pd.Series([self.defaultlang()]*df.shape[0])
            df.dropna(subset=['language_id'],inplace=True)
            df=df.astype({'language_id':'int32'})
            descriptions=df.values[:,[2,6,1]]
            [Setcurrdsc(*d).save() for d in descriptions]

# print(CurrencyDefaults('allcurrencycodes.csv').isfilled())

class NumberUsageDefaults:
    def __init__(self,fname):
        self.fname=fname
    
    def isfilled(self):
        cursor.execute("""select count(numbrusg.numbrusg_id) from numbrusg left join numbrusgds on 
        numbrusg.numbrusg_id=numbrusgds.numbrusg_id""");res=cursor.fetchone()[0]
        if res > 0:return True
        elif res <= 0:return False
    
    def defaultlang(self):
        cursor.execute("select language_id from languageds where description='English (Nigeria)'")
        return cursor.fetchone()[0]

    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            df['language_id']=pd.Series([self.defaultlang()]*df.shape[0])
            usages=df.values[:,[0,1]];descriptions=df.values[:,[0,2,3]]
            [Numbrusg(*u).save() for u in usages]
            [Numbrusgds(*d).save() for d in descriptions]

# print(NumberUsageDefaults('numberusage.csv').isfilled())
