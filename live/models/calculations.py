from db_con import con,cursor
from functions import build_constraint

class CalculationCode:
    """the calculation code data model shows the relationship
    between database tables that contain information about calculation
    codes."""
    def calcode(self):
        """a row in this table represents a calculationcode, calculationcodes
        represent ways of determining monetary amounts associated with 
        orderitems. they are also used to calculate discounts, shipping charges, 
        sales tax and shipping tax."""
        cursor.execute("""create table calcode(
            calcode_id serial not null,
            code char(128)not null,
            calusage_id integer not null,
            storeent_id integer not null,
            groupby integer not null default 0,
            txcdclass_id integer,
            published integer not null default 0,
            sequence float not null default 0,
            combination integer,
            lastupdate timestamp,
            calmethod_id integer not null,
            calmethod_id_app integer not null,
            calmethod_id_qfy integer not null,
            field1 varchar(254),
            description varchar(254),
            displaylevel integer not null default 0,
            startdate timestamp,
            enddate timestamp,
            flags integer not null default 0,
            precedence float not null default 0,
            primary key(calcode_id)
        )""")
        cursor.execute("create unique index i0000054 on calcode(calusage_id,code,description,storeent_id)")
        cursor.execute("create index i0000495 on calcode(calmethod_id_app)")
        cursor.execute("create index i0000496 on calcode(calmethod_id)")
        cursor.execute("create index i0000497 on calcode(calmethod_id_qfy)")
        cursor.execute("create index i0000498 on calcode(storeent_id)")
        cursor.execute("create index i001247 on calcode(txcdclass_id)")
        # CONSTRAINTS
    
    def calcodedesc(self):
        cursor.execute("""create table calcodedesc(
            calcode_id integer not null,
            language_id integer not null,
            description varchar(254),
            longdescription varchar(4000),
            primary key(calcode_id,language_id)
        )""")
        # CONSTRAINTS
    
    def calcodemgp(self):
        """the calculationcodequalifymethod can use the rows of the 
        table to restrict use of a calculationcode to members of certain
        member groups."""
        cursor.execute("""create table calcodemgp(
            calcode_id integer not null,
            mbrgrp_id bigint not null,
            primary key(calcode_id,mbrgrp_id)
        )""")
        cursor.execute("create index i0000499 on calcodemgp(mbrgrp_id)")
        # CONSTRAINTS
    
    def calmethod(self):
        """each row of this table defines a calculatino method
        implementation"""
        cursor.execute("""create table calmethod(
            calmethod_id serial not null,
            storeent_id integer not null,
            calusage_id integer not null,
            taskname varchar(254),
            description varchar(508),
            subclass integer,
            name varchar(254),
            primary key(calmethod_id)
        )""")
        cursor.execute("create unique index i0000055 on calmethod(subclass,calusage_id,storeent_id,name)")
        cursor.execute("create index i0000501 on calmethod(storeent_id)")
        cursor.execute("create index i0000502 on calmethod(calusage_id)")
        # CONSTRAINTS
    
    def calusage(self):
        """a row in this table represents a calculationusage, indicating which kind of
        calculation a calculationcode or calculationscale is used for. examples of calculationusages
        include discounts, shipping charges, sales tax and shipping tax."""
        cursor.execute("""create table calusage(
            calusage_id serial not null,
            description varchar(254),
            streltypnamecfg varchar(60),
            streltypnamert varchar(60),
            primary key(calusage_id)
        )""")

class CalculationCodeDirectAttachment:
    """the calculation code - direct attacment data model shows the 
    relationship between database tables that contain information
    about direct attachments in calculation codes."""
    def ordicalcd(self):
        """each row of this table indicates to the calculationcodecombine method
        that a calculationcode is directly attached to an order item.
        the attachment is not effective unless the directcalculationcodeattachment
        flag in orderitems.prepareflags is 1"""
        cursor.execute("""create table ordicalcd(
            calcode_id integer not null,
            ordicalcd_id bigserial not null,
            orderitems_id bigint not null,
            calflags integer not null default 0,
            calparmtype integer not null default 0,
            calparmamt decimal(20,5)not null default 0,
            primary key(ordicalcd_id)
        )""")
        cursor.execute("create index i0000656 on ordicalcd(orderitems_id)")
        cursor.execute("create index i0000657 on ordicalcd(calcode_id)")
        # CONSTRAINTS
    
    def caladjust(self):
        """a row in tis table represents a calculation adjustment. a calculation
        adjustment is an adjustment created by a service representative to be applied
        to the calculation usage specified. currently only shippin adjustments are supported"""
        cursor.execute("""create table caladjust(
            caladjust_id bigint not null,
            orders_id bigint not null,
            calusage_id integer not null,
            shipmode_id integer,
            servicerep_id bigint not null,
            parmtype integer not null default 0,
            parmamt decimal(20,5)not null default 0,
            field1 integer,
            field2 varchar(128),
            basecost decimal(20,5)not null default 0.00000,
            primary key(caladjust_id)
        )""")
        cursor.execute("create index i0000958 on caladjust(orders_id,calusage_id,shipmode_id)")
        cursor.execute("create index i0000959 on caladjust(shipmode_id)")
        cursor.execute("create index i0000960 on caladjust(servicerep_id)")
        cursor.execute("create index i0000961 on caladjust(calusage_id)")
        # CONSTRAINTS

    def ordcalcd(self):
        """each row of this table indicates to the calculationcodecombine method 
        that a calculationcode is directly attached to all orderitems in an
        order. the order directcalculationcodeattachment flag in orderitems.prepareflags is 1"""
        cursor.execute("""create table ordcalcd(
            ordcalcd_id bigserial not null,
            orders_id bigint not null,
            calcode_id integer not null,
            calflags integer not null default 0,
            calparmtype integer not null default 0,
            calparmamt decimal(20,5)not null default 0,
            primary key(ordcalcd_id)
        )""")
        cursor.execute("create index i0000637 on ordcalcd(calcode_id)")
        cursor.execute("create index i0000638 on ordcalcd(orders_id)")
        # CONSTRAINTS

class CalculationCodeIndirectAttachment:
    """the calculation code -indirect attachment model shows the relationship
    between database tables that contain information about indirect attachment
    to calculation codes."""
    def shipmodclcd(self):
        """the relationship between the calculationcode and the shipping mode
        for shipping promition use"""
        cursor.execute("""create table shipmodclcd(
            shipmodclcd_id serial not null,
            store_id integer not null,
            shipmode_id integer,
            calcode_id integer not null,
            trading_id bigint,
            primary key(shipmodclcd_id)
        )""")
        cursor.execute("create unique index i0000303 on shipmodclcd(store_id,calcode_id,shipmode_id,trading_id)")
        cursor.execute("create index i0000268 on shipmodclcd(trading_id)")
        cursor.execute("create index i0000269 on shipmodclcd(calcode_id)")
        cursor.execute("create index i0000270 on shipmodclcd(shipmode_id)")
        cursor.execute("create index i0000271 on shipmodclcd(store_id)")
        # CONSTRAINTS
    
    def catencalcd(self):
        """a row in this table indicates that a calculation code is attached
        to a catalog entry. and it is also attached to the catalog entry's 
        PRODUCT_ITEM children (or all catalogentries) for the specified store.
        and also it is attached to a trading agreement (or all trading agreements)"""
        cursor.execute("""create table catencalcd(
            store_id integer not null,
            catencalcd_id bigserial not null,
            trading_id bigint,
            catentry_id bigint,
            calcode_id integer,
            calflags smallint,
            primary key(catencalcd_id)
        )""")
        cursor.execute("create unique index i0000062 on catencalcd(store_id,catentry_id,calcode_id,trading_id)")
        cursor.execute("create index i0000514 on catencalcd(calcode_id)")
        cursor.execute("create index i0000515 on catencalcd(catentry_id)")
        cursor.execute("create index i0000516 on catencalcd(trading_id)")
        # CONSTRAINTS

    def catgpcalcd(self):
        """a row in this table indicates tat a calculationcode is attached to all catalog
        entries and their product_item children in a cataloggroup for the 
        specified store and trading agreement or all trading agreements"""
        cursor.execute("""create table catgpcalcd(
            store_id integer not null,
            catgpcalcd_id bigserial not null,
            trading_id bigint,
            catgroup_id bigint not null,
            calcode_id integer,
            calflags smallint,
            primary key(catgpcalcd_id)
        )""")
        cursor.execute("create unique index i0000066 on catgpcalcd(store_id,catgroup_id,calcode_id,trading_id)")
        cursor.execute("create index i0000520 on catgpcalcd(calcode_id)")
        cursor.execute("create index i0000521 on catgpcalcd(catgroup_id)")
        cursor.execute("create index i0000522 on catgpcalcd(trading_id)")
        # CONSTRAINTS
    
class CalculationMethod:
    """each row in the calmethod database table indicates a task command that can be
    used by a store or by stores in a store group, to perform calculations of discounts
    shipping charges, sales or use tax, and shipping taxes (depending on its calculation
    usage)."""
    def stencalusg(self):
        """each row of this table contains information about how a calculation usage
        is used by a storeentity. if a column value is null for a store, 
        the store uses the value specified by its storegroup."""
        cursor.execute("""create table stencalusg(
            storeent_id integer not null,
            calusage_id integer not null,
            atcc_calmethod_id integer,
            atrc_calmethod_id integer,
            calcode_id integer,
            calmethod_id_app integer,
            calmethod_id_sum integer,
            calmethod_id_fin integer,
            useflags integer not null default 0,
            calmethod_id_ini integer,
            sequence float not null default 0,
            primary key(storeent_id,calusage_id)
        )""")
        cursor.execute("create index i0000770 on stencalusg(atcc_calmethod_id)")
        cursor.execute("create index i0000771 on stencalusg(calusage_id)")
        cursor.execute("create index i0000772 on stencalusg(calmethod_id_app)")
        cursor.execute("create index i0000773 on stencalusg(calmethod_id_ini)")
        cursor.execute("create index i0000774 on stencalusg(calmethod_id_fin)")
        cursor.execute("create index i0000775 on stencalusg(calmethod_id_sum)")
        cursor.execute("create index i0000776 on stencalusg(calcode_id)")
        cursor.execute("create index i0000777 on stencalusg(atrc_calmethod_id)")
        # CONSTRAINTS
    
    def calscale(self):
        """a row in this table represents a calculation scale. it can be used
        to perform a scale lookup to calculate a monetary amount for a given set
        of orderitems. calculation scale defines what the charge is based on when calculating
        different kinds of charges. for example, the shipping charge can be charged by weight
        price, quantity, etc. CalculationScale can also be associated with the CalculationRule.
        through the CRULESCALE table."""
        cursor.execute("""create table calscale(
            calscale_id serial not null,
            qtyunit_id char(16),
            code char(30),
            description varchar(254),
            storeent_id integer not null,
            calusage_id integer not null,
            setccurr char(3),
            calmethod_id integer not null,
            field1 varchar(254),
            primary key(calscale_id)
        )""")
        cursor.execute("create unique index i0000059 on calscale(calusage_id,code,storeent_id)")
        cursor.execute("create index i0000508 on calscale(calmethod_id)")
        cursor.execute("create index i0000509 on calscale(storeent_id)")
        # CONSTRAINTS
    
    def crulescale(self):
        """each row of this table shows that a calculationrule is associated
        with a calculationscale. both are used y the calculation framework
        for discounts, shipping charges and taxes and so on"""
        cursor.execute("""create table crulescale(
            calscale_id integer not null,
            calrule_id integer not null,
            primary key(calrule_id,calscale_id)
        )""")
        cursor.execute("create index i0000550 on crulescale(calscale_id)")
        # CONSTRAINT
    
    def calscaleds(self):
        """each row of this table contains
        lang-depenent info for a calscale"""
        cursor.execute("""create table calscaleds(
            calscale_id integer not null,
            language_id integer not null,
            description varchar(254),
            primary key(language_id,calscale_id)
        )""")
    
    def calrule(self):
        """each row in this table represents a calculationrule. it defines how to arrive
        at a monetary amount for a set or orderitems. for each calculation code,
        one or more calculationrules can be defined. the calculationrules which belong to
        one calculationcode are responsible for doing the calculation."""
        cursor.execute("""create table calrule(
            calrule_id serial not null,
            calcode_id integer not null,
            startdate timestamp,
            taxcgry_id integer,
            enddate timestamp,
            sequence float not null default 0,
            combination integer not null default 2,
            calmethod_id integer not null,
            calmethod_id_qfy integer not null,
            field1 decimal(20,5),
            field2 varchar(254),
            flags integer not null default 0,
            identifier integer not null default 1,
            primary key(calrule_id)
        )""")
        cursor.execute("create unique index i0000058 on calrule(calcode_id,field2)")
        cursor.execute("create index i0000504 on calrule(taxcgry_id)")
        cursor.execute("create index i0000505 on calrule(calmethod_id)")
        cursor.execute("create index i0000506 on calrule(calmethod_id_qfy)")
        # CONSTRAINTS
    
    def calrange(self):
        """each row represents a calculationrange. which conceptually represents
        a row in a calculationscale."""
        cursor.execute("""create table calrange(
            calrange_id serial not null,
            calscale_id integer,
            calmethod_id integer not null,
            rangestart decimal(20,5),
            cumulative integer not null default 0,
            field1 decimal(20,5),
            field2 decimal(20,5),
            field3 varchar(254),
            markfordelete integer not null default 0,
            primary key(calrange_id)
        )""")
        cursor.execute("create unique index i0000056 on calrange(calscale_id,rangestart)")
        cursor.execute("create index i0000503 on calrange(calmethod_id)")
        # CONSTRAINTS
    
    def calrlookup(self):
        """each row in this table representa a calculationrangelookup result
        which is part of a calculation range."""
        cursor.execute("""create table calrlookup(
            calrlookup_id serial not null,
            setccurr char(3),
            calrange_id integer not null,
            value decimal(20,5)not null default 0,
            primary key(calrlookup_id)
        )""")
        cursor.execute("create unique index i0000057 on calrlookup(calrange_id,setccurr)")
        # CONSTRAINTS

class CalculationRuleDiscount:
    """the calculation rule - discount data model shows the 
    relationship between database tables that contain information
    about discount data in calculation rules."""
    def calrulemgp(self):
        """a row in this table associates a calculationrule wth a member group.
        the discount calculationrulequalifymethod can use this relationship
        to restrict use of the calculationrule to members of certain member groups.
        see the storembrgrp table for more info."""
        cursor.execute("""create table calrulemgp(
            calrule_id integer not null,
            mbrgrp_id bigint not null,
            primary key(mbrgrp_id,calrule_id)
        )""")
        cursor.execute("create index i0000507 on calrulemgp(calrule_id)")
        # CONSTRAINTS
    
    def taxcgry(self):
        "each row in tis table representa a tax category"
        cursor.execute("""create table taxcgry(
            taxcgry_id serial not null,
            taxtype_id integer not null,
            storeent_id integer not null,
            name varchar(254),
            calculationseq float not null default 0,
            displayseq float not null default 0,
            displayusage integer not null default 0,
            field1 decimal(20,5),
            field2 decimal(20,5),
            field3 varchar(254),
            markfordelete integer not null default 0,
            primary key(taxcgry_id)
        )""")
        cursor.execute("create unique index i0000244 on taxcgry(name,storeent_id)")
        cursor.execute("create index i0000803 on taxcgry(storeent_id)")
        # CONSTRAINTS

    def taxjcrule(self):
        """when shipping from a fulfullmentcenter to a shipping address
        that matches one of the taxjurisdictions in a particular taxjcgroup
        this table can be used by a tax calculationrulequalify method to choose
        a calculation rule."""
        cursor.execute("""create table taxjcrule(
            calrule_id integer not null,
            taxjcrule_id serial not null,
            ffmcenter_id integer,
            jurstgroup_id integer,
            precedence float not null default 0,
            primary key(taxjcrule_id)
        )""")
        cursor.execute("create unique index i0000345 on taxjcrule(calrule_id,ffmcenter_id,jurstgroup_id)")
        cursor.execute("create index i0000805 on taxjcrule(jurstgroup_id)")
        cursor.execute("create index i0000806 on taxjcrule(ffmcenter_id)")
        # CONSTRAINT
    
    def calcodtxex(self):
        """each row of this table indicates that a monetary amounts calculated
        using a particular calcode are exempt from taxation of a particular tax cat"""
        cursor.execute("""create table calcodtxex(
            calcode_id integer not null,
            taxcgry_id integer not null,
            primary key(calcode_id,taxcgry_id)
        )""")
        cursor.execute("create index i0000500 on calcodtxex(taxcgry_id)")
        # CONSTRAINTS

class CalculationRuleShipping:
    """the calculation rule - shipping data model shows the relationship between database tables
    that contain information about shipping data in calculation rules."""
    def shpjcrule(self):
        """this table can be used by the shipping calculationrulequalify method
        to choose a calculation rule based on the shipping mode and fulfillmentcenter
        it is used when the shipping address matches one of the shipping jurisdictions
        in a particular shippingjurisdictiongroup."""
        cursor.execute("""create table shpjcrule(
            calrule_id integer not null,
            shpjcrule_id serial not null,
            ffmcenter_id integer,
            jurstgroup_id integer,
            precedence float not null default 0,
            shipmode_id integer,
            primary key(shpjcrule_id)
        )""")
        cursor.execute("create unique index i0000230 on shpjcrule(ffmcenter_id,shipmode_id,jurstgroup_id,calrule_id)")
        cursor.execute("create index i0000767 on shpjcrule(shipmode_id)")
        cursor.execute("create index i0000768 on shpjcrule(jurstgroup_id)")
        cursor.execute("create index i0000769 on shpjcrule(calrule_id)")
        # CONSTRAINTS
    
    def jurstgroup(self):
        """each row of this table represents an instance of a particular subclass
        of jurisdictiongroup. a jurisdictiongroup of a particular subclass is a 
        grouping of jurisdiction definitions of that subclass."""
        cursor.execute("""create table jurstgroup(
            jurstgroup_id serial not null,
            description varchar(254),
            subclass integer not null,
            storeent_id integer not null,
            code char(30)not null,
            markfordelete integer not null default 0,
            primary key(jurstgroup_id)
        )""")
        cursor.execute("create unique index i0000143 on jurstgroup(code,storeent_id,subclass)")
        cursor.execute("create index i0000602 on jurstgroup(storeent_id)")
        # CONSTRAINTS
    
    def jurstgrprel(self):
        """each row of this table indicates that a jurisdiction of a 
        particular subclass is in a jurisdiction group of that same suclass"""
        cursor.execute("""create table jurstgrprel(
            jurst_id integer not null,
            jurstgroup_id integer not null,
            subclass integer not null,
            primary key(jurst_id,jurstgroup_id)
        )""")
        cursor.execute("create index i0000601 on jurstgrprel(jurstgroup_id)")
        # CONSTRAINT
    
    def jurst(self):
        """each row of this table defines an instance of a particular subclass
        of jurisdiction. a jurisdiction contains information that can be 
        matched with an address."""
        cursor.execute("""create table jurst(
            jurst_id serial not null,
            country varchar(128),
            storeent_id integer not null,
            code char(30)not null,
            description varchar(254),
            subclass integer not null,
            city varchar(254),
            state varchar(254),
            stateabbr varchar(10),
            countryabbr varchar(10),
            district varchar(254),
            county varchar(254),
            zipcodestart varchar(40),
            zipcodeend varchar(40),
            geocode varchar(254),
            markfordelete integer not null default 0,
            primary key(jurst_id)
        )""")
        cursor.execute("create unique index i0000142 on jurst(code,storeent_id,subclass)")
        cursor.execute("create index i0000600 on jurst(storeent_id)")
        # CONSTRAINT

class CalculationUsage:
    """the calculation usage data model shows the relationship between database tables
    that contain information about calculation usage.
    calculation usage includes discounts shipping charges, and sales, and shipping taxes
    calculation usage can be specified for individual stores, and affects the way that calcul
    ation codes and methods are used""" 
    def ordadjust(self):
        "each row of this table represents an order adjustment"
        cursor.execute("""create table ordadjust(
            ordadjust_id bigserial not null,
            orders_id bigint not null,
            calcode_id integer,
            calusage_id integer,
            amount decimal(20,5)default 0,
            displaylevel integer not null default 0,
            primary key(ordadjust_id)
        )""")
        cursor.execute("create index i0000171 on ordadjust(orders_id)")
        cursor.execute("create index i0000634 on ordadjust(calusage_id)")
        cursor.execute("create index i0000635 on ordadjust(calcode_id)")
        # CONSTRAINTS
    
    def taxtype(self):
        """this table represents a taxtype. for example,
        sales tax and shipping tax are two types of taxes."""
        cursor.execute("""create table taxtype(
            taxtype_id integer not null,
            name varchar(254)not null,
            txcdscheme_id integer,
            sequence float not null default 0,
            primary key(taxtype_id)
        )""")
        cursor.execute("create unique index i00003440 on taxtype(taxtype_id,name)")
        cursor.execute("create index i0000344 on taxtype(sequence,txcdscheme_id,taxtype_id)")
        # CONSTRAINT

    def fill_calusage(self):
        calusages=[{"calusage_id":-1,"description":"Discount"},{"calusage_id":-2,"description":"Shipping"},
        {"calusage_id":-3,"description":"Sales Tax"},{"calusage_id":-4,"description":"Shipping Tax"},
        {"calusage_id":-5,"description":"Coupon"},{"calusage_id":-6,"description":"Surcharge"},
        {"calusage_id":-7,"description":"Shipping Adjustment"}]
        for calusage in calusages:
            cursor.execute("""insert into calusage(calusage_id,description)values(%s,%s)returning
            calusage_id""",(calusage["calusage_id"],calusage["description"],))

if __name__=="__main__":
    c1=CalculationCode()
    c1.calcode()
    c1.calcodedesc()
    c1.calcodemgp()
    c1.calmethod()
    c1.calusage()

    c2=CalculationCodeDirectAttachment()
    c2.ordicalcd()
    c2.caladjust()
    c2.ordcalcd()

    c3=CalculationCodeIndirectAttachment()
    c3.shipmodclcd()
    c3.catencalcd()
    c3.catgpcalcd()

    c4=CalculationMethod()
    c4.stencalusg()
    c4.crulescale()
    c4.calscale()
    c4.calscaleds()
    c4.calrule()
    c4.calrlookup()
    c4.calrange()
    
    c5=CalculationRuleDiscount()
    c5.taxjcrule()
    c5.taxcgry()
    c5.calrulemgp()
    c5.calcodtxex()

    c6=CalculationRuleShipping()
    c6.shpjcrule()
    c6.jurstgrprel()
    c6.jurst()

    c7=CalculationUsage()
