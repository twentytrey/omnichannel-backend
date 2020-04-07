from db_con import createcon
con,cursor=createcon("retail","jmso","localhost","5432")
con.autocommit=True
from functions import build_constraint

class Tax:
    """the tax type and category data model shows the relationship
    between database tables that contain information about categories
    and types of taxes."""
    def taxtype(self):
        """the table represents a taxtype. for example, sales tax
        and shipping tax are two types of taxes."""
        cursor.execute("""create table taxtype(
            taxtype_id integer not null,
            txcdscheme_id integer,
            sequence float not null default 0,
            primary key(taxtype_id)
        )""")
        cursor.execute("create index i0000344 on taxtype(txcdscheme_id,taxtype_id)")
        # CONSTRAINTS
    
    def txcdclass(self):
        """each row in this table represents a tax classification.
        a tax classification is a group of tax calculation codes"""
        cursor.execute("""create table txcdclass(
            txcdclass_id serial not null,
            name varchar(254),
            txcdscheme_id integer,
            description varchar(254),
            storeent_id integer not null,
            primary key(txcdclass_id)
        )""")
        cursor.execute("create unique index i0000258 on txcdclass(storeent_id,name)")
        # CONSTRAINT
    
    def txcdscheme(self):
        """each row in this table represents a tax code scheme. a tax code scheme
        is a set of taxcode classifications of calculation codes of particular tax types"""
        cursor.execute("""create table txcdscheme(
            txcdscheme_id serial not null,
            description varchar(254),
            vendor varchar(32),
            software varchar(32),
            primary key(txcdscheme_id)
        )""")
        cursor.execute("create unique index i0000259 on txcdscheme(vendor,software)")
    
    def taxcgryds(self):
        cursor.execute("""create table taxcgryds(
            language_id integer not null,
            taxcgry_id integer not null,
            description varchar(254),
            primary key(language_id,taxcgry_id)
        )""")
        cursor.execute("create index i0000804 on taxcgryds(taxcgry_id)")
        # CONSTRAINT

if __name__=="__main__":
    t=Tax()
    t.taxtype()
    #NOTE drop the previous implementation of the taxtype table - it has a useless name column and index
    t.txcdclass()
    t.txcdscheme()
    t.taxcgryds()
