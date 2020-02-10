from db_con import createcon
con,cursor=createcon("jno","tiniraph","localhost","5432")
con.autocommit=True
from functions import build_constraint

class Pricing:
    """the pricing data model shows the relationship between database tables
    that contain information about pricing."""
    def dkpdcrel(self):
        "stores the complet structure of a predefined nested dkit"
        cursor.execute("""create table dkpdcrel(
            dkpdcrel_id bigserial not null,
            dkpredefconf_id bigint not null,
            catentry_id bigint not null,
            parent_id bigint,
            primary key(dkpdcrel_id)
        )""")
        cursor.execute("create index i0000412 on dkpdcrel(parent_id)")
        cursor.execute("create index i0000543 on dkpdcrel(dkpredefconf_id)")
        cursor.execute("create index i0000544 on dkpdcrel(catentry_id)")
        # CONSTRAINT
    
    def dkpdcofferrel(self):
        """contains relationships between predefined configurations
        and the offers that price them"""
        cursor.execute("""create table dkpdcofferrel(
            dkpredefconf_id bigint not null,
            offer_id bigint not null,
            primary key(dkpredefconf_id)
        )""")
        cursor.execute("create index i0000917 on dkpdcofferrel(offer_id)")
        # CONSTRAINTS
    
    def dkpdcdesc(self):
        "contains the description of predefined configurations"
        cursor.execute("""create table dkpdcdesc(
            dkpredefconf_id bigint not null,
            language_id integer not null,
            name varchar(254)not null,
            shortdescription varchar(254),
            longdescription text,
            primary key(dkpredefconf_id,language_id)
        )""")
        # CONSTRAINT
    
    def dkoffer(self):
        "stores prices of components within a dynamic kit"
        cursor.execute("""create table dkoffer(
            dkoffer_id bigserial not null,
            tradeposcn_id bigint not null,
            kit_id bigint not null,
            catentry_id bigint not null,
            currency char(3)not null,
            identifier bigint,
            price decimal(20,5)not null,
            startdate timestamp,
            enddate timestamp,
            minimumquantity float,
            maximumquantity float,
            precedence float not null default 0,
            published integer not null default 1,
            field1 char(30),
            field2 char(1),
            primary key(dkoffer_id)
        )""")
        cursor.execute("create unique index i0000932 on dkoffer(tradeposcn_id,kit_id,catentry_id,currency,identifier)")
        cursor.execute("create index i0000903 on dkoffer(kit_id)")
        cursor.execute("create index i0000904 on dkoffer(catentry_id)")
        cursor.execute("create index i0000905 on dkoffer(currency)")
        # CONSTRAINT
    
    def dkadjmnt(self):
        "stores adjustments to components within a dynamic kit"
        cursor.execute("""create table dkadjmnt(
            termcond_id bigint not null,
            kit_id bigint not null,
            catentry_id bigint not null,
            adjustment decimal(20,5)not null default 0,
            adjtype integer not null default 0,
            primary key(termcond_id,kit_id,catentry_id)
        )""")
        cursor.execute("create index i0000906 on dkadjmnt(kit_id)")
        cursor.execute("create index i0000907 on dkadjmnt(catentry_id)")
        # CONSTRAINT
    
    def pricerule(self):
        """each row of this table represents"""
        cursor.execute("""create table pricerule(
            pricerule_id bigserial not null,
            storeent_id integer not null,
            identifier varchar(254)not null,
            description varchar(512),
            version float,
            state smallint not null default 0,
            createtime timestamp,
            lastupdatetime timestamp,
            dependent smallint not null default 0,
            type smallint not null default 0,
            starttime timestamp,
            endtime timestamp,
            field1 varchar(254),
            field2 varchar(254),
            field3 varchar(254),
            markfordelete integer not null default 0,
            primary key(pricerule_id)
        )""")
        cursor.execute("create unique index i0001340 on pricerule(identifier,storeent_id)")
        cursor.execute("create index i0001341 on pricerule(storeent_id)")
        cursor.execute("create index i0001342 on pricerule(type)")
        # CONSTRAINT
    
    def storetpc(self):
        "the relationship between store entity and trading position container"
        cursor.execute("""create table storetpc(
            storeent_id integer not null,
            tradeposcn_id bigint not null,
            sttpcusg_id integer not null,
            primary key(storeent_id,tradeposcn_id,sttpcusg_id)
        )""")
        cursor.execute("create index i0001357 on storetpc(tradeposcn_id)")
        cursor.execute("create index i0001388 on storetpc(sttpcusg_id)")
        # CONSTRAINT
    
    def sttpcusg(self):
        "the usage tpes of a trading position contain for a store entity"
        cursor.execute("""create table sttpcusg(
            sttpcusg_id serial not null,
            identifier varchar(254)not null,
            description varchar(254),
            primary key(sttpcusg_id)
        )""")
    
    def prconstant(self):
        """each row of this table represents a price constant. price constant
        is a reusable number or monetary value with a name indicating its business
        meaning. for example, a constant 'UPlift for EU countries' is used to inc-
        rease prices in EU countries."""
        cursor.execute("""create table prconstant(
            prconstant_id bigserial not null,
            storeent_id integer not null,
            identifier varchar(254)not null,
            description varchar(254),
            type integer not null default 0,
            createtime timestamp,
            lastupdatetime timestamp,
            markfordelete integer not null default 0,
            primary key(prconstant_id)
        )""")
        cursor.execute("create unique index i0001351 on prconstant(identifier,storeent_id)")
        cursor.execute("create index i0001352 on prconstant(storeent_id)")
        cursor.execute("create index i0001353 on prconstant(type)")
        # CONSTRAINT
    
    def prconvalue(self):
        """each row of this table represents a price constant value.
        price constant value could be a number or monetary amount."""
        cursor.execute("""create table prconvalue(
            prconstant_id bigint not null,
            currency char(3)not null,
            value decimal(20,5)not null,
            primary key(prconstant_id,currency)
        )""")
        # CONSTRAINT
    
    def prequation(self):
        """each row of this table represents a price equation. price equation
        is an expression for price calculation. the parameters used in the equation
        can include input price, price lists, price constants etc. for example, the equation
        'input price + distribution cost' means the final price will be the sum of the 
        input price and distribution cost. """
        cursor.execute("""create table prequation(
            prequation_id bigserial not null,
            storeent_id integer not null,
            identifier varchar(254)not null,
            description varchar(512),
            value varchar(1024),
            createtime timestamp,
            lastupdate timestamp,
            markfordelete integer not null default 0,
            primary key(prequation_id)
        )""")
        cursor.execute("create unique index i0001349 on prequation(identifier,storeent_id)")
        cursor.execute("create index i0001350 on prequation(storeent_id)")
        # CONSTRAINT
    
    def preqentry(self):
        """each row of this table represents an equation entry (unit)for an equation
        multiple equation entries function together to compose an equation.
        for example the equation 'master price list * 0.5' is composed of 3 equation
        entries: 'master price list', '*', '0.5' """
        cursor.execute("""create table preqentry(
            preqentry_id bigserial not null,
            prequation_id bigint not null,
            preqentrytype_id bigint not null,
            value varchar(254),
            sequence float not null,
            primary key(preqentry_id)
        )""")
        cursor.execute("create index i0001359 on preqentry(prequation_id)")
        cursor.execute("create index i0001385 on preqentry(preqentrytype_id)")
        # CONSTRAINT
    
    def preqentrytype(self):
        """each row of this table represents an equation entry type. currently, there are
        the following types: PriceList,Operator,Number,PriceConstant,InputType"""
        cursor.execute("""create table preqentrytype(
            preqentrytype_id bigserial not null,
            identifier varchar(254)not null,
            description varchar(512),
            properties varchar(512),
            primary key(preqentrytype_id)
        )""")
        cursor.execute("create unique index i0001386 on preqentrytype(identifier)")
    
    def prelement(self):
        """each row of this table represents a price rule element.
        multiple elements function together to determine the flow of a price
        rule. for example, a price cule element could be price list,equation,branch and coordinator"""
        cursor.execute("""create table prelement(
            prelement_id bigserial not null,
            identifier varchar(254)not null,
            description varchar(512),
            preletemplate_id bigint not null,
            pricerule_id bigint not null,
            parent varchar(254),
            sequence float not null default 0,
            field1 varchar(254),
            field2 varchar(254),
            field3 varchar(254),
            primary key(prelement_id)
        )""")
        cursor.execute("create unique index i0001345 on prelement(identifier,pricerule_id)")
        cursor.execute("create index i0001346 on prelement(preletemplate_id,pricerule_id)")
        cursor.execute("create index i0001347 on prelement(pricerule_id)")
        # CONSTRAINT
    
    def prelementattr(self):
        """each row of this table represents a price rule attribute. a price rule attribute
        is a name-value pair used for price rule evaluation at runtime. for example, the element
        of pricelist type may have an attribute with the name pricelistid and the value 1001"""
        cursor.execute("""create table prelementattr(
            prelement_id bigint not null,
            name varchar(254)not null,
            value varchar(254)not null,
            properties varchar(254),
            sequence float,
            primary key(prelement_id,name,value)
        )""")
        cursor.execute("create index i0001348 on prelementattr(name,value)")
        # CONSTRAINT
    
    def preletemplate(self):
        """each row o this table represents a price rule element template.
        elements whoch share the same template use the same element command
        but different parameters for pricer rule evaluation at runtime. for example, customer
        segment condition is an element template"""
        cursor.execute("""create table preletemplate(
            preletemplate_id bigserial not null,
            identifier varchar(254)not null,
            storeent_id integer,
            description varchar(254),
            preletpltgrp_id bigint not null,
            runtimedata text,
            field1 varchar(254),
            field2 varchar(254),
            field3 varchar(254),
            primary key(preletemplate_id)
        )""")
        cursor.execute("create unique index i0001343 on preletemplate(preletpltgrp_id,identifier,storeent_id)")
        cursor.execute("create index i0001344 on preletemplate(storeent_id)")
        # CONSTRAINT
    
    def preletpltgrp(self):
        """each row of this table represents a price rule element template group.
        an element template group includes one or more element templates which have similar
        attributes and behaviors. for example, both category condition and customer segment
        condition are under the same template group (condition)"""
        cursor.execute("""create table preletpltgrp(
            preletpltgrp_id bigserial not null,
            identifier varchar(254)not null,
            description varchar(512),
            primary key(preletpltgrp_id)
        )""")

if __name__=="__main__":
    p=Pricing()
    p.dkadjmnt()
    p.dkoffer()
    p.dkpdcdesc()
    p.dkpdcofferrel()
    p.dkpdcrel()
    p.prconstant()
    p.prconvalue()
    p.prelement()
    p.prelementattr()
    p.preletemplate()
    p.preletpltgrp()
    p.preqentry()
    p.preqentrytype()
    p.prequation()
    p.pricerule()
    p.storetpc()
    p.sttpcusg()
