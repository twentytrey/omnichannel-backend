from db_con import createcon
con,cursor=createcon("jno","tiniraph","localhost","5432")
con.autocommit=True
from functions import build_constraint

class Currency:
    """the currency data model shows the relationship between database tables that contain
    information about currency within payments."""
    def curlist(self):
        "list of currencies supported by a store"
        cursor.execute("""create table curlist(
            storeent_id integer not null,
            currstr char(3)not null,
            primary key(currstr,storeent_id)
        )""")
        cursor.execute("create index i0000553 on curlist(storeent_id)")
        # CONSTRAINTS:
    
    def curconvert(self):
        """each row of this table represents a rule. the rule can be used to 
        convert a price (stored in the database in a particular currency)
        to an amount. the amount is what the customer will be charged in a
        supported shopping currency (the currency in which payment is accepted)"""
        cursor.execute("""create table curconvert(
            storeent_id integer not null,
            fromcurr char(3)not null,
            tocurr char(3)not null,
            factor decimal(31,20)not null default 1,
            multiplyordivide char(1)not null default 'M',
            bidirectional char(1)not null default 'N',
            updatable char(1)not null default 'Y',
            curconvert_id serial not null,
            primary key(curconvert_id)
        )""")
        cursor.execute("create unique index i0000083 on curconvert(fromcurr,tocurr,storeent_id)")
        cursor.execute("create index i0000551 on curconvert(storeent_id)")
        # CONSTRAINTS:
    
    def curformat(self):
        """each row of this table represents the language-dependent part of a 
        currency formatting rule. if a store has not formattin rule for a prticular
        currency, it uses the formattin rule of its store group."""
        cursor.execute("""create table curformat(
            storeent_id integer not null,
            setccurr char(3)not null,
            roundingmultiple integer not null default 1,
            numbrusg_id integer not null default 0,
            roundingmethod char(1)not null default 'R',
            decimalplaces integer not null default 2,
            minapproveamount decimal(20,5),
            primary key(storeent_id,setccurr,numbrusg_id)
        )""")
        # CONSTRAINTS:
    
    def curfmtdesc(self):
        """each row of this table represents the lang-dependent part of a currency
        formatting rule. it describes how to format (for display purposes)
        a monetary amount in a particular currency, in a partuicular language"""
        cursor.execute("""create table curfmtdesc(
            storeent_id integer not null,
            numbrusg_id integer not null default 0,
            setccurr char(3)not null,
            language_id integer not null,
            currencysymbol varchar(254),
            customizedcurrstr varchar(254),
            currencyprefixpos varchar(254),
            currencysuffixpos varchar(254),
            displaylocale char(16),
            currencyprefixneg varchar(254),
            currencysuffixneg varchar(254),
            radixpoint char(1),
            groupingchar char(1),
            numberpattern varchar(254),
            description varchar(254),
            primary key(numbrusg_id,storeent_id,setccurr,language_id)
        )""")
        cursor.execute("create index i0001254 on curfmtdesc(storeent_id,setccurr,numbrusg_id)")
        # CONSTRAINTS:
    
    def numbrusg(self):
        """each row defines a number usage object. numbers such as quantities and monetary
        amounts can be rounded and formatted differently depending on their associated
        number usage objects. the currency manager and quantity manager cache this information"""
        cursor.execute("""create table numbrusg(
            numbrusg_id integer not null,
            code char(60),
            primary key(numbrusg_id)
        )""")
        cursor.execute("create unique index i0000164 on numbrusg(code)")
    
    def numbrusgds(self):
        """each row of this table represents language-dependent information
        for a number usage. the table defines a usage of either a currency format
        or a quantity format.see the numbrusg tabnle also/."""
        cursor.execute("""create table numbrusgds(
            numbrusg_id integer not null,
            language_id integer not null,
            description varchar(254),
            primary key(numbrusg_id,language_id)
        )""")
        # CONSTRAINTS:
    
    def curcvlist(self):
        """each row represents a counter currency pair. the primary
        use of this information is for dual display of european monetary
        union monetary amounts/"""
        cursor.execute("""create table curcvlist(
            storeent_id integer not null,
            currstr char(3)not null,
            countervaluecurr char(3)not null,
            displayseq float not null default 0,
            primary key(countervaluecurr,currstr,storeent_id,displayseq)
        )""")
        cursor.execute("create index i0000552 on curcvlist(storeent_id)")
        # CONSTRAINTS:
    
    def setccurr(self):
        """this table contains information about the different
        national currencies. the currency alphabetic and numeric codes
        are derived from the ISO 4217 standard."""
        cursor.execute("""create table setcurr(
            setccurr char(3)not null,
            setccode integer not null,
            setcexp integer not null,
            setcnote varchar(40),
            primary key(setccurr)
        )""")
    
    def setcurrdsc(self):
        """stores the text descriptions for each currency in
        the setcurr table in a supported language."""
        cursor.execute("""create table setcurrdsc(
            setccurr char(3)not null,
            language_id integer not null,
            description varchar(254),
            primary key(setccurr,language_id)
        )""")
        # CONSTRAINTS

if __name__=="__main__":
    c=Currency()
    c.curlist()
    c.curconvert()
    c.curformat()
    c.curfmtdesc()
    c.numbrusg()
    c.numbrusgds()
    c.curcvlist()
    c.setccurr()
    c.setcurrdsc()