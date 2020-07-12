from db_con import con,cursor
from functions import build_constraint

class Vendor:
    """the vendor data model shows the relationship between database tables that contain
    information about vendors."""
    def vendor(self):
        """each row defines a vendor who has a relationship with a store
        or all the stores in a store group. generally to provide inventory"""
        cursor.execute("""create table vendor(
            vendor_id bigint not null,
            buyer_id bigint,
            lastupdate timestamp,
            markfordelete integer not null default 0,
            vendorname varchar(254),
            primary key(vendor_id)
        )""")
        cursor.execute("create unique index i0000263 on vendor(buyer_id,vendor_id)")
        # CONSTRAINT
    
    def vendordesc(self):
        cursor.execute("""create table vendordesc(
            vendor_id bigint not null,
            language_id integer not null,
            description varchar(512),
            lastupdate timestamp,
            primary key(vendor_id,language_id)
        )""")


if __name__=="__main__":
    v=Vendor()
    v.vendor()
    v.vendordesc()
