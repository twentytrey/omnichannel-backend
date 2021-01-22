from db_con import con,cursor
from functions import build_constraint

class AccessLogging:
    """access logging model shows the relationship between
    tables that log access violations and business auditing"""
    def acclogmain(self):
        """this table contains information about access violation.
        entries here are created only if a violation has occurred.
        there will be only one entry per request. detailed information
        is stored in the acclogsub table."""
        cursor.execute("""create table acclogmain(
            acclogmain_id bigserial not null,
            threadid varchar(32),
            hostname varchar(64),
            storeent_id integer not null,
            users_id bigint not null,
            primary key(acclogmain_id)
        )""")
    
    def acclogsub(self):
        """contains detailed information of the request causing access violation.
        the entries are linked to the acclogmain table"""
        cursor.execute("""create table acclogsub(
            acclogsub_id bigserial not null,
            acclogmain_id bigint not null,
            logtime timestamp,
            action varchar(254),
            result varchar(254),
            resources varchar(254),
            users_id bigint not null,
            primary key(acclogsub_id)
        )""")
        # CONSTRAINTS:
    
    def busaudit(self):
        """this table contains the systems auditing records captured when the 
        business auditing component is enabled."""
        cursor.execute("""create table busaudit(
            busaudit_id bigserial not null,
            session_id bigint,
            sequence integer,
            users_id bigint not null,
            for_user_id bigint,
            audit_timestamp timestamp not null,
            event_type char(3),
            signature varchar(254),
            store_id integer not null,
            occurence integer,
            command_name varchar(254),
            parameters text,
            primary key(busaudit_id)
        )""")
        cursor.execute("create index i0000374 on busaudit(session_id)")

if __name__=="__main__":
    a=AccessLogging()
    a.acclogmain()
    a.acclogsub()
    a.busaudit()
