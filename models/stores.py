from db_con import createcon
con,cursor=createcon("jno","tiniraph","localhost","5432")
con.autocommit=True
from functions import build_constraint

class Stores:
    """the stores data model shows the relationship between database
    tables that contain information about stores."""
    def storeent(self):
        """each row represents a storeentity. a storeentity is an abstract superclass
        tat can represent either a store or a storegroup."""
        cursor.execute("""create table storeent(
            storeent_id serial not null,
            member_id bigint not null,
            type char(1)not null,
            setccurr char(3),
            identifier varchar(254)not null,
            markfordelete integer not null default 0,
            primary key(storeent_id)
        )""")
        cursor.execute("create unique index i0000240 on storeent(identifier,member_id)")
        cursor.execute("create index i0000787 on storeent(member_id)")
        # CONSTRAINTS
    
    def storeentds(self):
        """each row of this table represents a store entity.
        a store entity is ab abstract super class that can represent
        either a store or a store group."""
        cursor.execute("""create table storeentds(
            language_id integer not null,
            storeent_id integer not null,
            displayname varchar(254),
            staddress_id_loc integer,
            description varchar(4000),
            staddress_id_cont integer,
            primary key(language_id,storeent_id)
        )""")
        cursor.execute("create index i0000788 on storeentds(staddress_id_loc)")
        cursor.execute("create index i0000789 on storeentds(staddress_id_cont)")
        cursor.execute("create index i0000790 on storeentds(storeent_id)")
        # CONSTRAINTS:

    def storembrgrp(self):
        """each row of this table indicates that a store
        recognizes a member group as a customer group"""
        cursor.execute("""create table storembrgrp(
            mbrgrp_id bigint not null,
            store_id integer not null,
            primary key(mbrgrp_id,store_id)
        )""")
        cursor.execute("create index i0000793 on storembrgrp(store_id)")
        # CONSTRAINTS:

    def storegrp(self):
        """each row of this table represents a store group. a store group
        contains information that can be used by the stores in that store group/
        a storegroup is a store entity."""
        cursor.execute("""create table storegrp(
            storegrp_id integer not null,
            field1 varchar(254),
            primary key(storegrp_id)
        )""")
        # CONSTRAINTS
    
    def store(self):
        "each row represents a store. a store is a store entity."
        cursor.execute("""create table store(
            store_id integer not null,
            storegrp_id integer not null,
            storecgry_id integer,
            language_id integer,
            ffmcenter_id integer,
            status integer not null default 1,
            storelevel char(10),
            quotegoodfor integer default 43200,
            field1 varchar(254),
            field2 varchar(254),
            allocationgoodfor integer not null default 43200,
            maxbooffset integer not null default 7776000,
            rejectedorexpiry integer default 259200,
            ffmselectionflags integer not null default 0,
            bopmpadfactor integer default 0,
            rtnffmctr_id integer,
            defaultbooffset integer not null default 7776000,
            pricerefflags integer not null default 0,
            storetype char(3),
            rmagoodfor integer default 86400,
            avsacceptcodes varchar(64),
            crtdbycntr_id bigint,
            lastupdatestatus timestamp,
            allocationoffset integer not null default 86400,
            maxfooffset integer default 7776000,
            inventoryopflag integer not null default 0,
            blockingactive smallint default 1,
            persistentsession smallint,
            orderhistoryactive char(1)not null default 'Y',
            inventorysystem smallint not null default -1,
            primary key(store_id)
        )""")
        cursor.execute("create index i0000778 on store(ffmcenter_id)")
        cursor.execute("create index i0000779 on store(storecgry_id)")
        cursor.execute("create index i0000780 on store(rtnffmctr_id)")
        cursor.execute("create index i0000781 on store(crtdbycntr_id)")
        cursor.execute("create index i0001288 on store(storegrp_id)")
        # CONSTRAINTS:
    
    def storecgry(self):
        """each row of this table represents a store category.
        store categories can be used to group stores of similar types.
        together for display purposes. for example, in order to display
        all clothing stores in a mall together, in the mall directory, 
        you could create a clothing store category."""
        cursor.execute("""create table storecgry(
            storecgry_id serial not null,
            name varchar(254)not null,
            remark varchar(254),
            primary key(storecgry_id)
        )""")
        cursor.execute("create unique index i0000239 on storecgry(name)")
    
    def storecgrydesc(self):
        cursor.execute("""create table storecgrydesc(
            storecgry_id integer not null,
            language_id integer not null,
            description varchar(254),
            displayname varchar(128),
            primary key(storecgry_id,language_id)
        )""")
        # CONSTRAINTS

    def storerel(self):
        "each row describes a relationship between stores"
        cursor.execute("""create table storerel(
            streltyp_id integer not null,
            relatedstore_id integer not null,
            store_id integer not null,
            sequence float not null default 0,
            state integer not null default 1,
            primary key(store_id,streltyp_id,relatedstore_id)
        )""")
        cursor.execute("create index i0000794 on storerel(streltyp_id)")
        cursor.execute("create index i0000795 on storerel(relatedstore_id)")
        # CONSTRAINTS
    
    def streltyp(self):
        "identifies all the store relationship types in the system"
        cursor.execute("""create table streltyp(
            name char(60),
            streltyp_id integer not null,
            primary key(streltyp_id)
        )""")
        cursor.execute("create unique index i0000267 on streltyp(name)")
    
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
            pickdelaymin smallint not null default 5,
            dropship char(1)not null default 'N',
            primary key(ffmcenter_id)
        )""")
        cursor.execute("create index i0000101 on ffmcenter(member_id,name)")
        # CONSTRAINTS:
    
    def storelang(self):
        "each row indicates that a store entity supports a language. see also the langpair table"
        cursor.execute("""create table storelang(
            language_id integer not null,
            storeent_id integer not null,
            setccurr char(3),
            primary key(language_id,storeent_id)
        )""")
        cursor.execute("create index i0000792 on storelang(storeent_id)")
        # CONSTRAINTS:
    
    def storelangds(self):
        """each row table contains a description,  in a particular languae
        of a supported language. for example the spanish language might be
        described as 'Espanol' in French but as 'Spanish' in English"""
        cursor.execute("""create table storelangds(
            storeent_id integer not null,
            language_id_desc integer not null,
            description varchar(254),
            language_id integer not null,
            primary key(storeent_id,language_id_desc,language_id)
        )""")
        cursor.execute("create index i0001290 on storelangds(language_id,storeent_id)")
        # CONSTRAINTS:
    
    def staddress(self):
        """each row of this table represents a store address.
        store entities, fulfillment centers and vendors can have
        store addresses."""
        cursor.execute("""create table staddress(
            staddress_id serial not null,
            address1 varchar(256),
            member_id bigint not null,
            address2 varchar(128),
            address3 varchar(128),
            city varchar(128),
            country varchar(128),
            email1 varchar(254),
            email2 varchar(254),
            fax1 varchar(32),
            fax2 varchar(32),
            field1 varchar(64),
            field2 varchar(64),
            field3 varchar(64),
            phone1 varchar(32),
            phone2 varchar(32),
            state varchar(128),
            zipcode varchar(40),
            firstname varchar(128),
            lastname varchar(128),
            middlename varchar(128),
            persontitle varchar(50),
            businesstitle varchar(128),
            nickname varchar(254)not null,
            shippinggeocode varchar(254),
            taxgeocode varchar(254),
            url varchar(254),
            primary key(staddress_id)
        )""")
        cursor.execute("create unique index i0000231 on staddress(member_id,nickname)")
        # CONSTRAINTS:
    
    def tickler(self):
        "this table jolds to-do items requiring actions to resolve"
        cursor.execute("""create table tickler(
            tickler_id bigserial not null,
            status smallint not null default 0,
            store_id integer not null,
            actionobjecttype char(5),
            actionobject bigint,
            tklrreason_id integer not null,
            responsiblemember bigint,
            lockedby_id bigint,
            createdby_id bigint,
            nexttickledate timestamp not null,
            createtime timestamp not null,
            locktime timestamp,
            lastupdate timestamp,
            field1 integer,
            field2 varchar(254),
            field3 bigint,
            language_id integer not null,
            ticklercomment varchar(1024),
            responsiblerole integer,
            primary key(tickler_id)
        )""")
        cursor.execute("create index i0000939 on tickler(tklrreason_id)")
        cursor.execute("create index i0000940 on tickler(language_id)")
        cursor.execute("create index i0000941 on tickler(createdby_id)")
        cursor.execute("create index i0000942 on tickler(lockedby_id)")
        cursor.execute("create index i0000948 on tickler(responsiblemember,store_id,status,nexttickledate)")
        cursor.execute("create index i0000953 on tickler(responsiblerole)")
        cursor.execute("create index i0000978 on tickler(status,nexttickledate)")
        # CONSTRAINTS:
    
    def tklraction(self):
        "this table holds the actions that can be performed on to-do items"
        cursor.execute("""create table tklraction(
            tklraction_id serial not null,
            store_id integer not null,
            code char(30)not null,
            closingaction smallint not null default 0,
            markfordelete integer not null default 0,
            field1 varchar(254),
            primary key(tklraction_id)
        )""")
        cursor.execute("create unique index i0000937 on tklraction(code,store_id)")
        cursor.execute("create index i0000947 on tklraction(store_id)")
        # CONSTRAINTS:

    def tklractdsc(self):
        "holds the description of actions that can be performed on to-do items"
        cursor.execute("""create table tklractdsc(
            tklraction_id integer not null,
            language_id integer not null,
            description varchar(254),
            primary key(tklraction_id,language_id)
        )""")
        # CONSTRAINTS:

    def repdlvry(self):
        "this table describes how store entities want their automated commerce reports delivered."
        cursor.execute("""create table repdlvry(
            storeent_id integer not null,
            fiscalyear char(50)not null default '01/01',
            format integer not null default 0,
            frequency char(1)not null default 'M',
            primary key(storeent_id)
        )""")
        # CONSTRAINTS:

    def tklacthist(self):
        "this table holds the description of actions that can be performed on to do items"
        cursor.execute("""create table tklacthist(
            tklacthist_id bigserial not null,
            tickler_id bigint not null,
            tklraction_id integer not null,
            actiondate timestamp not null,
            createdby_id bigint not null,
            lastupdate timestamp not null,
            field1 integer,
            field2 varchar(254),
            language_id integer not null,
            actioncomment varchar(1024),
            primary key(tklacthist_id)
        )""")
        cursor.execute("create unique index i0000936 on tklacthist(tickler_id,actiondate)")
        cursor.execute("create index i0000944 on tklacthist(tklraction_id)")
        cursor.execute("create index i0000945 on tklacthist(language_id)")
        cursor.execute("create index i0000946 on tklacthist(createdby_id)")
        # CONSTRAINTS:
    
    def tklrrsndsc(self):
        "holds description of reasons for creating to-do items"
        cursor.execute("""create table tklrrsndsc(
            tklrreason_id integer not null,
            language_id integer not null,
            description varchar(254),
            primary key(tklrreason_id,language_id)
        )""")
        # CONSTRAINTS:
    
    def tklrreason(self):
        "holds reasons for creating to-do items"
        cursor.execute("""create table tklrreason(
            tklrreason_id serial not null,
            store_id integer not null,
            systemdefined smallint not null default 0,
            code char(30)not null,
            ticklerfrequency integer not null default 0,
            markfordelete integer not null default 0,
            field1 varchar(254),
            assigntorole integer,
            primary key(tklrreason_id)
        )""")
        cursor.execute("create unique index i0000935 on tklrreason(code,store_id)")
        cursor.execute("create index i0000943 on tklrreason(store_id)")
        cursor.execute("create index i0000955 on tklrreason(assigntorole)")
        # CONSTRAINTS
    
    def storedef(self):
        "each row holds default information for a store."
        cursor.execute("""create table storedef(
            store_id integer not null,
            contract_id bigint,
            shipmode_id integer,
            primary key(store_id)
        )""")
        cursor.execute("create index i0000785 on storedef(contract_id)")
        cursor.execute("create index i0000786 on storedef(shipmode_id)")
        # CONSTRAINTS:
    
    def shipmode(self):
        """each row of this table represents a shipping mode for a store entity.
        a store can use its own shipping modes, and the shipping modes of its store group."""
        cursor.execute("""create table shipmode(
            shipmode_id serial not null,
            field1 varchar(254),
            storeent_id integer not null,
            field2 integer,
            code char(30),
            carrier char(30),
            trackingname varchar(64),
            trackingurl varchar(254),
            trackinghost varchar(64),
            trackingport integer,
            trackingicon varchar(64),
            trackingtype char(8),
            markfordelete integer not null default 0,
            primary key(shipmode_id)
        )""")
        cursor.execute("create unique index i0000228 on shipmode(storeent_id,code,carrier)")
        # CONSTRAINTS:
    
    def blkrsncode(self):
        "stores the various reason codes for which an order may be blocked."
        cursor.execute("""create table blkrsncode(
            blkrsncode_id serial not null,
            blockreasontype char(25)not null,
            manualblock smallint not null,
            markfordelete char(1)not null,
            field1 integer,
            field2 varchar(254),
            primary key(blkrsncode_id)
        )""")
    
    def storblkrsn(self):
        """store level block reason code configuration.
        used to configure whether a block reason code is turned
        on for a store and also configure whether this block reason 
        code will generate ticklers."""
        cursor.execute("""create table storblkrsn(
            storeent_id integer not null,
            blkrsncode_id integer not null,
            respected smallint not null default 1,
            tklrgeneration smallint not null default 1,
            field1 integer,
            field2 varchar(254),
            primary key(storeent_id,blkrsncode_id)
        )""")
        # CONSTRAINTS:
    
    def ordchgrsnds(self):
        "the order change reason code description for different languages"
        cursor.execute("""create table ordchgrsnds(
            ordchgrsn_id integer not null,
            language_id integer not null,
            description varchar(1024),
            primary key(ordchgrsn_id,language_id)
        )""")
        # CONSTRAINTS
    
    def ordchgrsn(self):
        "stores the order change reason code for different actions."
        cursor.execute("""create table ordchgrsn(
            ordchgrsn_id serial not null,
            storeent_id integer not null,
            reasoncode varchar(64)not null,
            field1 varchar(254),
            field2 varchar(254),
            field3 integer,
            primary key(ordchgrsn_id)
        )""")
        cursor.execute("create index i0001266 on ordchgrsn(storeent_id)")
        # CONSTRAINTS
    
    def orcomment(self):
        """stores the comments for an order entered by a customer service representative."""
        cursor.execute("""create table orcomment(
            orcomment_id bigserial not null,
            orders_id bigint not null,
            lastupdate timestamp,
            comments varchar(3000),
            ordchgrsn_id integer,
            servicerep_id bigint,
            buschn_id integer,
            orderversion smallint,
            field1 integer,
            field2 varchar(254),
            field3 timestamp,
            primary key(orcomment_id)
        )""")
        cursor.execute("create index i0000632 on orcomment(orders_id)")
        cursor.execute("create index i0001264 on orcomment(ordchgrsn_id)")
        cursor.execute("create index i0001265 on orcomment(servicerep_id)")
        # CONSTRAINTS:
    
    def opsystem(self):
        "this table is used for storing the order processing system."
        cursor.execute("""create table opsystem(
            opsystem_id serial not null,
            name varchar(254)not null,
            primary key(opsystem_id)
        )""")
    
    def buschn(self):
        "contains business channel information"
        cursor.execute("""create table buschn(
            buschn_id integer not null,
            name char(16)not null,
            state char(1)not null,
            primary key(buschn_id)
        )""")
    
    def stloc(self):
        "represents store location information"
        cursor.execute("""create table stloc(
            stloc_id serial not null,
            identifier varchar(128)not null,
            phone char(32),
            fax char(32),
            address1 varchar(128),
            address2 varchar(128),
            address3 varchar(64),
            city varchar(128),
            state varchar(128),
            country  varchar(128),
            zipcode char(40),
            active smallint not null default 1,
            latitude decimal(20,5),
            longitude decimal(20,5),
            geonode_id integer,
            storeent_id integer not null default 0,
            primary key(stloc_id)
        )""")
        cursor.execute("create unique index i0001460 on stloc(storeent_id,identifier)")
        cursor.execute("create index i0001210 on stloc(latitude,longitude)")
        cursor.execute("create index i0001211 on stloc(geonode_id)")
        # CONSTRAINTS
    
    def geonode(self):
        "represents a geographical node in the GEO tree"
        cursor.execute("""create table geonode(
            geonode_id serial not null,
            identifier varchar(64)not null,
            type char(4)not null,
            storeent_id integer not null default 0,
            primary key(geonode_id)
        )""")
        cursor.execute("create unique index i0001459 on geonode(storeent_id,identifier)")
        # CONSTRAINTS

    def geondds(self):
        "holds GEO node descriptions"
        cursor.execute("""create table geondds(
            geondds_id serial not null,
            geonode_id integer not null,
            language_id integer not null,
            name varchar(128)not null,
            description varchar(254),
            primary key(geondds_id)
        )""")
        cursor.execute("create unique index i0001216 on geondds(geonode_id,language_id)")
        # CONSTRAINTS

    def geotree(self):
        """represents a tree of geo locations. this is a relationship
        table og geonode, such as country state, city"""
        cursor.execute("""create table geotree(
            geotree_id serial not null,
            child_geonode_id integer not null,
            parent_geonode_id integer,
            sequence float,
            primary key(geotree_id)
        )""")
        cursor.execute("create unique index i0001217 on geotree(child_geonode_id,parent_geonode_id)")
        cursor.execute("create index i0001218 on geotree(parent_geonode_id)")
        # CONSTRAINTS
    
    def stlocds(self):
        "contains language specific to store detailed information"
        cursor.execute("""create table stlocds(
            stlocds_id serial not null,
            stloc_id integer not null,
            language_id integer not null,
            name varchar(128)not null,
            description varchar(2000),
            image1 varchar(254),
            image2 varchar(254),
            field1 varchar(2000),
            field2 varchar(2000),
            field3 varchar(2000),
            primary key(stlocds_id)
        )""")
        cursor.execute("create unique index i0001214 on stlocds(stloc_id,language_id)")
        # CONSTRAINTS

    def stlocattr(self):
        "holds language specific store searchable attributes"
        cursor.execute("""create table stlocattr(
            stlocattr_id serial not null,
            language_id integer not null,
            stloc_id integer not null,
            name varchar(64)not null,
            displayname varchar(2000),
            value varchar(128)not null,
            displayvalue varchar(2000),
            image varchar(254),
            displayable smallint not null default 1,
            sequence float,
            primary key(stlocattr_id)
        )""")
        cursor.execute("create unique index i0001212 on stlocattr(stloc_id,name,language_id)")
        cursor.execute("create index i0001213 on stlocattr(value)")
        # CONSTRAINTS

    def stqotcfg(self):
        "this table is used to config the quote on a store entity"
        cursor.execute("""create table stqotcfg(
            storeent_id integer not null,
            retireflag integer default 1,
            csrexpireperiod bigint default 5184000,
            cssexpireperiod bigint default -1,
            expireperiod bigint default 2592000,
            primary key(storeent_id)
        )""")
        # CONSTRAINTS:
    
    def orders(self):
        "each row in this table represents an order in a store"
        cursor.execute("""create table orders(
            orders_id bigint not null,
            ormorder char(30),
            orgentity_id bigint,
            totalproduct decimal(20,5)default 0,
            totaltax decimal(20,5)default 0,
            totalshipping decimal(20,5)default 0,
            totaltaxshipping decimal(20,5)default 0,
            description varchar(254),
            storeent_id integer not null,
            currency char(10),
            locked char(1),
            timeplaced timestamp,
            lastupdate timestamp,
            sequence float not null default 0,
            status varchar(3),
            member_id bigint not null,
            field1 integer,
            address_id bigint,
            field2 decimal(20,5),
            providerordernum integer,
            shipascomplete char(1)not null default 'Y',
            field3 varchar(254),
            totaladjustment decimal(20,5)default 0,
            ordchnltyp_id bigint,
            comments varchar(254),
            notificationid bigint,
            type char(3),
            editor_id bigint,
            buschn_id integer,
            sourceid bigint,
            expiredate timestamp,
            blocked smallint default 0,
            opsystem_id smallint,
            transferstatus smallint,
            buyerpo_id bigint,
            primary key(orders_id)
        )""")
        cursor.execute("create index i0000176 on orders(member_id,status,storeent_id)")
        cursor.execute("create index i0000652 on orders(address_id)")
        cursor.execute("create index i0000653 on orders(orgentity_id)")
        cursor.execute("create index i0000654 on orders(storeent_id)")
        cursor.execute("create index i0000892 on orders(editor_id)")
        cursor.execute("create index i0000933 on orders(sourceid)")
        cursor.execute("create index i0001267 on orders(buyerpo_id)")
        cursor.execute("create index i0001508 on orders(status,lastupdate)")
        cursor.execute("create index i173124 on orders(timeplaced)")
        # CONSTRAINTS
    
    def ordchnltyp(self):
        cursor.execute("""create table ordchnltyp(
            ordchnltyp_id bigserial not null,
            paymenttranstype char(4),
            lastupdate timestamp,
            name varchar(200),
            primary key(ordchnltyp_id)
        )""")
        cursor.execute("create unique index i0000172 on ordchnltyp(name)")
    
    def buyerpo(self):
        """each row of this table represents a purchase order number.
        it is that the buyer organization of the account has defined
        or used for trading with the seller organization. the number is only unique within the account."""
        cursor.execute("""create table buyerpo(
            buyerpo_id bigserial not null,
            setccurr char(3),
            account_id bigint,
            ponumber varchar(128)not null,
            buyerpotyp_id integer not null,
            state integer default 0,
            amount decimal(20,5),
            primary key(buyerpo_id)
        )""")
        cursor.execute("create index i0000488 on buyerpo(account_id)")
        cursor.execute("create index i0000489 on buyerpo(buyerpotyp_id)")
        # CONSTRAINTS:
    
    def buyerpotyp(self):
        """the buyer purchase order type table.
        this table defines the different types of buyer purchase order"""
        cursor.execute("""create table buyerpotyp(
            buyerpotyp_id serial not null,
            primary key(buyerpotyp_id)
        )""")

if __name__=="__main__":
        s=Stores()
        # s.buyerpotyp()
        # s.opsystem()
        # s.ordchgrsn()
        # s.ordchgrsnds()
        # s.ordchnltyp()
        # s.repdlvry()
        # s.staddress()
        # s.storblkrsn()
        # s.store()
        # s.storecgry()
        # s.storecgrydesc()
        # s.storedef()
        # s.storeent()
        # s.storeentds()
        # s.storegrp()
        # s.storelang()
        # s.storelangds()
        # s.storembrgrp()
        # s.storerel()
        # s.stqotcfg()
        # s.stloc()
        # s.stlocds()
        # s.stlocattr()
        # s.geonode()
        # s.geondds()
        # s.geotree()
        # s.streltyp()
        # s.tickler()
        # s.tklacthist()
        # s.tklractdsc()
        # s.tklraction()
        # s.tklrreason()
        # s.tklrrsndsc()
