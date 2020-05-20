from db_con import createcon
con,cursor=createcon("retail","pronov","localhost","5432")
con.autocommit=True
from functions import build_constraint

class QuantityUnit:
    """the quantity unit data model shows the relationship
    between database tables that contain information about quantity units"""
    def qtyunit(self):
        """each row of this table represents a quantity unit.
        a quantity unit is a unit of measurement such as kilogram,meter,
        liter,pound,foot,quart and so on. do not remove the row for the default qtyunit_id
        C62 - the unitless unit"""
        cursor.execute("""create table qtyunit(
            qtyunit_id char(16)not null,
            field1 varchar(254),
            primary key(qtyunit_id)
        )""")
    
    def qtyunitdsc(self):
        cursor.execute("""create table qtyunitdsc(
            qtyunit_id char(16)not null,
            language_id integer not null,
            description varchar(512),
            primary key(language_id,qtyunit_id)
        )""")
        # CONSTRAINT
    
    def qtyconvert(self):
        """each row of this table represents a rule. it can be used to convert
        a quantity amount from one quantity unit to another"""
        cursor.execute("""create table qtyconvert(
            qtyunit_id_to char(16)not null,
            qtyconvert_id serial not null,
            qtyunit_id_from char(16)not null,
            factor decimal(31,20)not null,
            multiplyordivide char(1)not null,
            updatable char(1)not null,
            primary key(qtyconvert_id)
        )""")
        cursor.execute("create unique index i0000198 on qtyconvert(qtyunit_id_to,qtyunit_id_from)")
        # CONSTRAINT
    
    def qtyformat(self):
        """each row of this table represents the lang-independent part of
        a qtyunit formatting rule. if a store has no formatting rule for a 
        particular qyuantity unit, ut uses the formatting rule for its storegroup."""
        cursor.execute("""create table qtyformat(
            storeent_id integer not null,
            qtyunit_id char(16)not null,
            roundingmultiple integer not null,
            numbrusg_id integer not null default -1,
            roundingmethod char(1)not null,
            decimalplaces integer not null,
            primary key(storeent_id,qtyunit_id,numbrusg_id)
        )""")
    
    def qtyfmtdesc(self):
        """each row of this table represents the language-dependent part of 
        a quantityunit formatting rule. it describes how to format
        for display purposes, a quantity amount in a partiocular qyuantity unit in a particular language"""
        cursor.execute("""create table qtyfmtdesc(
            storeent_id integer not null,
            numbrusg_id integer not null default -1,
            language_id integer not null,
            qtyunit_id char(16)not null,
            unitsymbol varchar(254),
            unitprefixpos varchar(254),
            unitsuffixpos varchar(254),
            displaylocale char(16),
            customizedqtystr varchar(254),
            unitprefixneg varchar(254),
            unitsuffixneg varchar(254),
            radixpoint char(1),
            groupingchar char(1),
            numberpattern varchar(254),
            description varchar(254),
            primary key(numbrusg_id,storeent_id,qtyunit_id,language_id)
        )""")
        cursor.execute("create index i0001274 on qtyfmtdesc(storeent_id,qtyunit_id,numbrusg_id)")
        # CONSTRAINT
    
    def numbrusg(self):
        """each row defines a number usage object. numbers such as quantities and montary amounts
        can be rounded and formatted differently depending on their associated numberusage
        objects. the currency manager and quantity manager cache this information"""
        cursor.execute("""create table numbrusg(
            numbrusg_id integer not null,
            code char(60),
            primary key(numbrusg_id)
        )""")
        cursor.execute("create index i0000164 on numbrusg(code)")
    
    def numbrusgds(self):
        cursor.execute("""create table numbrusgds(
            numbrusg_id integer not null,
            language_id integer not null,
            description varchar(254),
            primary key(numbrusg_id,language_id)
        )""")

    def qtyunitmap(self):
        """each row of this table maps a quantityunit defined in the qtyunit table to a unit of measurement
        code defined in an external standard"""
        cursor.execute("""create table qtyunitmap(
            uomstandard varchar(32)not null,
            uomcode varchar(16)not null,
            qtyunit_id char(16)not null,
            field1 varchar(254),
            primary key(uomstandard,uomcode)
        )""")
        cursor.execute("create unique index i0000199 on qtyunitmap(qtyunit_id,uomstandard)")
        # CONSTRAINT

if __name__=="__main__":
    q=QuantityUnit()
    q.qtyconvert()
    q.qtyfmtdesc()
    q.qtyformat()
    q.qtyunit()
    q.qtyunitdsc()
    q.qtyunitmap()
