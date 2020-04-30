from db_con import createcon
con,cursor=createcon("retail","jmso","localhost","5432")
con.autocommit=True
from functions import build_constraint

class Fulfillment:
    """the fulfillment data model shows the relationship between database
    tables that contain information about fulfillment fulfillment centers 
    are not part of a store and hold inventory and hold inventory on behalf of stores."""
    def ffmcenter(self):
        "each row in this table represents a fulfillment center"
        cursor.execute("""create table ffmcenter(
            ffmcenter_id serial not null,
            member_id bigint not null,
            name varchar(254),
            defaultshipoffset integer not null default 86400,
            markfordelete integer not null default 0,
            extffmstorenum varchar(128),
            inventoryopflags integer not null default 0,
            maxnumpick smallint not null default 25,
            pickdelayinmin smallint not null default 5,
            dropship char(1)not null default 'N',
            primary key(ffmcenter_id)
        )""")
        cursor.execute("create unique index i0000101 on ffmcenter(member_id,name)")
        # CONSTRAINTS
    
    def ffmcentds(self):
        """each row of this table contain lang-dependent information
        about a fulfillment center"""
        cursor.execute("""create table ffmcentds(
            ffmcenter_id integer not null,
            language_id integer not null,
            staddress_id integer,
            description varchar(4000),
            displayname varchar(254),
            primary key(ffmcenter_id,language_id)
        )""")
        cursor.execute("create index i0000570 on ffmcentds(staddress_id)")
        # CONSTRAINTS
    
    def inventory(self):
        """the inventory table. each row of this table contains a quantity amount
        representing the inventory for a particular catalogentry. the catalogentry
        is available to be shipped from a fulfillment center on behalf of a store.
        this table cannot be used in conjunction with ATP inventory allocation.
        it is used only when ATP inventory is not enabled (refer to INVENTORYSYSTEM
        column of the STORE table). and it is used by the default implementations of the 
        non-ATP inventory commands."""
        cursor.execute("""create table inventory(
            catentry_id bigint not null,
            quantity float not null default 0,
            ffmcenter_id integer not null,
            store_id integer not null,
            quantitymeasure char(16)not null default 'C62',
            inventoryflags integer not null default 0,
            primary key(catentry_id,ffmcenter_id,store_id)
        )""")
        cursor.execute("create index i0000594 on inventory(ffmcenter_id)")
        cursor.execute("create index i0000595 on inventory(store_id)")
        # CONSTRAINTS
    
    def storeinv(self):
        """storeinv is a view used by the catalog search bean.
        it collates several fields from the inventory table/. there
        is a column allocationgoodfor in the store table if this column
        is set to zero, the search bean makes use of this view."""
        cursor.execute("""create table storeinv(
            store_id integer not null,
            catentry_id bigint not null,
            storequantity float,
            quantitymeasure char(16),
            c5 integer
        )""")

if __name__=="__main__":
    f=Fulfillment()
    f.ffmcenter()
    f.ffmcentds()
    f.inventory()
    f.storeinv()
