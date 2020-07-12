from db_con import createcon
con,cursor=createcon("retail","pronov","localhost","5432")
con.autocommit=True
from functions import build_constraint

class Contract:
    """the contract data model shows the relationship between
    database tables containing information about contracts for trading positions"""
    def trading(self):
        "each row in this table represents a trading agreement"
        cursor.execute("""create table trading(
            trading_id bigserial not null,
            trdtype_id integer not null,
            account_id bigint,
            state integer not null default 0,
            markfordelete integer not null default 0,
            referencecount integer not null default 0,
            starttime timestamp,
            endtime timestamp,
            creditallowed integer not null default 0,
            reftrading_id bigint,
            primary key(trading_id)
        )""")
        cursor.execute("create index i0000815 on trading(trading_id)")
        # CONSTRAINTS

    def trddesc(self):
        "the trading agreement description table."
        cursor.execute("""create table trddesc(
            trading_id bigint not null,
            language_id integer not null,
            description varchar(254),
            longdescription varchar(4000),
            timecreated timestamp,
            timeupdated timestamp,
            primary key(trading_id,language_id)
        )""")
        # CONSTRAINTS

    def trdtype(self):
        "contains information about the type of trading for a trading agreement"
        cursor.execute("""create table trdtype(
            trdtype_id serial not null,
            primary key(trdtype_id)
        )""")
    
    def trdtypedsc(self):
        "stores a description for trading agreement types in multiple languages"
        cursor.execute("""create table trdtypedsc(
            trdtype_id integer not null,
            language_id integer not null,
            description varchar(4000),
            primary key(trdtype_id,language_id)
        )""")
        # CONSTRAINTS
    
    def account(self):
        """each row of this table represents a business account between a buyer
        organization and a seller organization. a business account can be used
        to organize various trading agreements, and to specify trading terms and conditions"""
        cursor.execute("""create table account(
            account_id bigint not null,
            name varchar(200)not null,
            member_id bigint not null,
            store_id integer,
            state integer not null default 0,
            currency char(3),
            defaultcontract integer not null default 0,
            markfordelete integer not null default 0,
            comments varchar(4000),
            timecreated timestamp,
            timeupdated timestamp,
            timeapproved timestamp,
            timeactivated timestamp,
            prcplcypref varchar(32),
            userprcplcypref smallint,
            primary key(account_id,name,member_id)
        )""")
        cursor.execute("create unique index i0000005 on account(account_id,name,member_id)")
        cursor.execute("create index i0000434 on account(member_id)")
        cursor.execute("create index i0000435 on account(store_id)")
        # CONSTRAINTS

    def contract(self):
        """each row of this table represents a contract. a contract is a part of a store
        and represents terms and conditions taht may be associated with order uitems
        such as prices, minimum quantities and who can use the contract."""
        cursor.execute("""create table contract(
            contract_id bigint not null,
            majorversion integer not null default 1,
            minorversion integer not null default 0,
            name varchar(200)not null,
            member_id bigint not null,
            origin integer not null default 0,
            state integer not null default 0,
            usage integer not null default 0,
            markfordelete integer not null default 0,
            comments varchar(4000),
            timecreated timestamp,
            timeupdated timestamp,
            timeapproved timestamp,
            timeactivated timestamp,
            timedeployed timestamp,
            family_id bigint,
            primary key(contract_id)
        )""")
        cursor.execute("create unique index i0000078 on contract(name,member_id,majorversion,minorversion,origin)")
        cursor.execute("create index i0000539 on contract(member_id)")
        cursor.execute("create index i0001510 on contract(family_id)")
        # CONSTRAINTS:
    
    def cntrname(self):
        """this table contains name information for a contract.
        the contract name is used to force serialization on contract management"""
        cursor.execute("""create table cntrname(
            name varchar(200)not null,
            member_id bigint not null,
            origin integer not null
        )""")
        cursor.execute("create unique index i0000076 on cntrname(name,member_id,origin)")
        cursor.execute("""create index i0000537 on cntrname(member_id)""")
        # CONSTRAINTS:
    
    def attachment(self):
        """this table contains information about attachments
        an attachment is a supporting document for a trading document
        for example it can be a specification of a product or a price list spreadsheet"""
        cursor.execute("""create table attachment(
            attachment_id bigserial not null,
            attachmenturl varchar(254)not null,
            member_id bigint not null,
            attachusg_id char(64),
            mimetype varchar(254),
            mimetypeencoding varchar(128),
            timecreated timestamp,
            timeupdated timestamp,
            markfordelete integer not null default 0,
            description varchar(254),
            filename varchar(254),
            filesize bigint,
            createmethod integer default 0,
            image1 varchar(254),
            image2 varchar(254),
            content text,
            reserved varchar(254),
            primary key(attachment_id)
        )""")
        cursor.execute("create unique index i0000017 on attachment(attachmenturl)")
        cursor.execute("create index i0000290 on attachment(attachusg_id)")
        cursor.execute("create index i0000452 on attachment(member_id)")
        # CONSTRAINTS:
    
    def attachusg(self):
        "the attachment usage table."
        cursor.execute("""create table attachusg(
            attachusg_id char(64)not null,
            primary key(attachusg_id)
        )""")

    def trdattach(self):
        "this table stores info about the trading attachment relationship for a trading agreement"
        cursor.execute("""create table trdattach(
            trading_id bigint not null,
            attachment_id bigint not null,
            primary key(trading_id,attachment_id)
        )""")
        cursor.execute("create index i0001292 on trdattach(attachment_id)")
        # CONSTRAINTS
    
    def participnt(self):
        "stores info about a participnt for a trading agreement"
        cursor.execute("""create table participnt(
            participnt_id bigserial not null,
            member_id bigint,
            partrole_id integer not null,
            trading_id bigint,
            termcond_id bigint,
            information varchar(4000),
            timecreated timestamp,
            timeupdated timestamp,
            primary key(participnt_id)
        )""")
        cursor.execute("create unique index i0000184 on participnt(member_id,partrole_id,trading_id,termcond_id)")
        cursor.execute("create index i0000678 on participnt(partrole_id)")
        cursor.execute("create index i000679 on participnt(trading_id)")
        cursor.execute("create index i000680 on participnt(termcond_id)")
        # CONSTRAINTS
    
    def buysupmap(self):
        """this table is used to register the buyer organization using procurement systems.
        with supplier organizations."""
        cursor.execute("""create table buysupmap(
            suporg_id bigint not null,
            buyorgunit_id bigint not null,
            catalog_id bigint not null,
            procprotcl_id integer,
            contract_id bigint,
            mbrgrp_id bigint,
            field1 varchar(64),
            field2 varchar(64),
            field3 varchar(64),
            primary key(suporg_id,buyorgunit_id)
        )""")
        cursor.execute("create index i0000490 on buysupmap(buyorgunit_id)")
        cursor.execute("create index i0000491 on buysupmap(catalog_id)")
        cursor.execute("create index i0000492 on buysupmap(contract_id)")
        cursor.execute("create index i0000493 on buysupmap(mbrgrp_id)")
        # constraints
    
    def procprotcl(self):
        """each row of the table represents a procurement system.
        protocol and its version number. for example cXML,OCI,OBI and so on."""
        cursor.execute("""create table procprotcl(
            procprotcl_id serial not null,
            procsysname char(16),
            protocolname varchar(32),
            version varchar(32),
            authtype integer not null,
            twostepmode char(1)not null,
            procprotclcomment varchar(254),
            classifdomain char(32),
            uomstandard varchar(32),
            field1 varchar(64),
            field2 varchar(64),
            field3 varchar(64),
            primary key(procprotcl_id)
        )""")
        cursor.execute("create unique index i0000190 on procprotcl(protocolname,version)")
        # CONSTRAINTS:
    
    def procsys(self):
        "each row of this table represents a procurement system"
        cursor.execute("""create table procsys(
            procsysname char(16)not null,
            field1 varchar(64),
            field2 varchar(64),
            primary key(procsysname)
        )""")
    
    def termcond(self):
        """this table contains terms and conditions used in trading agreements
        (business accounts,contracts and RFQs) to see how columns are used by the 
        different terms and conditions, refer to TERMCOND column mapping"""
        cursor.execute("""create table termcond(
            termcond_id bigserial not null,
            tcsubtype_id char(64)not null,
            trading_id bigint not null,
            mandatory integer not null default 0,
            changeable integer not null default 0,
            timecreated timestamp,
            timeupdated timestamp,
            stringfield1 varchar(2000),
            stringfield2 varchar(2000),
            stringfield3 varchar(2000),
            integerfield1 integer,
            integerfield2 integer,
            integerfield3 integer,
            bigintfield1 bigint,
            bigintfield2 bigint,
            bigintfield3 bigint,
            floatfield1 float,
            floatfield2 float,
            floatfield3 float,
            timefield1 timestamp,
            timefield2 timestamp,
            timefield3 timestamp,
            decimalfield1 decimal(20,5),
            decimalfield2 decimal(20,5),
            decimalfield3 decimal(20,5),
            sequence integer not null default 0,
            primary key(termcond_id)
        )""")
        cursor.execute("create unique index i0000246 on termcond(trading_id,tcsubtype_id)")
        cursor.execute("create index i0000810 on termcond(tcsubtype_id)")
        # CONSTRAINTS:
    
    def tcattr(self):
        """this table stores information about the terms and conditions attributes
        specified within a contract. this tale stores the xml data required by a term and condition"""
        cursor.execute("""create table tcattr(
            termcond_id bigint not null,
            type integer not null,
            trading_id bigint not null,
            sequence integer not null default 0,
            xmldefinition text not null,
            primary key(termcond_id,type,sequence)
        )""")
        cursor.execute("create index i0000807 on tcattr(trading_id)")
        # CONSTRAINTS:
    
    def tctype(self):
        "contains the types of terms and conditions"
        cursor.execute("""create table tctype(
            tctype_id char(64)not null,
            primary key(tctype_id)
        )""")

    def tcsubtype(self):
        "each row contains info about the implementation of a terms and condition subtype"
        cursor.execute("""create table tcsubtype(
            tcsubtype_id char(64)not null,
            tctype_id char(64)not null,
            accessbeanname varchar(254),
            deploycommand varchar(254),
            primary key(tcsubtype_id)
        )""")
        cursor.execute("create index i0000808 on tcsubtype(tctype_id)")
        # CONSTRAINTS:
    
    def tcsubtypds(self):
        "each row contains info for sub-type of terms and conditions"
        cursor.execute("""create table tcsubtypds(
            tcsubtype_id char(64)not null,
            language_id integer not null,
            description varchar(4000),
            primary key(tcsubtype_id,language_id)
        )""")
        # CONSTRAINTS
    
    def partrole(self):
        "stores role information about a participant for a trading agreement"
        cursor.execute("""create table partrole(
            partrole_id integer not null,
            primary key(partrole_id)
        )""")

    def partroleds(self):
        "stores description for the role a participant plays in a trading agreement"
        cursor.execute("""create table partroleds(
            partrole_id integer not null,
            language_id integer not null,
            description varchar(4000),
            primary key(partrole_id,language_id)
        )""")
        # CONSTRAINT
    
    def tcdesc(self):
        "stores descriptions for terms and conditions for a contract"
        cursor.execute("""create table tcdesc(
            termcond_id bigint not null,
            language_id integer not null,
            description varchar(254),
            longdescription varchar(4000),
            timecreated timestamp,
            timeupdated timestamp,
            primary key(termcond_id,language_id)
        )""")
        # CONSTRAINT
    
    def policytc(self):
        """stores information about which business policy is referenced 
        by a specific term or condition"""
        cursor.execute("""create table policytc(
            termcond_id bigint not null,
            policy_id bigint not null,
            primary key(policy_id,termcond_id)
        )""")
        cursor.execute("create index i0000357 on policytc(termcond_id,policy_id)")
        cursor.execute("create index i0001273 on policytc(policy_id)")
        # CONSTRAINTS
    
    def policy(self):
        """each row of this table indicates that the trading positions in a trading position container
        are available to customers of store. there the contract is deployed, subject
        to termsn and conditions associated with the contract."""
        cursor.execute("""create table policy(
            policy_id bigserial not null,
            policyname varchar(254)not null,
            policytype_id char(64)not null,
            storeent_id integer not null,
            properties varchar(2000),
            starttime timestamp,
            endtime timestamp,
            primary key(policy_id)
        )""")
        cursor.execute("create unique index i0000189 on policy(policyname,policytype_id,storeent_id)")
        cursor.execute("create index i0000337 on policy(policytype_id,storeent_id)")
        cursor.execute("create index i0000697 on policy(storeent_id)")
        # CONSTRAINT 
    
    def policydesc(self):
        "stores descriptions for business policies"
        cursor.execute("""create table policydesc(
            policy_id bigint not null,
            language_id integer not null,
            description varchar(508)not null,
            longdescription varchar(4000),
            timecreated timestamp,
            timeupdated timestamp,
            primary key(policy_id,language_id)
        )""")
        # CONSTRAINTS
    
    def policycmd(self):
        "stoers command relationship information for a business policy"
        cursor.execute("""create table policycmd(
            policy_id bigint not null,
            businesscmdclass varchar(200)not null,
            properties varchar(254),
            primary key(policy_id,businesscmdclass)
        )""")
        # CONSTRAINT
    
    def policytype(self):
        "stores information about the type of business policy for a policy"
        cursor.execute("""create table policytype(
            policytype_id char(64)not null,
            primary key(policytype_id)
        )""")
    
    def plcytycmif(self):
        "stores command interface relationship information for a business policy"
        cursor.execute("""create table plcytycmif(
            policytype_id char(64)not null,
            businesscmdif varchar(254)not null,
            primary key(businesscmdif)
        )""")
        # CONSTRAINTS
    
    def plcytypdsc(self):
        "describes the type of business policy for a policy"
        cursor.execute("""create table plcytypdsc(
            policytype_id char(64)not null,
            language_id integer not null,
            description varchar(254),
            primary key(policytype_id,language_id)
        )""")
        # CONSTRAINT

    def cntrstore(self):
        """stores store information for a contract.
        the data is used to persist XML data needed
        by a contract to create a store. """
        cursor.execute("""create table cntrstore(
            contract_id bigint not null,
            storexml text,
            primary key(contract_id)
        )""")
        # CONSTRAINTS:
    
    def fileupload(self):
        """contains information of uploaded files for the catalog
        import feature in the system."""
        cursor.execute("""create table fileupload(
            fileupload_id bigserial not null,
            member_id bigint,
            store_id integer,
            sccjobrefnum bigint,
            filepath varchar(254)not null,
            filename varchar(254),
            filesize bigint,
            filetype char(50),
            fileencoding varchar(128),
            uploadtime timestamp,
            hostname char(50),
            version integer not null,
            status integer not null default 0,
            primary key(fileupload_id)
        )""")
        cursor.execute("create unique index i0000295 on fileupload(filepath,version)")
        cursor.execute("create index i0000296 on fileupload(store_id)")
        cursor.execute("create index i0000571 on fileupload(sccjobrefnum)")
        cursor.execute("create index i0000572 on fileupload(member_id)")
        # CONSTRAINTS:
    
    def storecntr(self):
        "each row of this table indicates that a contract is deployed in a store"
        cursor.execute("""create table storecntr(
            contract_id bigint not null,
            store_id integer not null,
            primary key(contract_id,store_id)
        )""")
        cursor.execute("create index i0000784 on storecntr(store_id)")
        # CONSTRAINTS:
    
    def tdpscncntr(self):
        """each row of this table indicates that the trading positions
        in a trading position container are available to customers of stores
        where the contract is deployed, subject to any terms and conditions
        associated with the contract."""
        cursor.execute("""create table tdpscncntr(
            tradeposcn_id bigint not null,
            contract_id bigint not null,
            primary key(contract_id,tradeposcn_id)
        )""")
        cursor.execute("create index i0000809 on tdpscncntr(tradeposcn_id)")
        # CONSTRAINTS:
    
    def schconfig(self):
        "table contains all scheduled job entries"
        cursor.execute("""create table schconfig(
            sccjobrefnum bigserial not null,
            scchost varchar(128),
            member_id bigint not null,
            storeent_id integer not null default 0,
            sccrecdelay integer not null default 0,
            sccrecatt integer not null default 0,
            sccpathinfo varchar(254)not null,
            sccquery varchar(3000),
            sccstart timestamp not null,
            sccinterval integer,
            sccpriority integer not null,
            sccsequence integer not null default 0,
            sccactive char(1)not null default 'A',
            sccapptype char(20),
            interfacename varchar(254),
            sccdescription varchar(3000),
            primary key(sccjobrefnum)
        )""")
        cursor.execute("create index i0000321 on schconfig(sccpathinfo)")
        cursor.execute("create index i0000322 on schconfig(scchost)")
        cursor.execute("create index i0000323 on schconfig(sccapptype)")
        cursor.execute("create index i0000324x on schconfig(member_id)")
        cursor.execute("create index i0000325 on schconfig(storeent_id)")
        # CONSTRAINTS
    
    def catcntr(self):
        "each row of this table associates a catalog with a contract"
        cursor.execute("""create table catcntr(
            catalog_id bigint not null,
            contract_id bigint not null,
            primary key(contract_id,catalog_id)
        )""")
        cursor.execute("create index i0000513 on catcntr(catalog_id)")
        # CONSTRAINTS:
    
    def tradeposcn(self):
        """this table represents a tradingpositioncontainer. it can contain
        tradingpositions and can be made available to all customers, or only
        to customers in certain groups thru trading agreements or contracts."""
        cursor.execute("""create table tradeposcn(
            tradeposcn_id bigserial not null,
            member_id bigint not null,
            productset_id integer,
            description varchar(254),
            name varchar(254)not null,
            precedence float not null default 0,
            markfordelete integer not null default 0,
            type char(1)default 'S',
            flags integer not null default 0,
            primary key(tradeposcn_id)
        )""")
        cursor.execute("create unique index i0000255 on tradeposcn(member_id,name)")
        cursor.execute("create index i0000814 on tradeposcn(productset_id)")
        cursor.execute("create index i442156 on tradeposcn(tradeposcn_id,type)")
        # CONSTRAINTS
    
    def productset(self):
        """holds the definition of a productset. the actual representation of the 
        product set is held in the prsetcerel table"""
        cursor.execute("""create table productset(
            name varchar(64),
            productset_id serial not null,
            member_id bigint not null,
            xmldefinition text,
            publishtime timestamp,
            markfordelete integer not null default 0,
            static char(1),
            primary key(productset_id)
        )""")
        cursor.execute("create unique index i0000191 on productset(name,member_id)")
        cursor.execute("create index i0000700 on productset(member_id)")
        # CONSTRAINTS:
    
    def psetadjmnt(self):
        """this table stores information on product set adjustments and shows
        which productset is referenced by a term and condition for a business policy"""
        cursor.execute("""create table psetadjmnt(
            termcond_id bigint not null,
            productset_id integer not null,
            type integer,
            adjustment decimal(20,5)not null default 0,
            precedence integer not null default 0,
            primary key(termcond_id,productset_id)
        )""")
        cursor.execute("create index i0000703 on productset(productset_id)")
        # CONSTRAINTS

    def tradetypes(self):
        tradetypes=[{"text":"Account","value":0},{"text":"Contract","value":1},{"text":"RFQReq","value":2},
        {"text":"RFQResp","value":3},{"text":"RFQResult","value":4},{"text":"Exchange","value":5},
        {"text":"Auction","value":6},{"text":"ReverseAuction","value":7}]
        for tradetype in tradetypes:
            cursor.execute("insert into trdtype(trdtype_id)values(%s)",(tradetype["value"],))
    
    def policytypes(self):
        policytypes=['Price','ProductSet','ShippingMode','ShippingCharge','Payment','ReturnCharge','ReturnApproval',
        'ReturnPayment','InvoiceFormat']
        for policytype in policytypes:
            cursor.execute("insert into policytype(policytype_id)values(%s)",(policytype,))
    
    def tctypes(self):
        tctypes=['Addressbook','FulfillmentCenter','OrderApproval','Payment','CustomizedPriceList',
        'CatalogWithAdjustment','PriceListWithAdjustment','PriceListWithSelectiveAdjustment',
        'CatalogWithFiltering','CustomizedProductSetExclusion','CustomizedProductSetInclusion',
        'ProductSetExclusion','ProductSetInclusion','ReturnPayment','ReturnCharge','RightToBuyAmount',
        'ShippingMode','ShipToAddress','ShippingCharge','ShippingChargeAdjustment']
        for tctype in tctypes:
            cursor.execute("insert into tctype(tctype_id)values(%s)",(tctype,))
            cursor.execute("insert into tcsubtype(tctype_id,tcsubtype_id)values(%s,%s)",(tctype,tctype,))
    
    def fill_attachusg(self):
        usages=["Catalog","Contract","RFQ","Vendor","CountryAndState",]
        for usage in usages:
            cursor.execute("insert into attachusg(attachusg_id)values(%s)on conflict(attachusg_id)do update set attachusg_id=%s returning attachusg_id",(usage,usage,))
        con.commit();return cursor.fetchone()[0]
    
    def fill_partroles(self):
        cursor.execute("select language_id from languageds where description='Default'")
        langid=cursor.fetchone()[0]
        roles=["Creator",'Seller','Buyer','Supplier','Approver','Account Holder','Buyer contact',
        'Seller contact','Attorney','Administrator','Distributor','Service provider','Reseller',
        'Host','Recipent','Service representative']
        roleids=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        for i in range(len(roles)):
            cursor.execute("""insert into partrole(partrole_id)values(%s)on conflict(partrole_id)do update
            set partrole_id=%s returning partrole_id""",(roleids[i],roleids[i],))
            con.commit()
            cursor.execute("""insert into partroleds(partrole_id,language_id,description)values(%s,%s,%s)on conflict
            (partrole_id,language_id)do update set partrole_id=%s,language_id=%s,description=%s returning partrole_id
            """,(roleids[i],langid,roles[i],roleids[i],langid,roles[i],));con.commit()

if __name__=="__main__":
    c=Contract()
    c.trading()
    c.trddesc()
    c.trdtype()
    c.trdtypedsc()
    c.account()
    c.contract()
    c.cntrname()
    c.attachment()
    c.attachusg()
    c.trdattach()
    c.participnt()
    c.buysupmap()
    c.procprotcl()
    c.procsys()
    c.termcond()
    c.tcattr()
    c.tctype()
    c.tcsubtype()
    c.tcsubtypds()
    c.partrole()
    c.partroleds()
    c.tcdesc()
    c.policytc()
    c.policy()
    c.policydesc()
    c.policycmd()
    c.policytype()
    c.plcytycmif()
    c.plcytypdsc()
    c.cntrstore()
    c.fileupload()
    c.storecntr()
    c.tdpscncntr()
    c.schconfig()
    c.catcntr()
    c.tradeposcn()
    c.productset()
    c.psetadjmnt()
