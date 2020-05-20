from .db_con import createcon
# from db_con import createcon
import psycopg2,os
import pandas as pd
con,cursor=createcon('retail','pronov','localhost','5432')

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Qtyunit:
    def __init__(self,qtyunit_id,field1=None):
        self.qtyunit_id=qtyunit_id
        self.field1=field1
    
    def save(self):
        try:
            cursor.execute("""insert into qtyunit(qtyunit_id,field1)values(%s,%s)on conflict(qtyunit_id)
            do update set qtyunit_id=%s,field1=%s returning qtyunit_id""",(self.qtyunit_id,self.field1,
            self.qtyunit_id,self.field1,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Qtyunitdsc:
    def __init__(self,qtyunit_id,language_id,description=None):
        self.qtyunit_id=qtyunit_id
        self.language_id=language_id
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into qtyunitdsc(qtyunit_id,language_id,description)values(%s,%s,%s)
            on conflict(language_id,qtyunit_id)do update set qtyunit_id=%s,language_id=%s,description=%s
            returning qtyunit_id""",(self.qtyunit_id,self.language_id,self.description,self.qtyunit_id,
            self.language_id,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Qtyconvert:
    def __init__(self,qtyunit_id_to,qtyunit_id_from,factor,multiplyordivide,updatable):
        self.qtyunit_id_to=qtyunit_id_to
        self.qtyunit_id_from=qtyunit_id_from
        self.factor=factor
        self.multiplyordivide=multiplyordivide
        self.updatable=updatable
    
    def save(self):
        try:
            cursor.execute("""insert into qtyconvert(qtyunit_id_to,qtyunit_id_from,factor,multiplyordivide,updatable)
            values(%s,%s,%s,%s,%s)on conflict(qtyunit_id_to,qtyunit_id_from)do update set qtyunit_id_to=%s,qtyunit_id_from=%s,
            factor=%s,multiplyordivide=%s,updatable=%s returning qtyconvert_id""",(self.qtyunit_id_to,self.qtyunit_id_from,
            self.factor,self.multiplyordivide,self.updatable,self.qtyunit_id_to,self.qtyunit_id_from,self.factor,self.multiplyordivide,
            self.updatable,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Qtyformat:
    def __init__(self,storeent_id,qtyunit_id,roundingmultiple,numbrusg_id,roundingmethod,decimalplaces):
        self.storeent_id=storeent_id
        self.qtyunit_id=qtyunit_id
        self.roundingmultiple=roundingmultiple
        self.numbrusg_id=numbrusg_id
        self.roundingmethod=roundingmethod
        self.decimalplaces=decimalplaces
    
    def save(self):
        try:
            cursor.execute("""insert into qtyformat(storeent_id,qtyunit_id,roundingmultiple,numbrusg_id,roundingmethod,
            decimalplaces)values(%s,%s,%s,%s,%s,%s)on conflict(storeent_id,qtyunit_id,numbrusg_id)do update set
            storeent_id=%s,qtyunit_id=%s,roundingmultiple=%s,numbrusg_id=%s,roundingmethod=%s,decimalplaces=%s""",
            (self.storeent_id,self.qtyunit_id,self.roundingmultiple,self.numbrusg_id,self.roundingmethod,self.decimalplaces,
            self.storeent_id,self.qtyunit_id,self.roundingmultiple,self.numbrusg_id,self.roundingmethod,self.decimalplaces,))
            con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Qtyfmtdesc:
    def __init__(self,storeent_id,numbrusg_id,language_id,qtyunit_id,unitsymbol,unitprefixpos,unitsuffixpos,displaylocale,
    customizedqtystr,unitprefixneg,unitsuffixneg,radixpoint,groupingchar,numberpattern,description):
        self.storeent_id=storeent_id
        self.numbrusg_id=numbrusg_id
        self.language_id=language_id
        self.qtyunit_id=qtyunit_id
        self.unitsymbol=unitsymbol
        self.unitprefixpos=unitprefixpos
        self.unitsuffixpos=unitsuffixpos
        self.displaylocale=displaylocale
        self.customizedqtystr=customizedqtystr
        self.unitprefixneg=unitprefixneg
        self.unitsuffixneg=unitsuffixneg
        self.radixpoint=radixpoint
        self.groupingchar=groupingchar
        self.numberpattern=numberpattern
        self.description=description
    
    def save(self):
        try:
            cursor.execute("""insert into qtyfmtdesc(storeent_id,numbrusg_id,language_id,qtyunit_id,unitsymbol,unitprefixpos,
            unitsuffixpos,displaylocale,customizedqtystr,unitprefixneg,unitsuffixneg,radixpoint,groupingchar,numberpattern,
            description)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on conflict(numbrusg_id,storeent_id,qtyunit_id,language_id)
            do update set storeent_id=%s,numbrusg_id=%s,language_id=%s,qtyunit_id=%s,unitsymbol=%s,unitprefixpos=%s,
            unitsuffixpos=%s,displaylocale=%s,customizedqtystr=%s,unitprefixneg=%s,unitsuffixneg=%s,radixpoint=%s,groupingchar=%s,
            numberpattern=%s,description=%s""",(self.storeent_id,self.numbrusg_id,self.language_id,self.qtyunit_id,self.unitsymbol,self.unitprefixpos,
            self.unitsuffixpos,self.displaylocale,self.customizedqtystr,self.unitprefixneg,self.unitsuffixneg,self.radixpoint,self.groupingchar,
            self.numberpattern,self.description,
            self.storeent_id,self.numbrusg_id,self.language_id,self.qtyunit_id,self.unitsymbol,self.unitprefixpos,
            self.unitsuffixpos,self.displaylocale,self.customizedqtystr,self.unitprefixneg,self.unitsuffixneg,self.radixpoint,self.groupingchar,
            self.numberpattern,self.description,));con.commit();return cursor.fetchone()[0]
        except (Exception) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class InstallQtyunits:
    def __init__(self,fname):
        self.fname=fname
    
    def isfilled(self):
        cursor.execute("select count(qtyunit_id)from qtyunit")
        res=cursor.fetchone()[0]
        if res>0:return True
        elif res<=0:return False
    
    def save(self):
        basedir=os.path.abspath(os.path.dirname(__file__))
        fileurl=os.path.join(os.path.join(os.path.split(os.path.split(basedir)[0])[0],"static/datafiles"),self.fname)
        if os.path.isfile(fileurl):
            df=pd.read_csv(fileurl)
            units=df.values[:,[0,1]]
            descriptions=df.values[:,[0,2,3]]
            [Qtyunit(*u).save() for u in units]
            [Qtyunitdsc(*d).save() for d in descriptions]
            
