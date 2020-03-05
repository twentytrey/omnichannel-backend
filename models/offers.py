from db_con import createcon
con,cursor=createcon("retail","jmso","localhost","5432")
con.autocommit=True
from functions import build_constraint

class Offers:
    """the offers data model shows the relationship between database tables
    containing information about offers for trading positions."""
    def offer(self):
        """each row of this table represents an offer to sell 
        a product identified by a catalog entry."""
        cursor.execute("""create table offer(
            offer_id bigserial not null,
            startdate timestamp,
            tradeposcn_id bigint not null,
            catentry_id bigint not null,
            enddate timestamp,
            precedence float not null default 0,
            published integer not null default 0,
            lastupdate timestamp,
            minimumquantity float,
            qtyunit_id char(16),
            maximumquantity float,
            field1 char(30),
            field2 char(1),
            flags integer not null default 1,
            identifier bigint,
            primary key(offer_id)
        )""")
        cursor.execute("create unique index i0000165 on offer(catentry_id,identifier,tradeposcn_id)")
        cursor.execute("create index i0000167 on offer(catentry_id,published,tradeposcn_id)")
        cursor.execute("create index i0000626 on offer(tradeposcn_id)")
        # CONSTRAINTS
    
    def offerprice(self):
        """each row of this table represents
        a price in a currency for an offer"""
        cursor.execute("""create table offerprice(
            offer_id bigint not null,
            currency char(3)not null,
            price decimal(20,5)not null,
            compareprice decimal(20,5),
            primary key(offer_id,currency)
        )""")
        cursor.execute("create index i0000168 on offerprice(price,currency,offer_id)")
        # CONSTRAINTS
    
    def offerdesc(self):
        """each row of this table contains lang-
        dependent information for an offer."""
        cursor.execute("""create table offerdesc(
            offer_id bigint not null,
            language_id integer not null,
            description varchar(512),
            primary key(offer_id,language_id)
        )""")
        # CONSTRAINTS
    
    def mgptrdpscn(self):
        cursor.execute("""create table mgptrdpscn(
            mbrgrp_id bigint not null,
            tradeposcn_id bigint not null,
            primary key(tradeposcn_id,mbrgrp_id)
        )""")
        cursor.execute("create index i0000620 on mgptrdpscn(mbrgrp_id)")
        # CONSTRAINTS
    
    def ordioffer(self):
        """each row of this table indicates an offer that was searched
        to obtain the price for an orderitem. these rows are created by
        the orderitem add and order item update commands."""
        cursor.execute("""create table ordioffer(
            offer_id bigint not null,
            orderitems_id bigint not null,
            primary key(orderitems_id,offer_id)
        )""")
        cursor.execute("create index i0000658 on ordioffer(offer_id)")
        # CONSTRAINTS

if __name__=="__main__":
    o=Offers()
    o.offer()
    o.offerprice()
    o.offerdesc()
    o.mgptrdpscn()
    o.ordioffer()
