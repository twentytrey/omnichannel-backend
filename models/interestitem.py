from db_con import createcon
con,cursor=createcon("retail","jmso","localhost","5432")
con.autocommit=True
from functions import build_constraint

class InterestItem:
    """the interest item data model shows the relationship
    between database tables that contain information about interest items"""
    def iitem(self):
        "each row of this table represents an IItem in an iitemlist"
        cursor.execute("""create table iitem(
            catentry_id bigint not null,
            iitemlist_id bigint not null,
            member_id bigint not null,
            storeent_id integer not null,
            lastupdate timestamp,
            sequence float not null default 0,
            field1 integer,
            field2 decimal(20,5),
            quantity float,
            field3 varchar(254),
            primary key(iitemlist_id,catentry_id)
        )""")
        cursor.execute("create index i0000584 on iitem(catentry_id)")
        cursor.execute("create index i0000585 on iitem(storeent_id)")
        cursor.execute("create index i0000596 on iitem(member_id)")
        # CONSTRAINTS
    
    def iitemlist(self):
        "each row in this table represents an interestitemlist"
        cursor.execute("""create table iitemlist(
            iitemlist_id bigserial not null,
            member_id bigint not null,
            description varchar(254)not null,
            sequence float not null default 0,
            lastupdate timestamp,
            primary key(iitemlist_id)
        )""")
        cursor.execute("create unique index i0000132 on iitemlist(iitemlist_id,sequence,member_id)")
        cursor.execute("create unique index i0000133 on iitemlist(iitemlist_id,member_id)")
        cursor.execute("create index i0000587 on iitemlist(member_id)")
        # CONSTRAINT
    
    def ciitemlist(self):
        """each row in this table represents the relationship betweeen an iitemlist
        and a member to which it is te current list"""
        cursor.execute("""create table ciitemlist(
            iitemlist_id bigint not null,
            member_id bigint not null,
            primary key(iitemlist_id,member_id)
        )""")
        cursor.execute("create index i0000535 on ciitemlist(member_id)")
        # CONSTRAINTS

if __name__=="__main__":
    i=InterestItem()
    i.iitemlist()
    i.iitem()
    i.ciitemlist()
