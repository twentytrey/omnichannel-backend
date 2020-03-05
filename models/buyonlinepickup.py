from db_con import createcon
con,cursor=createcon("retail","jmso","localhost","5432")
con.autocommit=True
from functions import build_constraint

class BuyOnlinePickupInStore:
    """the buy oline, pickup in-store model shows the relationship between
    database tables that contain information about online orders that 
    are to be picked up in-store"""
    def invavl(self):
        """each row represents an inventory availability
        record cached by the commerce database"""
        cursor.execute("""create table invavl(
            invavl_id bigserial not null,
            availquantity float,
            availtime timestamp,
            availoffset integer,
            lastupdate timestamp,
            field1 integer,
            field2 decimal(20,5),
            field3 varchar(254),
            catentry_id bigint not null,
            store_id integer,
            stloc_id integer,
            quantitymeasure char(16)not null default 'C62',
            inventorystatus char(4),
            primary key(invavl_id)
        )""")
        cursor.execute("create unique index i0001223 on invavl(catentry_id,store_id,stloc_id)")
        cursor.execute("create index i0001224 on invavl(store_id)")
        cursor.execute("create index i0001225 on invavl(stloc_id)")
        # CONSTRAINT
    
    def stlffmrel(self):
        "the table holds relationships between store location and ffmcenter"
        cursor.execute("""create table stlffmrel(
            stlffmrel_id serial not null,
            stloc_id integer not null,
            ffmcenter_id integer not null,
            address_id bigint not null,
            primary key(stlffmrel_id)
        )""")
        cursor.execute("create unique index i0001220 on stlffmrel(stloc_id,ffmcenter_id)")
        cursor.execute("create index i0001221 on stlffmrel(ffmcenter_id)")
        cursor.execute("create index i0001222 on stlffmrel(address_id)")
        # CONSTRAINT

if __name__=="__main__":
    b=BuyOnlinePickupInStore()
    b.invavl()
    b.stlffmrel()
