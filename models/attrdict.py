from db_con import createcon
con,cursor=createcon("jno","tiniraph","localhost","5432")
con.autocommit=True
from functions import build_constraint

class Attrdict:
    """the attribute dictionary data model shows the relationship between database 
    table that contain information about dictionaries."""
    def attr(self):
        """stores attribute dictionary attributes. these attributes can be used for descriptive or SKU
        resolution purposes. and can be shared by catalog entries. non attribute dictionary attributes.
        used for single catalo entry are stored in the attribute table."""
        cursor.execute("""create table attr(
            attr_id bigserial not null,
            identifier varchar(254)not null,
            attrtype_id char(16)not null,
            attrdict_id bigint,
            storeent_id integer not null,
            sequence float not null default 0,
            displayable integer,
            searchable integer,
            comparable integer,
            field1 integer,
            field2 integer,
            field3 varchar(254),
            attrusage integer,
            storedisplay smallint,
            facetable smallint not null default 0,
            merchandisable integer,
            swatchable smallint not null default 0,
            primary key(attr_id)
        )""")
        cursor.execute("create unique index i0001203 on attr(identifier,attrdict_id)")
        cursor.execute("create index i0001204 on attr(storeent_id)")
        cursor.execute("create index i0001464 on attr(facetable)")
        # CONSTRAINT
    
    def attrdesc(self):
        """this table holds the language sensitive attribute description.
        before loading attributes in multiple languafes, the attributes must already
        exist in the database with default data."""
        cursor.execute("""create table attrdesc(
            attr_id bigint not null,
            language_id integer not null,
            attrtype_id char(16)not null,
            name varchar(254),
            description varchar(254),
            description2 varchar(254),
            field1 varchar(254),
            groupname varchar(64),
            qtyunit_id char(16),
            noteinfo varchar(64),
            primary key(attr_id,language_id)
        )""")
        cursor.execute("create index i0001465 on attrdesc(language_id)")
        cursor.execute("create index i0001466 on attrdesc(attrtype_id)")
        cursor.execute("create index i0001467 on attrdesc(qtyunit_id)")
        # CONSTRAINTS
    
    def attrdict(self):
        """table used to store the attribute dictionaries configured for the system.
        each attribute dictionary is owned by a store, but can be used by children stores 
        through store relationships. there can be only one attribute dictionary owned by any given store."""
        cursor.execute("""create table attrdict(
            attrdict_id bigserial not null,
            storeent_id integer,
            field1 integer,
            field2 integer,
            field3 varchar(254),
            primary key(attrdict_id)
        )""")
        cursor.execute("create unique index i0001133 on attrdict(storeent_id)")
        # CONSTRAINTS
    
    def attrval(self):
        """this table holds an attribute value that can be a shareable global attribute
        or a local attribute value defined for a catalog entry."""
        cursor.execute("""create table attrval(
            attrval_id bigserial not null,
            attr_id bigint not null,
            identifier varchar(254),
            valusage integer,
            storeent_id integer,
            field1 integer,
            field2 integer,
            field3 varchar(254),
            primary key(attrval_id)
        )""")
        cursor.execute("create unique index i0001205 on attrval(attr_id,identifier)")
        cursor.execute("create index i0001206 on attrval(attr_id,storeent_id,valusage)")
        # CONSTRAINT
    
    def attrvaldesc(self):
        cursor.execute("""create table attrvaldesc(
            attrval_id bigint not null,
            language_id integer not null,
            attr_id bigint not null,
            value varchar(254),
            valusage integer,
            sequence float,
            stringvalue varchar(2000),
            integervalue integer,
            floatvalue float,
            qtyunit_id char(16),
            image1 varchar(254),
            image2 varchar(254),
            field1 integer,
            field2 varchar(254),
            field3 varchar(254),
            primary key(attrval_id,language_id)
        )""")
        cursor.execute("create index i0001468 on attrvaldesc(language_id)")
        cursor.execute("create index i0001469 on attrvaldesc(attr_id)")
        cursor.execute("create index i0001470 on attrvaldesc(qtyunit_id)")
        # CONSTRAINT
    
    def catentryattr(self):
        """stores the catalog entry and attribute dictionary relationship. for example when assigning
        an attribute dictionary attribute to a catalog entry, a row is created in this table with the details
        of the relationship between the two objects"""
        cursor.execute("""create table catentryattr(
            catentry_id bigint not null,
            attr_id bigint not null,
            attrval_id bigint not null default 0,
            usage char(1)not null,
            sequence float,
            field1 integer,
            field2 integer,
            field3 varchar(254),
            primary key(catentry_id,attr_id,attrval_id)
        )""")
        cursor.execute("create index i0001202 on catentryattr(catentry_id,usage)")
        cursor.execute("create index i0001462 on catentryattr(attrval_id)")
        cursor.execute("create index i0001463 on catentryattr(attr_id)")
        # CONSTRAINT
    
    def attrdictgrpattrel(self):
        "stores the rel between attribute dictionary group and attribute dictionary attribute"
        cursor.execute("""create table attrdictgrpattrel(
            attrdictgrp_id bigint not null,
            attr_id bigint not null,
            sequence float not null default 0,
            primary key(attrdictgrp_id,attr_id)
        )""")
        # CONSTRAINTS
    
    def attrdictgrprel(self):
        """defines the relationships between attribute dictionary attribute groups.
        an attribute dictionary attribute group can only have one parent group."""
        cursor.execute("""create table attrdictgrprel(
            attrdictgrp_parent bigint not null,
            attrdictgrp_child bigint not null,
            sequence float not null default 0,
            primary key(attrdictgrp_parent,attrdictgrp_child)
        )""")
        cursor.execute("create unique index i0001137 on attrdictgrprel(attrdictgrp_child)")
        # CONSTRAINTS

    def attrdictgrpdesc(self):
        "the table holds the attribute dictionary group description"
        cursor.execute("""create table attrdictgrpdesc(
            attrdictgrp_id bigint not null,
            language_id integer not null,
            name varchar(254)not null,
            shortdescription varchar(254),
            field1 integer,
            primary key(attrdictgrp_id,language_id)
        )""")
        cursor.execute("create index i0001136 on attrdictgrpdesc(name,language_id)")
        # CONSTRAINTS
    
    def attrdictgrp(self):
        """used to store attribute dictionary attribute groups. these groups are a convenience mechanism
        used during administration of the attribute dictionary. and when assigning attriute dictionary 
        attributes to catalog entries or catalog groups. attributes can belong to zero or more attribute groups."""
        cursor.execute("""create table attrdictgrp(
            attrdictgrp_id bigserial not null,
            identifier varchar(254)not null,
            attrdict_id bigint not null,
            storeent_id integer not null,
            markfordelete integer not null default 0,
            sequence float not null default 0,
            field1 integer,
            field2 integer,
            field3 varchar(254),
            primary key(attrdictgrp_id)
        )""")
        cursor.execute("create unique index i0001135 on attrdictgrp(identifier,attrdict_id)")
        cursor.execute("create index i0001187 on attrdictgrp(storeent_id)")
        cursor.execute("create index i0001188 on attrdictgrp(attrdict_id)")
        # CONSTRAINT

if __name__=="__main__":
    a=Attrdict()
    # a.attr()
    # a.attrdesc()
    # a.attrdict()
    # a.attrdictgrp()
    # a.attrdictgrpattrel()
    # a.attrdictgrpdesc()
    # a.attrdictgrprel()
    # a.attrval()
    # a.attrvaldesc()
    # a.catentryattr()
