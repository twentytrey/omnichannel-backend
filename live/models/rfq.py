from db_con import createcon
con,cursor=createcon("retail","pronov","localhost","5432")
con.autocommit=True
from functions import build_constraint

class RFQ:
    """the request for quote data model shows the relationship 
    between database tables that contain information about RFQs"""
    def rfq(self):
        "this table holds basic RFQ data."
        cursor.execute("""create table rfq(
            member_id bigint not null,
            rfq_id bigint not null,
            accesstype integer,
            starttime timestamp,
            store_id integer,
            endtime timestamp,
            duration timestamp,
            numresponses integer,
            createtime timestamp,
            updatetime timestamp,
            canceltime timestamp,
            state integer not null,
            prevoffid bigint,
            nextoffid bigint,
            nextofftype integer,
            round integer,
            stage integer,
            name varchar(254)not null,
            majorversion integer not null,
            minorversion integer not null,
            endresult integer,
            markfordelete integer,
            activatetime timestamp,
            closetime timestamp,
            completetime timestamp,
            ruletype integer not null default 1,
            tracknumber varchar(254),
            versionflags integer,
            extrfqnum varchar(64),
            field1 bigint,
            field2 integer,
            field3 varchar(254),
            field4 varchar(254),
            field5 timestamp,
            field6 timestamp,
            primary key(rfq_id)
        )""")
        cursor.execute("create unique index i0000207 on rfq(name,majorversion,minorversion)")
        cursor.execute("create index i0000348 on rfq(state)")
        cursor.execute("create index i0000724 on rfq(store_id)")
        cursor.execute("create index i0000725 on rfq(member_id)")
        # CONSTRAINTS
    
    def rfqtarget(self):
        "this table holds the target stores for RFQs"
        cursor.execute("""create table rfqtarget(
            store_id integer not null,
            rfq_id bigint not null,
            primary key(store_id,rfq_id)
        )""")
        cursor.execute("create index i0000358 on rfqtarget(rfq_id)")
        # CONSTRAINTS
    
    def rfqrsp(self):
        "RFQ response table. stores response information"
        cursor.execute("""create table rfqrsp(
            rfq_id bigint not null,
            majorversion integer not null,
            member_id bigint not null,
            minorversion integer not null,
            name varchar(200)not null,
            state integer not null,
            rejectreason varchar(254),
            remarks varchar(254),
            createtime timestamp,
            updatetime timestamp,
            canceltime timestamp,
            markfordelete integer,
            rfqrsp_id bigint not null,
            description varchar(254),
            versionflags integer,
            store_id integer not null,
            prevrsp bigint,
            acceptaction integer not null default 0,
            extrfqresponsenum varchar(64),
            field1 bigint,
            field2 integer,
            field3 varchar(254),
            field4 varchar(254),
            field5 timestamp,
            field6 timestamp,
            primary key(rfqrsp_id)
        )""")
        cursor.execute("create unique index i0000209 on rfqrsp(name,majorversion,minorversion)")
        cursor.execute("create index i0000351 on rfqrsp(rfq_id,member_id)")
        cursor.execute("create index i0000727 on rfqrsp(member_id)")
        cursor.execute("create index i0000352 on rfqrsp(name)")
        # CONSTRAINTS
    
    def rfqcategry(self):
        "this table holds categories created in each RFQ"
        cursor.execute("""create table rfqcategry(
            rfqcategry_id bigserial not null,
            name varchar(200)not null,
            rfq_id bigint not null,
            primary key(rfqcategry_id)
        )""")
        cursor.execute("create unique index i0000297 on rfqcategry(rfq_id,name)")
        # CONSTRAINTS
    
    def rfqrspprod(self):
        """RFQ response and product relationship table.
        this table stores the products included in the specific RFQ response."""
        cursor.execute("""create table rfqrspprod(
            catentry_id bigint,
            rfqrsp_id bigint not null,
            quantity float,
            currency char(3),
            price decimal(20,5),
            qtyunit_id char(16),
            rfqcatentryid bigint,
            rfqrspprod_id bigint not null,
            rfqprod_id bigint,
            skugenflag integer not null default 0,
            priceadjustment float,
            field1 bigint,
            field2 integer,
            field3 varchar(254),
            field4 varchar(254),
            primary key(rfqrspprod_id)
        )""")
        cursor.execute("create index i0000353 on rfqrspprod(rfqrsp_id,rfqprod_id)")
        cursor.execute("create index i0000733 on rfqrspprod(rfqprod_id)")
        cursor.execute("create index i0000734 on rfqrspprod(catentry_id)")
        # CONSTRAINT

    def rfqrspeval(self):
        "holds all the response product evaluations for the RFQ"
        cursor.execute("""create table rfqrspeval(
            rfqrspeval_id bigserial not null,
            evalresult integer not null default 1,
            remarks varchar(254),
            updatetime timestamp,
            rfq_id bigint not null,
            rfqrsp_id bigint not null,
            rfqrspprod_id bigint not null,
            primary key(rfqrspeval_id)
        )""")
        cursor.execute("create index i0000338 on rfqrspeval(rfqrspprod_id)")
        cursor.execute("create index i0000728 on rfqrspeval(rfqrsp_id)")
        cursor.execute("create index i0000729 on rfqrspeval(rfq_id)")
        # CONSTRAINTS
    
    def rfqrsptcrl(self):
        """the relationship between one specified RFQ term or condition
        and an RFQ response to this term or condition"""
        cursor.execute("""create table rfqrsptcrl(
            rfqrsptcrl_id bigserial not null,
            rfq_id bigint not null,
            rfqrsp_id bigint not null,
            rfqtc_id bigint not null,
            rfqrsptc_id bigint not null,
            changeflag integer,
            primary key(rfqrsptcrl_id)
        )""")
        cursor.execute("create unique index i0000211 on rfqrsptcrl(rfq_id,rfqrsp_id,rfqtc_id,rfqrsptc_id)")
        cursor.execute("create unique index i0000212 on rfqrsptcrl(rfqtc_id,rfqrsptc_id)")
        cursor.execute("create index i0000735 on rfqrsptcrl(rfqrsptc_id)")
        cursor.execute("create index i0000736 on rfqrsptcrl(rfqrsp_id)")
        # CONSTRAINTS
    
    def rfqprod(self):
        """RFQ Request and Product relationship table.
        this table stores information about the products requested in an RFQ."""
        cursor.execute("""create table rfqprod(
            rfq_id bigint not null,
            quantity float,
            price decimal(20,5),
            currency char(3),
            qtyunit_id char(16),
            catentry_id bigint,
            rfqprod_id bigint not null,
            rfqprodname varchar(254),
            rfqcategory_id bigint,
            changeable integer not null default 0,
            priceadjustment float,
            negotiationtype integer not null default 1,
            field1 bigint,
            field2 integer,
            field3 varchar(254),
            field4 varchar(254),
            primary key(rfqprod_id)
        )""")
        cursor.execute("create index i0000349 on rfqprod(rfq_id,catentry_id)")
        cursor.execute("create index i0000350 on rfqprod(rfq_id)")
        cursor.execute("create index i0000372 on rfqprod(rfq_id,negotiationtype)")
        cursor.execute("create index i0000726 on rfqprod(catentry_id)")
        cursor.execute("create index i0001278 on rfqprod(rfqcategory_id)")
        # CONSTRAINTS
    
    def rfqrspparl(self):
        """this table holds the relationship of the personalized
        attributes in the RFQ and the response."""
        cursor.execute("""create table rfqrspparl(
            rfqrspparl_id bigint not null,
            rfq_id bigint not null,
            rfqrsp_id bigint not null,
            rfqpattrvalue_id bigint not null,
            rfqrsppattrval_id bigint,
            primary key(rfqrspparl_id)
        )""")
        cursor.execute("create index i0000359 on rfqrspparl(rfqpattrvalue_id)")
        cursor.execute("create index i000730 on rfqrspparl(rfq_id)")
        cursor.execute("create index i0000731 on rfqrspparl(rfqrsp_id)")
        cursor.execute("create index i0000732 on rfqrspparl(rfqrsppattrval_id)")
        # CONSTRAINTS
    
    def pattrvalue(self):
        """the personalization attribute value table.
        this table holds the values associated with personalization attributes"""
        cursor.execute("""create table pattrvalue(
            pattrvalue_id bigint not null,
            pattribute_id bigint not null,
            attrtype_id char(16)not null,
            operator_id integer not null,
            termcond_id bigint,
            qtyunit_id char(16),
            integervalue integer,
            floatvalue float,
            stringvalue varchar(254),
            datevalue timestamp,
            bigintvalue bigint,
            sequence integer,
            encryptflag integer not null default 0,
            orderitems_id bigint,
            mandatory integer not null default 0,
            attachment_id bigint,
            changeable integer not null default 0,
            rfqprod_id bigint,
            rfqrspprod_id bigint,
            correlationgroup bigint,
            primary key(pattrvalue_id)
        )""")
        cursor.execute("create index i0000354 on pattrvalue(termcond_id)")
        cursor.execute("create index i0000355 on pattrvalue(rfqprod_id)")
        cursor.execute("create index i0000356 on pattrvalue(rfqrspprod_id)")
        cursor.execute("create index i0000367 on pattrvalue(correlationgroup)")
        cursor.execute("create index i0000682 on pattrvalue(pattribute_id)")
        cursor.execute("create index i0000683 on pattrvalue(orderitems_id)")
        cursor.execute("create index i0001270 on pattrvalue(attachment_id)")
        # CONSTRAINTS
    
    def pattribute(self):
        "this is the personalization attribute supported by the site."
        cursor.execute("""create table pattribute(
            pattribute_id bigint not null,
            name varchar(254),
            attrtype_id char(16)not null,
            accessbeanname varchar(254),
            sequence integer,
            encryptflag integer not null,
            primary key(pattribute_id)
        )""")
        cursor.execute("create unique index i0000185 on pattribute(name)")
        # CONSTRAINTS
    
    def pattrdesc(self):
        cursor.execute("""create table pattrdesc(
            pattribute_id bigint not null,
            language_id integer not null,
            description varchar(1024),
            primary key(pattribute_id,language_id)
        )""")
    
    def pattrprod(self):
        "the relationship table between the pattribute and the catentry tables"
        cursor.execute("""create table pattrprod(
            pattribute_id bigint not null,
            catentry_id bigint not null,
            primary key(pattribute_id,catentry_id)
        )""")
        cursor.execute("create index i0000681 on pattrprod(catentry_id)")
        # CONSTRAINTS

if __name__=="__main__":
    r=RFQ()
    r.pattrdesc()
    r.pattribute()
    r.pattrprod()
    r.pattrvalue()
    r.rfq()
    r.rfqcategry()
    r.rfqprod()
    r.rfqrsp()
    r.rfqrspeval()
    r.rfqrspparl()
    r.rfqrspprod()
    r.rfqrsptcrl()
    r.rfqtarget()
    