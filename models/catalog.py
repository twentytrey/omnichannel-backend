from db_con import createcon
con,cursor=createcon("retail","jmso","localhost","5432")
con.autocommit=True
from functions import build_constraint

class Attachment:
    """the attachment shows the relationship between database tables that
    contain information about attachments."""
    def attachusg(self):
        "the attachment usage table"
        cursor.execute("""create table attachusg(
            attachusg_id char(64)not null,
            primary key(attachusg_id)
        )""")
    
    def atchtgt(self):
        """this table holds information about the target which is used to
        hold a collection of assets, for use as an attachment target"""
        cursor.execute("""create table atchtgt(
            atchtgt_id bigserial not null,
            storeent_id integer not null default 0,
            member_id bigint not null,
            identifier varchar(128)not null,
            attachusg_id char(64),
            markfordelete integer not null default 0,
            field1 bigint,
            field2 float,
            field3 varchar(254),
            field4 varchar(254),
            primary key(atchtgt_id)
        )""")
        cursor.execute("create unique index i0000854 on atchtgt(storeent_id,member_id,identifier)")
        cursor.execute("create index i0000862 on atchtgt(storeent_id)")
        cursor.execute("create index i0000863 on atchtgt(member_id)")
        cursor.execute("create index i0000864 on atchtgt(attachusg_id)")
        # CONSTRAINTS:

    def atchtgtdsc(self):
        "holds the description of an attachment target"
        cursor.execute("""create table atchtgtdsc(
            atchtgtdsc_id bigint not null,
            atchtgt_id bigint not null,
            language_id integer not null,
            name varchar(128),
            shortdescription varchar(254),
            longdescription varchar(4000),
            primary key(atchtgtdsc_id)
        )""")
        cursor.execute("create unique index i0000855 on atchtgtdsc(atchtgt_id,language_id)")
        cursor.execute("create index i0000865 on atchtgtdsc(atchtgt_id)")
        cursor.execute("create index i0000866 on atchtgtdsc(language_id)")
        cursor.execute("create index i0001208 on atchtgtdsc(name)")
        # CONSTRAINTS

    def atchast(self):
        "this table holds metadata for the attachment in the attachment target."
        cursor.execute("""create table atchast(
            atchast_id bigserial not null,
            storeent_id integer not null,
            atchtgt_id bigint not null,
            atchastpath varchar(256),
            directorypath varchar(128),
            mimetype varchar(254),
            mimetypeencoding varchar(128),
            timecreated timestamp,
            timeupdate timestamp,
            image1 varchar(254),
            image2 varchar(254),
            primary key(atchast_id)
        )""")
        cursor.execute("create unique index i0000857 on atchast(storeent_id,atchtgt_id,atchastpath)")
        cursor.execute("create index i0000867 on atchast(storeent_id)")
        cursor.execute("create index i0000868 on atchast(atchtgt_id)")
        # CONSTRAINT

    def atchastlg(self):
        "this table holds the attachment asset to language relationship"
        cursor.execute("""create table atchastlg(
            atchastlg_id bigserial not null,
            atchast_id bigint not null,
            language_id integer,
            primary key(atchastlg_id)
        )""")
        cursor.execute("create unique index i0000859 on atchastlg(atchast_id,language_id)")
        cursor.execute("create index i0000871 on atchastlg(atchast_id)")
        cursor.execute("create index i0000872 on atchastlg(language_id)")
        # CONSTRAINTS:

    def atchrel(self):
        """this table holds the attachment relation between a business object
        and an attachment target"""
        cursor.execute("""create table atchrel(
            atchrel_id bigserial not null,
            object_id char(64)not null,
            atchobjtyp_id integer not null,
            atchtgt_id bigint not null,
            atchrlus_id integer not null,
            lastupdate timestamp,
            sequence float not null default 0,
            bigintobject_id bigint,
            primary key(atchrel_id)
        )""")
        cursor.execute("create unique index i0000860 on atchrel(atchobjtyp_id,object_id,atchrlus_id,atchtgt_id)")
        cursor.execute("create index i0000873 on atchrel(atchobjtyp_id)")
        cursor.execute("create index i0000874 on atchrel(atchtgt_id)")
        cursor.execute("create index i0000877 on atchrel(atchrlus_id)")
        cursor.execute("create index i0001207 on atchrel(bigintobject_id)")
        # CONSTRAINT

    def atchobjtyp(self):
        """this table holds the information about the types of business objects
        that are configured to have attachments. for example, attachments can be associated
        with catalog,catgroup,and catentry business objects."""
        cursor.execute("""create table atchobjtyp(
            atchobjtyp_id serial not null,
            identifier char(32)not null,
            sequence float not null default 0,
            description varchar(254),
            primary key(atchobjtyp_id)
        )""")
        cursor.execute("create unique index i0000853 on atchobjtyp(identifier)")

    def atchrlus(self):
        """this table holds usage information for attachment
        relations. for example an attachment can be a warranty document
        related to a product.in this case the usage is warranty"""
        cursor.execute("""create table atchrlus(
            atchrlus_id serial not null,
            identifier varchar(254),
            image varchar(254),
            sequence float,
            primary key(atchrlus_id)
        )""")
        cursor.execute("create unique index i0000878 on atchrlus(identifier)")

    def atchrlusds(self):
        "holds the description of an attachment relation usage"
        cursor.execute("""create table atchrlusds(
            atchrlusds_id serial not null,
            atchrlus_id integer not null,
            language_id integer not null,
            name varchar(128),
            shortdescription varchar(254),
            longdescription varchar(4000),
            primary key(atchrlus_id)
        )""")
        cursor.execute("create unique index i0000879 on atchrlusds(atchrlus_id,language_id)")
        # CONSTRAINTS:

    def atchreldsc(self):
        "this is a description for an attachment relation"
        cursor.execute("""create table atchreldsc(
            atchreldsc_id bigserial not null,
            atchrel_id bigint not null,
            language_id integer not null,
            name varchar(128),
            shortdescription varchar(254),
            longdescription varchar(4000),
            primary key(atchreldsc_id)
        )""")
        cursor.execute("create unique index i0000861 on atchreldsc(atchrel_id,language_id)")
        cursor.execute("create index i0000875 on atchreldsc(atchrel_id)")
        cursor.execute("create index i0000876 on atchreldsc(language_id)")
        # CONSTRAINTS

class Attribute:
    """the attribute data model sows the relationship between database tables
    that contain information about product attributes. attributes
    can be one of several types, identified by the attrtype column."""
    def attribute(self):
        """this table holds catalog entry attributes used for descriptive or SKU
        resolution purposes. an attribute stored in this table is for single
        catalog entry and is not shared between catalog entries. attribute
        dictionary attributes are stored in the attr table."""
        cursor.execute("""create table attribute(
            attribute_id bigserial not null,
            language_id integer not null,
            attrtype_id char(16)not null,
            name varchar(254),
            sequence float not null default 0,
            description varchar(254),
            catentry_id bigint,
            field1 varchar(254),
            usage char(1)default '1',
            qtyunit_id char(16),
            groupname varchar(64),
            noteinfo varchar(64),
            multitype char(1),
            primary key(attribute_id,language_id)
        )""")
        cursor.execute("create unique index i0000019 on attribute(catentry_id,language_id,name)")
        cursor.execute("create index i0000298 on attribute(groupname,sequence)")
        # CONSTRAINTS
    
    def attrtype(self):
        "holds the type identifier for product attributes"
        cursor.execute("""create table attrtype(
            attrtype_id char(16)not null,
            description varchar(254),
            oid varchar(64),
            primary key(attrtype_id)
        )""")
    
    def fill_attrtype(self):
        attrtypes=[{'attrtype_id':'INTEGER','desc':'Integer'},{'attrtype_id':'STRING','desc':'String or Text'},
        {'attrtype_id':'FLOAT','desc':'Floating point'},{'attrtype_id':'DATETIME','desc':'Date / Time values'},
        {'attrtype_id':'BIGINT','desc':'Big Integer'}]
        for attrtype in attrtypes:
            cursor.execute("""insert into attrtype(attrtype_id,description)values(%s,%s) returning attrtype_id""",
            (attrtype['attrtype_id'],attrtype['desc'],));con.commit()
    
    def attrvalue(self):
        """this table holds values assigned to product attributes
        and relates them back to catalog entries for SKU resolution"""
        cursor.execute("""create table attrvalue(
            attrvalue_id bigserial not null,
            language_id integer not null,
            attribute_id bigint not null,
            attrtype_id char(16)not null,
            stringvalue char(254),
            operator_id integer,
            sequence float not null default 0,
            integervalue integer,
            floatvalue float,
            catentry_id bigint not null,
            name varchar(254),
            field1 integer,
            image1 varchar(254),
            image2 varchar(254),
            field2 varchar(254),
            field3 varchar(254),
            qtyunit_id char(16),
            attachment_id bigint,
            primary key(attrvalue_id,language_id)
        )""")
        cursor.execute("create unique index i0000020 on attrvalue(attribute_id,catentry_id,language_id,name)")
        cursor.execute("create unique index i0000021 on attrvalue(attribute_id,catentry_id,stringvalue,language_id,integervalue,floatvalue)")
        cursor.execute("create index i0000453 on attrvalue(catentry_id)")
        cursor.execute("create index i0001235 on attrvalue(attachment_id)")
        cursor.execute("create index i0001236 on attrvalue(attribute_id,language_id)")
        cursor.execute("create index i194153 on attrvalue(attrtype_id,catentry_id,language_id,sequence)")
        # CONSTRAINTS
    
    def operator(self):
        "this table is used to define operators"
        cursor.execute("""create table operator(
            operator_id serial not null,
            operator char(32)not null,
            operatortype char(1)not null default '1',
            primary key(operator_id)
        )""")
    
    def operatrdsc(self):
        "language-dependent descriptions for an operator"
        cursor.execute("""create table operatrdsc(
            operator_id integer not null,
            language_id integer not null,
            description varchar(254),
            primary key(operator_id,language_id)
        )""")
        # CONSTRAINTS

class Catalog:
    """the catalog data model shows the relationship between database tables
    that contain information about a catalog."""
    def catalog(self):
        "holds information related to a catalog."
        cursor.execute("""create table catalog(
            catalog_id bigserial not null,
            member_id bigint not null,
            identifier varchar(254)not null,
            description varchar(254),
            tpclevel integer,
            primary key(catalog_id)
        )""")
        cursor.execute("create unique index i0000061 on catalog(member_id,identifier)")
        # CONSTRAINTS:
    
    def catalogdsc(self):
        "table holds language-dependent information realted to a catalog"
        cursor.execute("""create table catalogdsc(
            catalog_id bigint not null,
            language_id integer not null,
            name varchar(254)not null,
            shortdescription varchar(254),
            longdescription varchar(4000),
            thumbnaiol varchar(254),
            fullimage varchar(254),
            primary key(language_id,catalog_id)
        )""")
        cursor.execute("create index i0000512 on catalogdsc(catalog_id)")
        # CONSTRAINTS
    
    def catgroup(self):
        """this table holds the information related to a catalog group.
        a catalog group is similar to a generic category that can both contain
        other catalog groups and also catalog entries."""
        cursor.execute("""create table catgroup(
            catgroup_id bigserial not null,
            member_id bigint not null,
            identifier varchar(254),
            markfordelete integer not null default 0,
            lastupdate timestamp,
            field1 varchar(254),
            field2 varchar(254),
            rank float,
            dynamic integer default 0,
            primary key(catgroup_id)
        )""")
        cursor.execute("create unique index i0000067 on catgroup(identifier,member_id)")
        cursor.execute("create index i0000376 on catgroup(rank)")
        cursor.execute("create index i0000525 on catgroup(member_id)")
        # CONSTRAINTS
    
    def cattogrp(self):
        "table identifies the root catalog groups or root categories contained witin a catalog"
        cursor.execute("""create table cattogrp(
            catalog_id bigint not null,
            catgroup_id bigint not null,
            lastupdate timestamp,
            sequence float,
            catalog_id_link bigint,
            primary key(catalog_id,catgroup_id)
        )""")
        cursor.execute("create index i0000373 on cattogrp(catalog_id_link)")
        cursor.execute("create index i0000532 on cattogrp(catgroup_id)")
        # CONSTRAINTS
    
    def catgrprel(self):
        """this table relates catalog groups to child catalog groups.
        you can use this table to dictate the navigational flow from 
        catalog groups to child catalog groups. each relationship is also
        qualified by a catalog ID."""
        cursor.execute("""create table catgrprel(
            catgroup_id_parent bigint not null,
            catgroup_id_child bigint not null,
            catalog_id bigint not null,
            rule varchar(254),
            sequence float not null default 0,
            lastupdate timestamp,
            catalog_id_link bigint,
            primary key(catgroup_id_child,catgroup_id_parent,catalog_id)
        )""")
        cursor.execute("create index i0000294 on catgrprel(catalog_id_link)")
        cursor.execute("create index i0000527 on catgrprel(catalog_id)")
        cursor.execute("create index i0000528 on catgrprel(catgroup_id_parent)")
        # CONSTRAINTS
    
    def catgpenrel(self):
        """this table relates catalog groups or categories to the catalog entries that are
        inside them. you can also use this table to dictate the navigational flow from catalog
        groups to catalog entries. each relationship is also qualified by a catalog ID"""
        cursor.execute("""create table catgpenrel(
            catgroup_id bigint not null,
            catalog_id bigint not null,
            catentry_id bigint not null,
            rule varchar(254),
            sequence float not null default 0,
            lastupdate timestamp,
            field1 varchar(254),
            field2 integer,
            field3 decimal(20,5),
            primary key(catgroup_id,catentry_id,catalog_id)
        )""")
        cursor.execute("create index i0000523 on catgpenrel(catalog_id)")
        cursor.execute("create index i0000524 on catgpenrel(catentry_id)")
        cursor.execute("create index i0001546 on catgpenrel(catgroup_id,catalog_id,catentry_id)")
        # CONSTRAINTS
    
    def catentry(self):
        """this table holds the information related to a catlog entry.
        examples of catalog entries include products, items packages and bundles."""
        cursor.execute("""create table catentry(
            catentry_id bigserial not null,
            member_id bigint not null,
            itemspc_id bigint,
            catenttype_id char(16)not null,
            partnumber varchar(64)not null,
            mfpartnumber varchar(64),
            mfname varchar(254),
            markfordelete integer not null default 0,
            url varchar(254),
            field1 integer,
            field2 integer,
            lastupdate timestamp,
            field3 decimal(20,5),
            onspecial integer,
            onauction integer,
            field4 varchar(254),
            field5 varchar(254),
            buyable integer,
            baseitem_id bigint,
            state char(1)default '1',
            startdate timestamp,
            enddate timestamp,
            rank float,
            availabilitydate timestamp,
            lastorderdate timestamp,
            endofservicedate timestamp,
            discontinuedate timestamp,
            primary key(catentry_id)
        )""")
        cursor.execute("create unique index i0000064 on catentry(partnumber,member_id)")
        cursor.execute("create index i0000065 on catentry(catentry_id,markfordelete)")
        cursor.execute("create index i0000305 on catentry(buyable,catentry_id,catenttype_id)")
        cursor.execute("create index i0000375 on catentry(rank)")
        cursor.execute("create index i0000518 on catentry(catenttype_id)")
        cursor.execute("create index i0000519 on catentry(member_id)")
        cursor.execute("create index i263103 on catentry(catentry_id,catenttype_id)")
        cursor.execute("create index i263121 on catentry(itemspc_id)")
        cursor.execute("create index i263122 on catentry(baseitem_id)")
        # CONSTRAINTS:
    
    def catgrptpc(self):
        """this table relates master catalogs with trading position containers.
        each catalog entry belonging to the indicated master catalog must have
        a standard price offer supplied for the specified trading position container"""
        cursor.execute("""create table catgrptpc(
            catalog_id bigint not null,
            catgroup_id bigint not null default 0,
            tradeposcn_id bigint not null,
            store_id integer not null default 0,
            primary key(catalog_id,catgroup_id,tradeposcn_id,store_id)
        )""")
        cursor.execute("create index i0000529 on catgrptpc(tradeposcn_id)")
        cursor.execute("create index i0000530 on catgrptpc(store_id)")
        cursor.execute("create index i0000531 on catgrptpc(catgroup_id)")
        # CONSTRAINTS
    
    def catgrprule(self):
        "relates a category to a web activity."
        cursor.execute("""create table catgrprule(
            catgroup_id bigint not null,
            dmactivity_id integer not null,
            evaltime timestamp,
            showafter smallint not null default 0,
            evaluating smallint not null default 0,
            primary key(catgroup_id,dmactivity_id)
        )""")
        cursor.execute("create index i0001520 on catgrprule(dmactivity_id)")
        # CONSTRAINT
    
    def storedefcat(self):
        "holds the relationship between store and the default catalog."
        cursor.execute("""create table storedefcat(
            storedefcat_id bigserial not null,
            storeent_id integer not null,
            catalog_id bigint not null,
            field1 integer,
            field2 varchar(256),
            field3 varchar(256),
            primary key(storedefcat_id)
        )""")
        cursor.execute("create index i0001439 on storedefcat(storeent_id,catalog_id)")
        cursor.execute("create index i0001440 on storedefcat(catalog_id)")
        # CONSTRAINT
    
    def storecat(self):
        "holds the relationship between storeentities and catalogs that they offer."
        cursor.execute("""create table storecat(
            catalog_id bigint not null,
            storeent_id integer not null,
            mastercatalog char(1),
            lastupdate timestamp,
            primary key(catalog_id,storeent_id)
        )""")
        cursor.execute("create index i0000782 on storecat(storeent_id)")
        # CONSTRAINTS
    
class Catentry:
    """the catalog entry data model shows the relationsip between database tables
    that contain informtion about a catalog entry."""
    def baseitem(self):
        """base items represent a general family of goods
        with a common name and description. baseitems are used
        exclusively for fulfillment. each catalog entry that 
        represents a product in the catalog has a corresponding baseitem for 
        fulfillment purposes."""
        cursor.execute("""create table baseitem(
            baseitem_id bigserial not null,
            baseitem_name varchar(254)not null,
            member_id bigint not null,
            itemtype_id char(4)not null,
            quantitymeasure char(16)not null default 'C62',
            lastupdate timestamp,
            markfordelete integer not null default 0,
            partnumber varchar(72)not null,
            quantitymultiple float not null default 1.0,
            primary key(baseitem_id)
        )""")
        cursor.execute("create unique index i0000040 on baseitem(member_id,baseitem_name)")
        # CONSTRAINTS:

    def itemspc(self):
        """information about specified items. a specified item is a product
        with values for all of its attributes. a specified item could correspond to 
        a 2L bottle of mill, with 2% fat content. a specified item is the customer view of the goods"""
        cursor.execute("""create table itemspc(
            itemspc_id bigserial not null,
            lastupdate timestamp,
            member_id bigint not null,
            markfordelete integer not null default 0,
            baseitem_id bigint,
            discontinued char(1)not null default 'N',
            partnumber varchar(64)not null,
            primary key(itemspc_id)
        )""")
        cursor.execute("create unique index i0000138 on itemspc(partnumber,member_id)")
        cursor.execute("create index i0000139 on itemspc(baseitem_id,itemspc_id)")
        cursor.execute("create index i0000361 on itemspc(itemspc_id,baseitem_id,partnumber)")
        cursor.execute("create index i0000599 on itemspc(member_id)")
        cursor.execute("create index i800140 on itemspc(discontinued)")
        # CONSTRAINTS
    
    def catentrel(self):
        """this table holds containment relationshops between catalog entries.
        examples of these relationships are product-item, bundle and package
        relationshops. the table should not be used for a peer-to-peer
        catalo relationship such as cross-sells"""
        cursor.execute("""create table catentrel(
            catentry_id_parent bigint not null,
            catreltype_id char(32)not null,
            catentry_id_child bigint not null,
            sequence float not null default 0,
            quantity float,
            groupname varchar(254),
            field1 varchar(254),
            field2 integer,
            field3 decimal(20,5),
            mandatory char(3),
            primary key(catreltype_id,catentry_id_parent,catentry_id_child)
        )""")
        cursor.execute("create index i0000365 on catentrel(catentry_id_child,catreltype_id)")
        cursor.execute("create index i0000517 on catentrel(catentry_id_parent)")
        # CONSTRAINTS:
    
    def catreltype(self):
        """this table describes the types of containment relationships
        between catalog entries, such as types for productitems,
        and packagecomponents."""
        cursor.execute("""create table catreltype(
            catreltype_id char(32)not null,
            description varchar(254),
            field1 integer,
            field2 decimal(20,5),
            field3 varchar(254),
            primary key(catreltype_id)
        )""")
    
    def listprice(self):
        """each row of this table represents a listprice in a
        particular curency for a catalog entry/"""
        cursor.execute("""create table listprice(
            catentry_id bigint not null,
            currency char(3)not null,
            listprice decimal(20,5)not null,
            oid varchar(64),
            primary key(currency,catentry_id)
        )""")
        cursor.execute("create index i0000145 on listprice(currency,catentry_id,listprice)")
        cursor.execute("create index i0000604 on listprice(catentry_id)")
        # CONSTRAINTS:
    
    def catentship(self):
        """each row of this table contains information about how a product represented
        by a catalog entry is packaged. the information can be used to determine prices,
        discounts, shipping charges and taxes."""
        cursor.execute("""create table catentship(
            catentry_id bigint not null,
            weight float,
            weightmeasure char(16),
            length float,
            width float,
            height float,
            sizemeasure char(16),
            nominalquantity float not null default 1.0,
            quantitymultiple float not null default 1.0,
            quantitymeasure char(16)not null default 'C62',
            primary key(catentry_id)
        )""")
        # CONSTRAINTS:
    
    def storecent(self):
        """this table holds the relationship between storeentities
        and catalog entries that they can display and process."""
        cursor.execute("""create table storecent(
            storeent_id integer not null,
            catentry_id bigint not null,
            primary key(storeent_id,catentry_id)
        )""")
        cursor.execute("create index i0000345x on storecent(catentry_id)")
        # CONSTRAINTS:
    
    def storecatovrgrp(self):
        """this table is used to hold the relationship between the store entities
        and catalog override groups they can use to display the catalog in the store front"""
        cursor.execute("""create table storecatovrgrp(
            storeent_id integer not null,
            catovrgrp_id bigint not null,
            sequence float not null default 0,
            primary key(catovrgrp_id,storeent_id)
        )""")
        cursor.execute("create index i0001452 on storecatovrgrp(storeent_id)")
        # CONSTRAINTS
    
    def catovrgrp(self):
        """this table holds information realted to the catalog
        override group. the catalog override group is a container to
        group different catalog override."""
        cursor.execute("""create table catovrgrp(
            catovrgrp_id bigserial not null,
            member_id bigint not null,
            identifier varchar(254) not null,
            storeent_id integer not null,
            primary key(catovrgrp_id)
        )""")
        cursor.execute("create unique index i0001450 on catovrgrp(identifier,member_id)")
        cursor.execute("create index i0001451 on catovrgrp(storeent_id)")
        # CONSTRAINTS
    
    def catentattr(self):
        """this table is deprecated and is provided for backward compatibility only.
        attrubutes in this table should be migrated to the attribute and attrvalue tables
        as descriptive attributes. attruibute table should not be a null,0 or 1"""
        cursor.execute("""create table catentattr(
            catentattr_id bigserial not null,
            language_id integer not null,
            catentry_id bigint not null,
            name varchar(254)not null,
            value varchar(254)not null,
            description varchar(254),
            field1 integer,
            fiel2 varchar(254),
            field3 varchar(254),
            primary key(catentattr_id)
        )""")
        cursor.execute("create unique index i0000063 on catentattr(catentry_id,language_id,name)")
        # CONSTRAINTS:
    
    def catentdesc(self):
        # spelling errors
        cursor.execute("""create table catentdesc(
            catentry_id bigint not null,
            language_id integer not null,
            name varchar(128),
            shortdesciption text,
            longdesctiption varchar(2500),
            thumbnail varchar(254),
            auxdescription1 varchar(4000),
            fullimage varchar(254),
            auxdescription2 varchar(4000),
            xmldetail text,
            avaialble integer,
            published integer not null,
            availabilitydate timestamp,
            primary key(catentry_id,language_id)
        )""")
        cursor.execute("create index i0000304 on catentdesc(language_id,catentry_id,name,published)")
        cursor.execute("create index i0001196 on catentdesc(name,language_id,published)")
        cursor.execute("create index i0001248 on catentdesc(catentry_id)")
        # CONSTRAINTS
    
    def catenttype(self):
        """this table defines all possible types of catalog entries.
        examples of catalog entry types are catalogentrybean,productbean
        itembean,packagebean,bundlebean,dynamickitbean,and preddynakitbean"""
        cursor.execute("""create table catenttype(
            catenttype_id char(16)not null,
            description varchar(254),
            oid varchar(64),
            primary key(catenttype_id)
        )""")
    
    def catentdescovr(self):
        """this table is used to store information about catalog entry
        description override. when a field of a record in this table contains the
        null value, this means there is no override for this field and the product
        on the store front should use the field from the asset store."""
        cursor.execute("""create table catentdescovr(
            catentdescovr_id bigserial not null,
            catentry_id bigint not null,
            language_id integer not null,
            catovrgrp_id bigint not null,
            name char(128),
            shortdescription varchar(254),
            longdescription text,
            thumbnail varchar(254),
            auxdescription1 varchar(4000),
            fullimage varchar(254),
            auxdescription2 varchar(4000),
            published integer,
            field1 integer,
            field2 varchar(254),
            field3 varchar(254),
            primary key(catentdescovr_id)
        )""")
        cursor.execute("create unique index i0001446 on catentdescovr(catentry_id,language_id,catovrgrp_id)")
        cursor.execute("create index i0001448 on catentdescovr(catovrgrp_id)")
        cursor.execute("create index i0001447 on catentdescovr(language_id)")
        cursor.execute("create index i0001449 on catentdescovr(catentry_id,catovrgrp_id)")
        # CONSTRAINTS

    def outputq(self):
        cursor.execute("""create table outputq(
            outputq_id bigserial not null,
            outputqtype char(4),
            lastupdate timestamp,
            name varchar(60),
            primary key(outputq_id)
        )""")
        cursor.execute("create unique index i0000183 on outputq(name)")

    def versionspc(self):
        "each row defines the relationship between a product version and specified item"
        cursor.execute("""create table versionspc(
            versionspc_id bigserial not null,
            itemspc_id bigint not null,
            itemversn_id bigint not null,
            lastupdate timestamp,
            primary key(versionspc_id)
        )""")
        cursor.execute("create unique index i0000264 on versionspc(itemspc_id,itemversn_id)")
        cursor.execute("create unique index i0000363 on versionspc(versionspc_id,itemspc_id)")
        cursor.execute("create index i0001293 on versionspc(itemversn_id)")
        # CONSTRAINT
        cursor.execute(build_constraint("versionspc","f_905","itemspc_id","itemspc","itemspc_id"))
        cursor.execute(build_constraint("versionspc","f_906","itemversn_id","itemversn","itemversn_id"))
    
    def itemversn(self):
        """each row of this table represents an item version for a base item
        an itemversion expired when its expiration date is in the past.
        each baseitem must only have a single itemversion defined."""
        cursor.execute("""create table itemversn(
            itemversn_id bigserial not null,
            lastupdate timestamp,
            baseitem_id bigint not null,
            expirationdate timestamp not null,
            versionname char(30)not null default 'Version 1',
            primary key(itemversn_id)
        )""")
        cursor.execute("create unique index i0000140 on itemversn(baseitem_id,expirationdate)")
        cursor.execute("create unique index i0000141 on itemversn(baseitem_id,versionname)")
        # CONSTRAINT
        cursor.execute(build_constraint("itemversn","f_408","baseitem_id","baseitem","baseitem_id"))

    def enter_itemtype(self):
        itemtypes=[{'itemtype_id':'ITEM','description':'An item is a tangible unit of merchandise that has a specific name, part number, and price. For example, a small black shirt is an item while a shirt is a product. '},
        {'itemtype_id':'DNKT','description':"A dynamic kit is a type of catalog entry which can be dynamically configured by the customer. This configuration (or grouping) of products is based on the customer's requirements and is sold as a single unit."},
        {'itemtype_id':'STKT','description':"A static kit is a group of products that are ordered as a unit. The information about the products that are contained in a static kit is predefined and controlled within the system. The individual components within the order cannot be modified and must be fulfilled together."}]
        for item in itemtypes:
            cursor.execute("""insert into itemtype(itemtype_id,description)values(%s,%s)
            returning itemtype_id""",(item['itemtype_id'],item['description'],))
    
    def enter_catenttype(self):
        catenttypes=[
            {'catenttype_id':'Product','description':'Product',},
            {'catenttype_id':'Item','description':'Item'},
            {'catenttype_id':'Package','description':'Package'},
            {'catenttype_id':'Bundle','description':'Bundle'},
            {'catenttype_id':'DynamicKit','description':'DynamicKit'},
            {'catenttype_id':'PredDynaKit','description':'Predefined Dynamic Kit'}]
        for catenttype in catenttypes:
            cursor.execute("""insert into catenttype(catenttype_id,description)values(%s,%s)returning catenttype_id""",
            (catenttype['catenttype_id'],catenttype['description'],))

class CatalogGroup:
    """this catalog group data model shows the relationship
    between database tables that contain information about catalog groups."""
    def catgrpdesc(self):
        """this table holds the lang-dependent information
        related to a catalog group."""
        cursor.execute("""create table catgrpdesc(
            language_id integer not null,
            catgroup_id bigint not null,
            name varchar(254)not null,
            shortdescription varchar(254),
            longdescription varchar(4000),
            thumbnail varchar(254),
            fullimage varchar(254),
            published integer not null,
            display varchar(254),
            note varchar(4000),
            primary key(catgroup_id,language_id)
        )""")
        # CONSTRAINTS
    
    def catgrpattr(self):
        cursor.execute("""create table catgrpattr(
            catgrpattr_id bigserial not null,
            language_id integer not null,
            catgroup_id bigint not null,
            name varchar(254)not null,
            description varchar(254),
            sequence float,
            primary key(language_id,catgrpattr_id)
        )""")
        cursor.execute("create unique index i0000068 on catgrpattr(catgroup_id,language_id,name)")
        # CONSTRAINT:

    def storecgrp(self):
        """this table holds the relationship between storeentities
        and cataloggroups that they can display and process."""
        cursor.execute("""create table storecgrp(
            storeent_id integer not null,
            catgroup_id bigint not null,
            primary key(storeent_id,catgroup_id)
        )""")
        cursor.execute("create index i0000783 on storecgrp(catgroup_id)")
        # CONSTRAINTS
    
    def catgrpps(self):
        """this table relates catalo groups to product sets.
        every catalog entry under the catalog subtree for this catalog group
        is a member of the specified product set"""
        cursor.execute("""create table catgrpps(
            catalog_id bigint not null,
            catgroup_id bigint not null,
            productset_id integer not null,
            usage char(1),
            primary key(catalog_id,catgroup_id,productset_id)
        )""")
        cursor.execute("create index i0000291 on catgrpps(catalog_id,catgroup_id,usage)")
        cursor.execute("create index i0000292 on catgrpps(productset_id,usage)")
        cursor.execute("create index i0000526 on catgrpps(catgroup_id)")
        # CONSTRAINTS
    
class MerchandiseAssociation:
    """the merchandising association data model shows the
    relationship between database tables that contain information
    about merchandising associations."""
    def massoc(self):
        """this table holds all of the possible specifiers
        that can be used when associating catalog objects."""
        cursor.execute("""create table massoc(
            massoc_id char(32)not null,
            description varchar(254),
            oid varchar(64),
            primary key(massoc_id)
        )""")
    
    def massoccece(self):
        "holds the merchandising associations that exist between catalog entries"
        cursor.execute("""create table massoccece(
            massoccece_id bigserial not null,
            massoctype_id char(32)not null,
            catentry_id_from bigint not null,
            rank decimal(20,5),
            catentry_id_to bigint not null,
            massoc_id char(32)not null,
            quantity float,
            rule varchar(254),
            groupname varchar(254),
            field1 varchar(254),
            field2 integer,
            field3 decimal(20,5),
            oid varchar(64),
            date1 timestamp,
            store_id integer not null default 0,
            primary key(massoccece_id)
        )""")
        cursor.execute("create unique index i0000148 on massoccece(store_id,massoctype_id,massoc_id,catentry_id_from,catentry_id_to)")
        cursor.execute("create index i0000370 on massoccece(catentry_id_from)")
        cursor.execute("create index i0000610 on massoccece(catentry_id_to)")
        # CONSTRAINTS
    
    def massoctype(self):
        """holds all of the possible types of associations that can exist between catalog objects"""
        cursor.execute("""create table massoctype(
            massoctype_id char(32)not null,
            description varchar(254),
            field1 integer,
            oid varchar(64),
            field2 decimal(20,5),
            field3 varchar(254),
            primary key(massoctype_id)
        )""")
    
    def massocgpgp(self):
        "this table holds the merchandising associations that exist between the catalog groups."
        cursor.execute("""create table massocgpgp(
            massocgpgp_id bigserial not null,
            catgroup_id_to bigint not null,
            catgroup_id_from bigint not null,
            massoctype_id char(32)not null,
            rank decimal(20,5),
            massoc_id char(32)not null,
            quantity float,
            rule char(254),
            groupname varchar(254),
            field1 varchar(254),
            field2 integer,
            field3 integer,
            date1 timestamp,
            store_id integer not null default 0,
            primary key(massocgpgp_id)
        )""")
        cursor.execute("create unique index i0000149 on massocgpgp(store_id,massoctype_id,massoc_id,catgroup_id_from,catgroup_id_to)")
        cursor.execute("create index i0000611 on massocgpgp(catgroup_id_from)")
        cursor.execute("create index i0000612 on massocgpgp(catgroup_id_to)")
        # CONSTRAINTS

    
class Package:
    """the package data model shows the relationship between database tables
    that contain information about packages. a package is a group of 
    items that are preselected for a fixed price. packages must be bought intact
    and cannot be broken down by the customer. if a package
    contains products with definiing attributes it must e associated to those attributes
    and their corresponding values."""
    def pkgattr(self):
        """this table holds package attributes. package attributes are
        inherited from the attributes of the products that are contained within"""
        cursor.execute("""create table pkgattr(
            pkgattr_id bigserial not null,
            attribute_id bigint not null,
            language_id integer not null,
            catentry_id bigint,
            oid char(32),
            primary key(pkgattr_id,language_id)
        )""")
        cursor.execute("create unique index i0000187 on pkgattr(catentry_id,language_id,attribute_id)")
        cursor.execute("create index i0001271 on pkgattr(attribute_id,language_id)")
        # CONSTRAINTS
    
    def pkgattrval(self):
        """this table holds the values assigned to the package attributes.
        package attribute values are inherited from the attribute values of the
        products that are contained within packages"""
        cursor.execute("""create table pkgattrval(
            pkgattrval_id bigserial not null,
            attrvalue_id bigint not null,
            language_id integer not null,
            catentry_id bigint not null,
            oid char(32),
            primary key(pkgattrval_id,language_id)
        )""")
        cursor.execute("create unique index i0000188 on pkgattrval(catentry_id,language_id,attrvalue_id)")
        cursor.execute("create index i0001272 on pkgattrval(attrvalue_id,language_id)")
        # CONSTRAINTS
    
class DynamicKit:
    """this dynamic kit data model shows the relationship between database tables that contain
    information about configurable products. these configurable products are dynamic kit
    catalog entries."""
    def oicomprel(self):
        """stores all kit level information for an Order item that is a kit.
        a kit may contain other kits and catalog entries outside of a kit.
        hoverver there is no storefront, tooling or server side support for kits that
        contain other kits. this table stores information about kit components and the 
        oicomplist table stores information about catalog"""
        cursor.execute("""create table oicomprel(
            oicomprel_id bigserial not null,
            orderitems_id bigint,
            itemspc_id bigint not null,
            parent_id bigint,
            required smallint default 1,
            configuration_id varchar(128),
            primary key(oicomprel_id)
        )""")
        cursor.execute("create index i0000963 on oicomprel(itemspc_id)")
        cursor.execute("create index i0000964 on oicomprel(parent_id)")
        cursor.execute("create index i0000966 on oicomprel(orderitems_id)")
        cursor.execute("create index i0001101 on oicomprel(configuration_id,orderitems_id)")
        # CONSTRAINTS
    
    def itemtype(self):
        "each row of tis table represents a type of baseitem."
        cursor.execute("""create table itemtype(
            itemtype_id char(14)not null,
            description varchar(254),
            oid varchar(64),
            primary key(itemtype_id)
        )""")
    
    def oicomplist(self):
        "each row contains information about the components of a configured order item"
        cursor.execute("""create table oicomplist(
            itemspc_id bigint,
            oicomplist_id bigint not null,
            catentry_id bigint,
            orderitems_id bigint,
            catalogquantity float,
            inventoryquantity integer,
            required char(1)default 'Y',
            configurationid varchar(128),
            unitprice decimal(20,5),
            currency char(3),
            supplierdata varchar(254),
            supplierpartnumber varchar(254),
            rfqprod_id bigint,
            oicomprel_id bigint,
            primary key(oicomplist_id)
        )""")
        cursor.execute("create index i0000301 on oicomplist(orderitems_id)")
        cursor.execute("create index i0000371 on oicomplist(rfqprod_id)")
        cursor.execute("create index i0000627 on oicomplist(catentry_id)")
        cursor.execute("create index i0000628 on oicomplist(itemspc_id)")
        cursor.execute("create index i0001100 on oicomplist(orderitems_id,configurationid)")
        cursor.execute("create index i0001263 on oicomplist(oicomprel_id)")
        # CONSTRAINTS
    
    def dkpdccomplist(self):
        "contains the components within a predefined configuration"
        cursor.execute("""create table dkpdccomplist(
            dkpdccomplist_id bigserial not null,
            dkpredefconf_id bigint not null,
            catentry_id bigint not null,
            groupname varchar(254),
            sequence float not null default 0,
            quantity float not null,
            qtyunit_id char(16),
            dkpdcrel_id bigint,
            primary key(dkpdccomplist_id)
        )""")
        cursor.execute("create unique index i0000414 on dkpdccomplist(dkpredefconf_id,catentry_id)")
        cursor.execute("create index i0000413 on dkpdccomplist(dkpdcrel_id)")
        cursor.execute("create index i000908 on dkpdccomplist(qtyunit_id)")
        cursor.execute("create index i0001256 on dkpdccomplist(catentry_id)")
        # CONSTRAINTS
    
    def catconfinf(self):
        """this table holds additional information for catalog entries
        that represent configurable products. this information may be 
        required by an external configurator to configure catalog entries"""
        cursor.execute("""create table catconfinf(
            catentry_id bigint not null,
            url varchar(254),
            reference varchar(4000),
            field1 integer,
            field2 float,
            field3 varchar(254),
            field4 varchar(254),
            field5 timestamp,
            configuration text,
            configurable smallint default 1,
            primary key(catentry_id)
        )""")
    
    def dkpdccatentrel(self):
        """contains relationships between predefined configurations and the
        dynamic kit catalog entries for which they are built"""
        cursor.execute("""create table dkpdccatentrel(
            dkpredefconf_id bigint not null,
            catentry_id bigint not null,
            sequence integer not null default 0,
            primary key(dkpredefconf_id,catentry_id)
        )""")
        cursor.execute("create index i0001255 on dkpdccatentrel(catentry_id)")
        # CONSTRAINTS
    
    def dkpredefconf(self):
        "contains predefined configurations of dynamic kit catalog entries"
        cursor.execute("""create table dkpredefconf(
            dkpredefconf_id bigserial not null,
            configuration_id varchar(256),
            complete smallint not null default 0,
            primary key(dkpredefconf_id)
        )""")

class Productset:
    """this data model shows the relationship between database tables
    that contian information about product sets."""
    def productset(self):
        """this table holds tje definition of a product set
        the actual representation of the product set is
        held in the prsetcerel table."""
        cursor.execute("""create table productset(
            name varchar(64),
            productset_id serial not null,
            member_id bigint not null,
            definition text,
            publishtime timestamp,
            markfordelete integer not null default 0,
            static char(1),
            primary key(productset_id)
        )""")
        cursor.execute("create unique index i0000191 on productset(name,member_id)")
        cursor.execute("create index i0000700 on productset(member_id)")
        # CONSTRAINTS
    
    def prodsetdsc(self):
        "lang-dependent information related to product sets"
        cursor.execute("""create table prodsetdsc(
            productset_id integer not null,
            language_id integer not null,
            description varchar(254),
            primary key(productset_id,language_id)
        )""")
    
    def prsetcerel(self):
        "this table holds the expanded form of a product set"
        cursor.execute("""create table prsetcerel(
            productset_id integer not null,
            catentry_id bigint not null,
            primary key(productset_id,catentry_id)
        )""")
        cursor.execute("create index i0000702 on prsetcerel(catentry_id)")
        # CONSTRAINTS
    
    def psetadjmnt(self):
        """this table stores information on product set adjustments.
        and shows which product set is referenced by a term and condition
        for a business policy."""
        cursor.execute("""create table psetadjmnt(
            termcond_id bigint not null,
            productset_id integer not null,
            type integer not null,
            adjustment decimal(20,5)not null default 0,
            precedence integer not null default 0,
            primary key(termcond_id,productset_id)
        )""")
        cursor.execute("create index i0000703 on psetadjmnt(productset_id)")
        # CONSTRAINTS
    
    def fill_catreltype(self):
        catreltypes=[dict(value='PRODUCT_ITEM',text='Product-Item'),dict(value='PACKAGE_COMPONENT',text='Package Component'),
        dict(value='BUNDLE_COMPONENT',text='Bundle Component'),dict(value='DYNAMIC_KIT_COMPONENT',text='Dynamic Kit Component')]
        for catreltype in catreltypes:
            cursor.execute("""insert into catreltype(catreltype_id,description)values(%s,%s)on conflict(catreltype_id)
            do update set catreltype_id=%s,description=%s returning catreltype_id""",(catreltype['value'],catreltype['text'],
            catreltype['value'],catreltype['text'],));con.commit()

if __name__=="__main__":
    p=Productset()
    p.prodsetdsc()
    p.prsetcerel()
    p.psetadjmnt()
    # p.fill_catreltype()

    d=DynamicKit()
    d.oicomprel()
    d.oicomplist()
    d.itemtype()
    d.dkpredefconf()
    d.dkpdccomplist()
    d.dkpdccatentrel()
    d.catconfinf()

    p=Package()
    p.pkgattrval()
    p.pkgattr()

    m=MerchandiseAssociation()
    m.massoctype()
    m.massocgpgp()
    m.massoccece()
    m.massoc()

    c=CatalogGroup()
    c.storecgrp()
    c.catgrpps()
    c.catgrpdesc()
    c.catgrpattr()

    c=Catentry()
    c.storecent()
    c.storecatovrgrp()
    c.listprice()
    c.itemspc()
    c.catreltype()
    c.catovrgrp()
    c.catenttype()
    c.catentship()
    c.catentrel()
    c.catentdescovr()
    c.catentdesc()
    c.catentattr()
    c.baseitem()
    c.itemversn()
    c.versionspc()
    c.outputq()
    # c.enter_itemtype()
    # c.enter_catenttype()

    c=Catalog()
    c.storedefcat()
    c.storecat()
    c.cattogrp()
    c.catgrptpc()
    c.catgrprule()
    c.catgrprel()
    c.catgroup()
    c.catgpenrel()
    c.catentry()
    c.catalogdsc()
    c.catalog()

    a=Attribute()
    a.operatrdsc()
    a.operator()
    a.attrvalue()
    a.attrtype()
    # a.fill_attrtype()
    a.attribute()

    a=Attachment()
    a.attachusg()
    a.atchtgtdsc()
    a.atchtgt()
    a.atchrlusds()
    a.atchrlus()
    a.atchreldsc()
    a.atchrel()
    a.atchobjtyp()
    a.atchastlg()
    a.atchast()
