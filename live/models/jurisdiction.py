from db_con import con,cursor
from functions import build_constraint

class Jurisdiction:
    """the jurisdiction data model shows the relationship between database tables
    that contain information about tax and shipping jurisdictions."""
    def jurstgprel(self):
        """each row of this table indicates that a jurisdiction of a particular
        subclass is in a jurisdiction group of that same class"""
        cursor.execute("""create table jurstgprel(
            jurst_id integer not null,
            jurstgroup_id integer not null,
            subclass integer not null,
            primary key(jurst_id,jurstgroup_id)
        )""")
        cursor.execute("create index i0000601x on jurstgprel(jurstgroup_id)")
        # CONSTRAINT
    
    def jurstgroup(self):
        """each row in this table represents an instance of a particular subclass
        of jurisdiction group. a jgroup of a particular suclass is a grouping of 
        jurisdiction definitions of that subclass/"""
        cursor.execute("""create table jurstgroup(
            jurstgroup_id serial not null,
            description varchar(254),
            subclass integer not null,
            storeent_id integer not null,
            code char(30)not null,
            markfordelete integer not null default 0,
            primary key(jurstgroup_id)
        )""")
        cursor.execute("create unique index i0000143 on jurstgroup(code,storeent_id,subclass,description)")
        cursor.execute("create index i0000602 on jurstgroup(storeent_id)")
        # CONSTRAINT
    
if __name__=="__main__":
    j=Jurisdiction()
    j.jurstgprel()
    j.jurstgroup()
