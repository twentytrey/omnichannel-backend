from db_con import con,cursor
from functions import build_constraint

class Order:
    """the order data model shows the relationshp between database tables that contain
    iformation about orders. members can own store entities. other members can create orders 
    and addresses. an order may have a billing address."""
    def orders(self):
        "each row in this table represents an order in a store."
        cursor.execute("""create table orders(
            orders_id bigserial not null,
            ormorder char(60),
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
            opsystem_id integer,
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
    
    def ordshiphst(self):
        """each row contains information about inventory
        that has been released for fulfillment of an orderitem"""
        cursor.execute("""create table ordshiphst(
            ordshiphstnum serial not null,
            orderitems_id bigint not null,
            versionspc_id bigint not null,
            receipt_id bigint,
            qtyshipped integer,
            dateshipped timestamp,
            lastupdate timestamp,
            qtyreturned integer not null default 0,
            primary key(orderitems_id,ordshiphstnum)
        )""")
        cursor.execute("create index i0000674 on ordshiphst(receipt_id)")
        cursor.execute("create index i0000675 on ordshiphst(versionspc_id)")
        # CONSTRAINT
    
    def ordpaymthd(self):
        cursor.execute("""create table ordpaymthd(
            paymethod char(5)not null,
            orders_id bigint not null,
            paydevice smallint,
            startdate timestamp,
            refundnumber bigint not null default 0,
            trading_id bigint,
            account_id bigint,
            rma_id bigint,
            policy_id bigint,
            paysummary_id bigint,
            enddate timestamp,
            buyerpo_id bigint,
            maxamount decimal(20,5),
            creditline_id bigint,
            actualamount decimal(20,5),
            chargeamount decimal(20,5),
            chargetime timestamp,
            chargeamtcurr char(3),
            paymentdata text,
            stringfield1 varchar(512),
            stringfield2 varchar(512),
            stringfield3 varchar(254),
            stringfield4 varchar(254),
            status integer default 0,
            bigintfield1 bigint,
            bigintfield2 bigint,
            bigintfield3 bigint,
            decimalfield1 decimal(20,5),
            decimalfield2 decimal(20,5),
            decimalfield3 decimal(20,5),
            primary key(orders_id,paymethod,refundnumber)
        )""")
        cursor.execute("create index i0000665 on ordpaymthd(creditline_id)")
        cursor.execute("create index i0000666 on ordpaymthd(buyerpo_id)")
        cursor.execute("create index i0000667 on ordpaymthd(paysummary_id)")
        cursor.execute("create index i0000668 on ordpaymthd(policy_id)")
        cursor.execute("create index i0000669 on ordpaymthd(rma_id)")
        cursor.execute("create index i0000670 on ordpaymthd(account_id)")
        # CONSTRAINT
    
    def creditline(self):
        """each row of this table represents a credit line the account holder
        (buyer organization) has with the seller organization. this credit line is
        associated with a specific business account"""
        cursor.execute("""create table creditline(
            creditline_id bigserial not null,
            setccurr char(3),
            account_id integer default 0,
            timecreated timestamp,
            timeupdated timestamp,
            nextduedate timestamp,
            n integer not null,
            rate decimal(20,1) not null,
            creditlimit decimal(20,5),
            decimalfield1 decimal(20,5),
            decimalfield2 decimal(20,5),
            plan_integration bigint,
            plan_code varchar(254),
            plan_id bigint,
            primary key(creditline_id)
        )""")
        cursor.execute("create index i0000549 on creditline(account_id)")
        cursor.execute("create index a8dpb2 on creditline(plan_integration,plan_code,plan_id)")
        cursor.execute("create index a3vd0w on creditline(n,rate,decimalfield2)")
        # CONSTRAINTS

    def orcomment(self):
        """this table stores the comments for an order entered
        by a customer service representative."""
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
        cursor.execute("create index i0000532x on orcomment(orders_id)")
        cursor.execute("create index i0001264 on orcomment(ordchgrsn_id)")
        cursor.execute("create index i0001265 on orcomment(servicerep_id)")
        # CONSTRAINTS
    
    def buschn(self):
        "this table contains business channel information"
        cursor.execute("""create table buschn(
            buschn_id integer not null,
            name char(60)not null,
            state char(1)not null,
            primary key(buschn_id)
        )""")
    
    def buyerpo(self):
        """each of this table represents a purchase order number. it is that the buyer
        organization of the account has defined or used for trading with the seller
        organiztion. the number is only unique within the account."""
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
        # CONSTRAINT
    
    def ordusers(self):
        "contains information about users tat worjked with an order"
        cursor.execute("""create table ordusers(
            orders_id bigint not null,
            creator_id bigint,
            submitter_id bigint,
            primary key(orders_id)
        )""")
    
    def orderhist(self):
        "used to save order snapshots"
        cursor.execute("""create table orderhist(
            orders_id bigint not null,
            orderversion smallint not null,
            lastupdate timestamp,
            orderdata text,
            field1 integer,
            field2 varchar(254),
            field3 timestamp,
            primary key(orders_id,orderversion)
        )""")
    
    def ordpayinfo(self):
        """each row in this table holds a name-value pair representing payment 
        information for a particular order. values added to this table are encrypted
        wen the instance/pdiencrypt configuration flag is 'on' """
        cursor.execute("""create table ordpayinfo(
            orders_id bigint not null,
            ordpayinfo_id bigserial not null,
            name varchar(254)not null,
            value varchar(512)not null,
            primary key(ordpayinfo_id)
        )""")
        cursor.execute("create index i0000179 on ordpayinfo(orders_id)")
        # CONSTRAINT
    
    def ordoptions(self):
        "tis table is used for order notification"
        cursor.execute("""create table ordoptions(
            orders_id bigint not null,
            notifymerchant integer,
            notifyshopper integer,
            primary key(orders_id)
        )""")
        # CONSTRAINTS
    
    def cpendorder(self):
        """each row of this table indicates that an order is marked
        as current for a customer in a store, if its stats is 'P' pending."""
        cursor.execute("""create table cpendorder(
            storeent_id integer not null,
            orders_id bigint not null,
            member_id bigint not null,
            field1 integer,
            field2 varchar(254),
            primary key(orders_id,member_id)
        )""")
        cursor.execute("create index i0000542 on cpendorder(storeent_id)")
        cursor.execute("create index i168207 on cpendorder(member_id)")
        # CONSTRAINTS
    
    def ordtax(self):
        """each row of this table represents the total tax amounts
        of a particular taxcategory. taxcategory for all the orderitems in that order"""
        cursor.execute("""create table ordtax(
            orders_id bigint not null,
            taxcgry_id integer not null,
            taxamount decimal(20,5)not null,
            lastupdate timestamp,
            primary key(orders_id,taxcgry_id)
        )""")
        cursor.execute("create index i0000676 on ordtax(taxcgry_id)")
        # CONSTRAINTS
    
    def ordertmpl(self):
        """each row of this table indicates that an order is used
        as a template by a customer. and it also indicates whether the template
        is current for the customer"""
        cursor.execute("""create table ordertmpl(
            orders_id bigint not null,
            member_id bigint not null,
            usage integer not null default 0,
            primary key(member_id,orders_id)
        )""")
        cursor.execute("create index i0000655 on ordertmpl(orders_id)")
        # CONSTRAINTS
    
    def ordermgp(self):
        """this table is used to track the customer
        segments to which an order is associated"""
        cursor.execute("""create table ordermgp(
            orders_id bigint not null,
            mbrgrp_id bigint not null,
            primary key(orders_id,mbrgrp_id)
        )""")
        cursor.execute("create index i0000650 on ordermgp(mbrgrp_id)")
        # CONSTRAINTS
    
    def blkrsncode(self):
        "stores the various reason codes for which an order may be blocked"
        cursor.execute("""create table blkrsncode(
            blkrsncode_id serial not null,
            blockreasontype char(25)not null,
            manualblock smallint not null,
            markfordelete smallint not null default 0,
            field1 integer,
            field2 varchar(254),
            primary key(blkrsncode_id)
        )""")
    
    def blkrsndesc(self):
        "holds reason code description in different locales"
        cursor.execute("""create table blkrsndesc(
            blkrsncode_id integer not null,
            language_id integer not null,
            description varchar(254)not null,
            primary key(blkrsncode_id,language_id)
        )""")
        # CONSTRAINTS
    
    def orderblk(self):
        "stores blocked orders with reason code"
        cursor.execute("""create table orderblk(
            orderblk_id bigserial not null,
            orders_id bigint not null,
            blkrsncode_id integer not null,
            timeblocked timestamp not null,
            resolved smallint not null default 0,
            blkcomment varchar(254),
            field1 integer,
            field2 varchar(254),
            primary key(orderblk_id)
        )""")
        cursor.execute("create index i0000956 on orderblk(orders_id)")
        cursor.execute("create index i0000957 on orderblk(blkrsncode_id,resolved)")
        # CONSTRAINT

class OrderAdjustment:
    """the order adjustment data model shows the relationship between database tables
    that contain information about order adjustments. each orderadjustments is the total
    of the orderitemadjustments that ar created when the results from a particular
    calculationcode calculation are applied. orderadjustments are created by the
    applyorderadjustments  task command that is invoked by the order prepare controller
    command. a suborder adjustment is the subtotal of the orderitemadjustments with orderitems
    that jave the same shipping address. typically the orderitem adjustment is taxable and effects
    tax calculations, but if the orderadjustment is marked as tax exempt for certain tax categories
    the tax calculations for those tax categories are not affected. an orderadjustment has a muilti lingual
    description that can be displayed to customers hat is copied from the description of the calculation
    code taht created it."""
    def suborders(self):
        """eah row of this table contains subtotals of
        amounts for all the orderitems of an order with the same
        shipping address."""
        cursor.execute("""create table suborders(
            orders_id bigint not null,
            suborder_id bigserial not null,
            address_id bigint,
            country char(30),
            totalproduct decimal(20,5)default 0,
            totaltax decimal(20,5)default 0,
            totalshipping decimal(20,5)default 0,
            currency char(10),
            field1 integer,
            field2 decimal(20,5),
            field3 varchar(254),
            totaladjustment decimal(20,5)default 0,
            primary key(suborder_id)
        )""")
        cursor.execute("create index i0000242 on suborders(totalproduct)")
        cursor.execute("create index i0000243 on suborders(orders_id)")
        cursor.execute("create index i0000801 on suborders(address_id)")
        # CONSTRAINTS
    
    def subordadj(self):
        """eac row of this table represents a subtotal of all the orderitem adjustment amounts
        in an orderadjustment whose orderitems have the same shipping address"""
        cursor.execute("""create table subordadj(
            suborder_id bigint not null,
            ordadjust_id bigint not null,
            totaladjustment decimal(20,5)default 0,
            primary key(suborder_id,ordadjust_id)
        )""")
        cursor.execute("create index i0000800 on subordadj(ordadjust_id)")
        # CONSTRAINTS
    
    def ordadjust(self):
        "each row represents an orderadjustment"
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
        # CONSTRAINT
    
    def ordiadjust(self):
        "each row represents an orderitemadjustment"
        cursor.execute("""create table ordiadjust(
            ordiadjust_id bigserial not null,
            ordadjust_id bigint not null,
            orderitems_id bigint not null,
            amount decimal(20,5)not null default 0,
            primary key(ordiadjust_id)
        )""")
        cursor.execute("create unique index i0000177 on ordiadjust(ordiadjust_id,orderitems_id)")
        cursor.execute("create index i0000178 on ordiadjust(orderitems_id)")
        # CONSTAINTS
    
    def ordadjtxex(self):
        """each row of this table indicates that an orderadjustment is exempt
        from taxation of a particular taxcategory. for example, an "after tax" 
        rebate can be repreented as a negative orderadjustment that is exempt from taxation 
        of all tax categories."""
        cursor.execute("""create table ordadjtxex(
            ordadjust_id bigint not null,
            taxcgry_id integer not null,
            primary key(ordadjust_id,taxcgry_id)
        )""")
        cursor.execute("create index i0000633 on ordadjtxex(taxcgry_id)")
        # CONSTRAINT
    
    def ordadjdsc(self):
        """each row of this table contains lang-dependent information
        for an order adjustment"""
        cursor.execute("""create table ordadjdsc(
            ordadjust_id bigint not null,
            language_id integer not null,
            description varchar(254),
            primary key(ordadjust_id,language_id)
        )""")
    
    def prcorsn(self):
        """Price Override Reason - tis table stores the reason the merchant 
        needed to override a system calculated price."""
        cursor.execute("""create table prcorsn(
            prcorsn_id serial not null,
            storeent_id integer not null,
            markfordelete integer not null default 0,
            code varchar(50)not null,
            primary key(prcorsn_id)
        )""")
        cursor.execute("create unique index i0000968 on prcorsn(storeent_id,code)")
        # CONSTRAINT
    
    def prcorsndsc(self):
        """Price Override Reason Description - this table stores the 
        lang-dependent description of the price override reason codes."""
        cursor.execute("""create table prcorsndsc(
            prcorsn_id integer not null,
            language_id integer not null,
            description varchar(254),
            primary key(prcorsn_id)
        )""")

class OrderManagementAdjustmentAndTax:
    """the order management adjustment and tax data model shows the relationship between
    database tables that contain information about order management adjustment and tax data for order"""
    def rmaiadjcrd(self):
        """this table stores return merchandise authorization item
        adjustment credits. these are the portion of an order item adjustment
        that is to be refunded to the buyer."""
        cursor.execute("""create table rmaiadjcrd(
            rmaiadjcrd_id bigserial not null,
            rmaitem_id bigint not null,
            ordadjust_id bigint not null,
            amount decimal(20,5)not null default 0,
            primary key(rmaiadjcrd_id)
        )""")
        cursor.execute("create index i0000214 on rmaiadjcrd(rmaitem_id)")
        cursor.execute("create index i0000746 on rmaiadjcrd(ordadjust_id)")
        # CONSTRAINTS
    
    def rmaitem(self):
        """this table stores item information for a return
        or credit for a return merchandise authorization RMA"""
        cursor.execute("""create table rmaitem(
            rmaitem_id bigserial not null,
            rma_id bigint not null,
            catentry_id bigint not null,
            member_id bigint not null,
            orderitems_id bigint,
            itemspc_id bigint not null,
            rtnreason_id integer not null,
            refundorreplace char(3)not null,
            creditamount decimal(20,5)not null default 0,
            quantity float not null,
            creditdate timestamp,
            status char(3)default 'PND',
            currency char(3)not null,
            comments varchar(254),
            taxamount decimal(20,5),
            adjustmentcredit decimal(20,5)not null default 0,
            adjustment decimal(20,5)not null default 0,
            lastupdate timestamp,
            totalcredit decimal(20,5)not null default 0,
            invquantity integer not null default 0,
            primary key(rmaitem_id)
        )""")
        cursor.execute("create index i0000215 on rmaitem(rma_id,rmaitem_id)")
        cursor.execute("create index i0000747 on rmaitem(itemspc_id)")
        cursor.execute("create index i0000748 on rmaitem(member_id)")
        cursor.execute("create index i0000749 on rmaitem(catentry_id)")
        cursor.execute("create index i0001282 on rmaitem(rtnreason_id)")
        cursor.execute("create index i837116 on rmaitem(orderitems_id,rmaitem_id,status,rma_id)")
        # CONSTRAINTS
    
    def rma(self):
        "this table is a container for return merchandise authorizations"
        cursor.execute("""create table rma(
            rma_id bigserial not null,
            store_id integer not null,
            orgentity_id bigint,
            policy_id bigint,
            member_id bigint not null,
            trading_id bigint,
            ffmcenter_id integer,
            rmadate timestamp not null,
            totalcredit decimal(20,5)default 0,
            status char(3)not null default 'PRC',
            comments varchar(254),
            lastupdate timestamp,
            refundagainstordid bigint,
            inuse char(1)not null default 'N',
            currency char(3),
            prepared char(1)not null default 'N',
            primary key(rma_id)
        )""")
        cursor.execute("create index i0000213 on rma(rma_id,rmadate)")
        cursor.execute("create index i0000737 on rma(trading_id)")
        cursor.execute("create index i0000738 on rma(policy_id)")
        cursor.execute("create index i0000739 on rma(orgentity_id)")
        cursor.execute("create index i0000740 on rma(ffmcenter_id)")
        cursor.execute("create index i0000741 on rma(member_id)")
        cursor.execute("create index i0000742 on rma(store_id)")
        cursor.execute("create index i0000743x on rma(rma_id,status)")
        # CONSTRAINTS
    
    def rmacharge(self):
        """this table stores charges or credits, applied to a rma, which are not for salable products
        or services. this can be applicable to the entire RMA or to a specific RMA item. such as 
        restocking fees or shipping credits."""
        cursor.execute("""create table rmacharge(
            rmacharge_id bigserial not null,
            rmaitem_id bigint,
            chargetype_id integer not null,
            rma_id bigint not null,
            amount decimal(20,5)not null,
            currency char(3)not null,
            primary key(rmacharge_id)
        )""")
        cursor.execute("create index i0000744 on rmacharge(rmaitem_id)")
        cursor.execute("create index i0000745 on rmacharge(rma_id)")
        cursor.execute("create index i0001280 on rmacharge(chargetype_id)")
        # CONSTRAINT
    
    def rmatax(self):
        "stores rma tax credits"
        cursor.execute("""create table rmatax(
            rma_id bigint not null,
            taxcgry_id integer not null,
            taxamount decimal(20,5)not null,
            lastupdate timestamp not null,
            primary key(rma_id,taxcgry_id)
        )""")
        cursor.execute("create index i0000751 on rmatax(taxcgry_id)")
        # CONSTRAINT
    
    def chargetype(self):
        """charge or credit applied against a transaction which is not for product.
        examples include expedite fees, customization fees and restocking fees"""
        cursor.execute("""create table chargetype(
            chargetype_id serial not null,
            storeent_id integer not null,
            markfordelete integer not null default 0,
            displayaggregated char(1)not null,
            code char(10)not null,
            primary key(chargetype_id)
        )""")
        cursor.execute("create unique index i0000071 on chargetype(storeent_id,code)")
        # CONSTRAINT
    
    def chrgtypdsc(self):
        cursor.execute("""create table chrgtypdsc(
            chargetype_id integer not null,
            language_id integer not null,
            description varchar(254)not null,
            primary key(chargetype_id,language_id)
        )""")

class OrderManagementReceiptAndDisposition:
    """the order management - receipt and disposition data model shows the relationshp
    between database table that contain information about receipt and disposition data for an order"""
    def rtnreason(self):
        "this table stores the reason for customer dissatisfaction with a product"
        cursor.execute("""create table rtnreason(
            reasontype char(1)not null default 'B',
            rtnreason_id serial not null,
            storeent_id integer not null,
            markfordelete integer not null default 0,
            code char(30)not null,
            primary key(rtnreason_id)
        )""")
        cursor.execute("create unique index i0000221 on rtnreason(code,storeent_id)")
        cursor.execute("create index i0000753 on rtnreason(storeent_id)")
        # CONSTRAINT
    
    def rtnrsndesc(self):
        cursor.execute("""create table rtnrsndesc(
            rtnreason_id integer not null,
            language_id integer not null,
            description varchar(254),
            primary key(rtnreason_id)
        )""")
    
    def rtndspdesc(self):
        cursor.execute("""create table rtndspdesc(
            rtndspcode_id integer not null,
            description varchar(254),
            language_id integer not null,
            primary key(rtndspcode_id,language_id)
        )""")
    
    def rtndspcode(self):
        "the table stores return disposition codes to describe how a received item is disposed."
        cursor.execute("""create table rtndspcode(
            rtndspcode_id serial not null,
            returntoinventory char(1)not null default 'Y',
            storeent_id integer not null,
            code char(10)not null,
            markfordelete integer not null default 0,
            primary key(rtndspcode_id)
        )""")
        cursor.execute("create unique index i0000219 on rtndspcode(code,storeent_id)")
        cursor.execute("create index i0000752 on rtndspcode(storeent_id)")
        # CONSTRAINT
    
    def rtnrcptdsp(self):
        "this table describes how a returned item has been disposed"
        cursor.execute("""create table rtnrcptdsp(
            rtndspcode_id integer not null,
            rtnreceipt_id bigint not null,
            rtnrcptdsp_id bigserial not null,
            rtnreason_id integer,
            quantity integer not null,
            dispositiondate timestamp not null,
            comments varchar(254),
            primary key(rtnrcptdsp_id)
        )""")
        cursor.execute("create index i0000220 on rtnrcptdsp(rtnreceipt_id,rtnrcptdsp_id)")
        cursor.execute("create index i0001285 on rtnrcptdsp(rtndspcode_id)")
        cursor.execute("create index i0001286 on rtnrcptdsp(rtnreason_id)")
        # CONSTRAINT
    
    def rtnreceipt(self):
        """this table specifies the receipt record that indicates a returned item from a rma,
        this returned item specifies that the item has been received. it also has information
        about the received items."""
        cursor.execute("""create table rtnreceipt(
            rtnreceipt_id bigserial not null,
            rma_id bigint not null,
            versionspc_id bigint not null,
            rmaitemcmp_id bigint not null,
            lastupdate timestamp not null,
            quantity integer not null,
            datereceived timestamp not null,
            dispocitiondqty integer not null default 0,
            primary key(rtnreceipt_id)
        )""")
        cursor.execute("create index i0000222 on rtnreceipt(rmaitemcmp_id,rtnreceipt_id,datereceived)")
        cursor.execute("create index i0000754 on rtnreceipt(versionspc_id)")
        cursor.execute("create index i0000755 on rtnreceipt(rma_id)")
        # CONSTRAINT
    
    def rmaitemcmp(self):
        "this table descs the smallest unit of inventory involved in a rma"
        cursor.execute("""create table rmaitemcmp(
            rmaitemcmp_id bigserial not null,
            rmaitem_id bigint not null,
            catentry_id bigint,
            itemspc_id bigint not null,
            quantity float not null,
            shouldreceive char(1)not null default 'Y',
            invquantity integer not null default 0,
            primary key(rmaitemcmp_id)
        )""")
        cursor.execute("create index i0000216 on rmaitemcmp(rmaitem_id,rmaitemcmp_id,shouldreceive)")
        cursor.execute("create index i0000750 on rmaitemcmp(catentry_id)")
        cursor.execute("create index i838141 on rmaitemcmp(itemspc_id,rmaitem_id,invquantity)")
        # CONSTRAINT
    
class OrderManagementRMA:
    """the order management - RMA data model shows the relationship between database tables
    that contain information about RMA data for an order."""
    def exchorders(self):
        """each row of this table represents a relationship between an exchanged order
        and its associated return merchandise authorization"""
        cursor.execute("""create table exchorders(
            ex_ord_id bigserial not null,
            rma_id bigint not null,
            cross_ship char(1)not null default 'N',
            primary key(ex_ord_id,rma_id)
        )""")
        cursor.execute("create index i0001257 on exchorders(rma_id)")
        # CONSTRAINT
    
    def rmaauthlog(self):
        """this table is a log of when each rma was authorized.
        a single RMA may appear multiple times if changes were
        made and the rma was re-authorized."""
        cursor.execute("""create table rmaauthlog(
            rmaauthlog_id bigserial not null,
            authnoticedate timestamp not null,
            rma_id bigint not null,
            primary key(rmaauthlog_id)
        )""")
        cursor.execute("create index i0000743 on rmaauthlog(rma_id)")
        # CONSTRAINT

class OrderManagementRMAItem:
    """the order management - RMA Item data model show the relationship between database tables
    that contain information about RMA item data for an Order"""
    def rmaitemserial(self):
        "this table is used to track return serial numbers"
        cursor.execute("""create table rmaitemserial(
            rmaitemserial_id bigserial not null,
            rmaitem_id bigint not null,
            rmaitemcmp_id bigint,
            serialnumber varchar(128),
            quantity float not null,
            receivedquantity float not null,
            creation_timestamp timestamp not null,
            lastupdate timestamp not null,
            primary key(rmaitemserial_id)
        )""")
        cursor.execute("create index i0000976 on rmaitemserial(rmaitem_id,rmaitemcmp_id)")
        cursor.execute("create index i0000977 on rmaitemserial(serialnumber)")
        cursor.execute("create index i0001283 on rmaitemserial(rmaitemcmp_id)")
        # CONSTRAINTS
    
    def rtndnydesc(self):
        cursor.execute("""create table rtndnydesc(
            rtndnyrsn_id integer not null,
            language_id integer not null,
            description varchar(384)not null,
            primary key(rtndnyrsn_id,language_id)
        )""")
    
    def rtndnyrsn(self):
        """this table stores denial reasons for return merchandise authorizatin items.
        these are the reasons for which a RMA was not automatically approved by the system"""
        cursor.execute("""create table rtndnyrsn(
            rtndnyrsn_id serial not null,
            storeent_id integer not null,
            code char(10)not null,
            markfordelete integer not null default 0,
            primary key(rtndnyrsn_id)
        )""")
        cursor.execute("create unique index i0000218 on rtndnyrsn(storeent_id,code)")
        # CONSTRAINT
    
    def rmaidnyrsn(self):
        """a joint table which specifies reasons for denying a RMA item. NOTE: there is no
        similar table for rejecting an RMA . if you wish to reject an entire RMA, you must
        reject each RMA Item individually"""
        cursor.execute("""create table rmaidnyrsn(
            rmaitem_id bigint not null,
            rtndnyrsn_id integer not null,
            primary key(rmaitem_id,rtndnyrsn_id)
        )""")
        cursor.execute("create index i0001281 on rmaidnyrsn(rtndnyrsn_id)")
        # CONSTRAINT
    
class OrderTax:
    """the order tax data model shows the relationship between database tables that contain
    information about tax data for an order."""
    def ordtax(self):
        """each row of this table represents the total of the tax
        amounts of a particular taxcategory for all the items in an order"""
        cursor.execute("""create table ordtax(
            orders_id bigint not null,
            taxcgry_id integer not null,
            taxamount decimal(20,5)not null,
            lastupdate timestamp,
            primary key(orders_id,taxcgry_id)
        )""")
        cursor.execute("create index i0000676 on ordtax(taxcgry_id)")
        # CONSTRAINTS
    
    def orditax(self):
        """each row of this table contains a tax amount of a particular tax category
        for an orderitem. by default you do not save any data in this table, 
        however tax amounts are aggregated by taxcategory in the subordtax and ordtax tables."""
        cursor.execute("""create table orditax(
            orderitems_id bigint not null,
            taxcgry_id integer not null,
            taxamount decimal(20,5)not null,
            taxcgry_dsc varchar(255),
            primary key(orderitems_id,taxcgry_id)
        )""")
        cursor.execute("create index i0000662 on orditax(taxcgry_id)")
        # CONSTRAINTS
    
    def subordtax(self):
        """eac row of this table specifies the tax amount of a particular taxcategory
        for all the order items with the same shipping address as the suborder"""
        cursor.execute("""create table subordtax(
            suborder_id bigint not null,
            taxcgry_id integer not null,
            taxamount decimal(20,5),
            primary key(suborder_id,taxcgry_id)
        )""")
        cursor.execute("create index i0000802 on subordtax(suborder_id,taxcgry_id)")
        # CONSTRAINT

class OrderTradingAgreement:
    """the order trading agreement data model shows the relationship
    between database tables that contain information about order trading agreement"""
    def paysummary(self):
        """each row of this table stores a payment summary data that could be sent
        to an external accounting system. the summary is by store,account and payment policy"""
        cursor.execute("""create table paysummary(
            paysummary_id bigserial not null,
            account_id bigint,
            setccurr char(3),
            creditline_id bigint,
            storeent_id integer not null,
            policy_id bigint,
            periodstarttime timestamp not null,
            periodendtime timestamp not null,
            totalcharge decimal(20,5)not null,
            paysummarydata text,
            status integer,
            primary key(paysummary_id)
        )""")
        cursor.execute("create index i0000686 on paysummary(account_id)")
        cursor.execute("create index i0000687 on paysummary(policy_id)")
        cursor.execute("create index i0000689 on paysummary(creditline_id)")
        cursor.execute("create index i0000690 on paysummary(storeent_id)")
        # CONSTRAINT
    
    def trdrefamt(self):
        """this table is used to keep track of refund amounts by trading agreements
        by orders and by RMA ID. entries are created only for trading agreements
        with right-to-buy by amount or obligation-to-buy by amount terms and conditions"""
        cursor.execute("""create table trdrefamt(
            trdrefamt_id bigserial not null,
            orders_id bigint not null,
            setccurr char(3),
            rma_id bigint not null,
            trading_id bigint not null,
            amount decimal(20,5)not null,
            primary key(trdrefamt_id)
        )""")
        cursor.execute("create index i0000821 on trdrefamt(trading_id)")
        cursor.execute("create index i0000822 on trdrefamt(rma_id)")
        cursor.execute("create index i0000823 on trdrefamt(orders_id)")
        # CONSTRAINT
    
    def trddepamt(self):
        """this table is used to keep track of deposited amounts by trading
        agreements. by orders or orderitems."""
        cursor.execute("""create table trddepamt(
            trddepamt_id bigserial not null,
            orderitems_id bigint,
            orders_id bigint not null,
            trading_id bigint not null,
            setccurr char(3),
            amount decimal(20,5)not null,
            primary key(trddepamt_id)
        )""")
        cursor.execute("create unique index i0000257 on trddepamt(trading_id,orders_id,orderitems_id)")
        cursor.execute("create index i0000816 on trddepamt(orders_id)")
        cursor.execute("create index i0000817 on trddepamt(orderitems_id)")
        # CONSTRAINTS
    
    def trdpuramt(self):
        """this table is used to keep track of purchase amounts by trading agreements
        by orders or orderitems. entries are created only for trading agreement with
        right-to-buy by amount or obligation-to-buy by amount terms and conditions"""
        cursor.execute("""create table trdpuramt(
            trading_id bigint not null,
            trdpuramt_id bigserial not null,
            setccurr char(3),
            orderitems_id bigint,
            amount decimal(20,5)not null,
            orders_id bigint not null,
            primary key(trdpuramt_id)
        )""")
        cursor.execute("create index i0000818 on trdpuramt(trading_id)")
        cursor.execute("create index i0000819 on trdpuramt(orders_id)")
        cursor.execute("create index i0000820 on trdpuramt(orderitems_id)")
        # CONSTRAINT
    
    def orditrd(self):
        """eac row of this table indicates a trading agreement that was searched
        to obtain the price for an orderitem. these rows are created by the 
        orderitemadd and orderitemupdate commands"""
        cursor.execute("""create table orditrd(
            orderitems_id bigint not null,
            trading_id bigint not null,
            primary key(orderitems_id,trading_id)
        )""")
        cursor.execute("create index i0000663 on orditrd(trading_id)")
        # CONSTRAINT
    
    def ordquotrel(self):
        "each row of this table represents a relationship between an order an a child order"
        cursor.execute("""create table ordquotrel(
            parent_id bigint not null,
            child_id bigint,
            ordquotrel_id bigserial not null,
            childstore_id integer,
            trading_id bigint,
            reltype char(16)not null,
            timeouttime timestamp,
            displaysequence float not null default 0,
            flags integer not null default 0,
            primary key(ordquotrel_id)
        )""")
        cursor.execute("create index i0000278 on ordquotrel(child_id)")
        cursor.execute("create index i0000308 on ordquotrel(parent_id,reltype,childstore_id,child_id)")
        cursor.execute("create index i0000309 on ordquotrel(childstore_id,child_id,reltype,parent_id)")
        cursor.execute("create index i0000673 on ordquotrel(trading_id)")
        # CONSTRAINT

class OrderRelease:
    """the order release data model shows the relationship between database tables
    that contain information about release data for an order."""
    def ordrlsttls(self):
        "stores release level charges"
        cursor.execute("""create table ordrlsttls(
            orders_id bigint not null,
            ordreleasenum integer not null,
            chargetype char(70)not null,
            amount decimal(20,5),
            lastcreated timestamp,
            field1 integer,
            field2 varchar(250),
            field3 varchar(250),
            primary key(orders_id,ordreleasenum,chargetype)
        )""")
        # CONSTRAINT

class OrderItem:
    """the order item data model shows the relationship between database tables
    that contain information about order item data"""
    def orditemconf(self):
        """this table is used to check order item shipment
        confirmation and capture the order serial numbers"""
        cursor.execute("""create table orditemconf(
            orditemconf_id bigserial not null,
            orderitems_id bigint not null,
            oicomplist_id bigint,
            serialnumber varchar(128),
            manifest_id bigint,
            ordreleasenum integer not null,
            quantity float not null,
            confirmtype smallint not null,
            creation timestamp,
            lastupdate timestamp not null,
            primary key(orditemconf_id)
        )""")
        cursor.execute("create index i0000974 on orditemconf(orderitems_id,oicomplist_id)")
        cursor.execute("create index i0000975 on orditemconf(serialnumber)")
        cursor.execute("create index i0001268 on orditemconf(oicomplist_id)")
        cursor.execute("create index i0001269 on orditemconf(manifest_id)")
        # CONSTRAINT
    
    def fill_buyerpotyp(self):
        types=[1,2,3,4]
        for t in types:
            cursor.execute("""insert into buyerpotyp(buyerpotyp_id)values(%s) on conflict
            (buyerpotyp_id)do update set buyerpotyp_id=%s""",(t,t,));con.commit()

if __name__=="__main__":
    o=OrderItem()
    o.orditemconf()

    o=OrderRelease()
    o.ordrlsttls()
    
    o=OrderTradingAgreement()
    o.orditrd()
    o.ordquotrel()
    o.paysummary()
    o.trddepamt()
    o.trdpuramt()
    o.trdrefamt()

    o=OrderTax()
    o.orditax()
    o.ordtax()
    o.subordtax()

    o=OrderManagementRMAItem()
    o.rmaidnyrsn()
    o.rmaitemserial()
    o.rtndnydesc()
    o.rtndnyrsn()

    o=OrderManagementRMA()
    o.exchorders()
    o.rmaauthlog()

    o=OrderManagementReceiptAndDisposition()
    o.rmaitemcmp()
    o.rtndspcode()
    o.rtndspdesc()
    o.rtnrcptdsp()
    o.rtnreason()
    o.rtnreceipt()
    o.rtnrsndesc()
    
    o=OrderManagementAdjustmentAndTax()
    o.chargetype()
    o.chrgtypdsc()
    o.rma()
    o.rmacharge()
    o.rmaiadjcrd()
    o.rmaitem()
    o.rmatax()
    
    o=OrderAdjustment()
    o.ordadjdsc()
    o.ordadjtxex()
    o.ordadjust()
    o.ordiadjust()
    o.prcorsn()
    o.prcorsndsc()
    o.subordadj()
    o.suborders()

    o=Order()
    o.ordusers()
    ## o.ordtax()
    o.ordshiphst()
    o.ordpaymthd()
    o.creditline()
    o.ordpayinfo()
    o.ordoptions()
    o.ordertmpl()
    o.orders()
    o.ordermgp()
    o.orderhist()
    o.orderblk()
    o.orcomment()
    o.cpendorder()
    o.buyerpo()
    o.buschn()
    o.blkrsndesc()
    o.blkrsncode()
