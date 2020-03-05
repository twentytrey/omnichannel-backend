from db_con import createcon
con,cursor=createcon("retail","jmso","localhost","5432")
con.autocommit=True
from functions import build_constraint

class Shipping:
    """the shipping data model shows the relationship between database tables
    that contain information about shipping."""
    def shipmodedsc(self):
        cursor.execute("""create table shipmodedsc(
            shipmode_id integer not null,
            language_id integer not null,
            description varchar(254),
            field1 varchar(254),
            field2 varchar(254),
            primary key(shipmode_id,language_id)
        )""")
    
    def shipmode(self):
        """each row of this table represents a shippingmode for a storeentity
        a store can use its own shippingmodes and the shippingmodes of its storegroup."""
        cursor.execute("""create table shipmode(
            shipmode_id serial not null,
            field1 varchar(254),
            storeent_id integer not null,
            field2 integer,
            code char(60),
            carrier char(60),
            trackingname varchar(254),
            trackingurl varchar(254),
            trackinghost varchar(254),
            trackingport integer,
            trackingicon varchar(254),
            trackingtype char(8),
            markfordelete integer not null default 0,
            primary key(shipmode_id)
        )""")
        cursor.execute("create unique index i0000228 on shipmode(storeent_id,code,carrier)")
        # CONSTRAINT
    
    def shparrange(self):
        """each row of this table represents a shipping arrangement.
        indicating that a ffmcenter can ship products on behalf of a store
        using a shipping mode"""
        cursor.execute("""create table shparrange(
            shparrange_id serial not null,
            store_id integer not null,
            ffmcenter_id integer not null,
            shipmode_id integer,
            startdate timestamp,
            enddate timestamp,
            trackingnumber varchar(64),
            field1 varchar(254),
            precedence float not null default 0,
            field2 integer,
            flags integer not null default 0,
            primary key(shparrange_id)
        )""")
        cursor.execute("create unique index i0000229 on shparrange(ffmcenter_id,shipmode_id,store_id,startdate,enddate)")
        cursor.execute("create index i0000765 on shparrange(shipmode_id)")
        cursor.execute("create index i0000766 on shparrange(store_id)")
        # CONSTRAINT
    
    def shparjurgp(self):
        """each row of this table indicates that a shippingarrangement applies to all orderitems
        whose shipping addresses match a shipping jurisdiction group. refer to shparrange.flags"""
        cursor.execute("""create table shparjurgp(
            shparrange_id integer not null,
            jurstgroup_id integer not null,
            primary key(shparrange_id,jurstgroup_id)
        )""")
        cursor.execute("create index i0000764 on shparjurgp(jurstgroup_id)")
        # CONSTRAINT
    
    def shpinfo(self):
        """this table is used to store two different types of shipping information.
        both sets of information will be passed in the generated packslip file.
        the first set of information is to store shipping instructions. only one set of
        shipping instructions will be captured for any order, address, and ship mode combination.
        the second set of information is to store a shipping carrier account number.
        a shipping carrier account number will be stored for any order and shipmode combination"""
        cursor.execute("""create table shpinfo(
            shpinfo_id bigserial not null,
            orders_id bigint not null,
            address_id bigint not null,
            policy_id bigint,
            shipmode_id integer not null,
            carrieraccntnum varchar(100),
            instructions varchar(4000),
            primary key(shpinfo_id)
        )""")
        cursor.execute("create unique index i0000898 on shpinfo(orders_id,shipmode_id,address_id)")
        cursor.execute("create index i0000899 on shpinfo(address_id)")
        cursor.execute("create index i0000900 on shpinfo(policy_id)")
        cursor.execute("create index i0000902 on shpinfo(shipmode_id)")
        # CONSTRAINT

if __name__=="__main__":
    s=Shipping()
    s.shipmodedsc()
    s.shipmode()
    s.shparrange()
    s.shparjurgp()
    s.shpinfo()
