from db_con import con,cursor
from functions import build_constraint

class PaymentRules:
    """the payments subsystem data model shows the relationship between database tables
    that contain information about the components that make up the payments subsystem. these components
    store the information to determine how payments are handled by the payment rule engine or the 
    payment plug-in controller module. the data in the database tabes with prefix EDP is manipulated
    by the payment rule engine module in the payments subsystem. the payment plug-in controller module
    in the payments subsystem manipulates the data in the database tables that are prefixed wth the PPC."""
    
    def edppayinst(self):
        "this table stores the information of the value object container Payment Instruction in payment rules."
        cursor.execute("""create table edppayinst(
            edppayinst_id bigserial not null,
            edporder_id bigint,
            amount decimal(20,5)not null,
            sequencenumber integer not null,
            priority integer not null,
            humaneditable integer not null,
            systemeditable integer not null,
            maxamount decimal(20,5)not null default -1.00000,
            minamount decimal(20,5)not null default 0.00000,
            markfordelete integer not null default 0,
            deprecated integer not null default 0,
            dirty integer not null default 0,
            refundallowed integer not null default 0,
            pending integer not null default 0,
            paymentrule varchar(64)not null,
            paymentmethod varchar(64)not null,
            paymentsystem varchar(64)not null,
            backendpiid varchar(64),
            payconfiggroup varchar(64),
            policy_id bigint not null,
            field1 integer,
            field2 varchar(254),
            field3 varchar(254),
            primary key(edppayinst_id)
        )""")
        cursor.execute("create index i0000844 on edppayinst(edporder_id)")
        cursor.execute("create index i0000845 on edppayinst(backendpiid)")
        # CONSTRAINT
    
    def edporder(self):
        """this table stores the information of the value object container Credit for 
        credit-related transactions in the payments subsystem."""
        cursor.execute("""create table edporder(
            edporder_id bigserial not null,
            order_id bigint,
            store_id integer,
            initialamount decimal(20,5)not null default 0.00000,
            totalamount decimal(20,5)not null default 0.00000,
            currency char(3)not null,
            markfordelete integer not null default 0,
            blocked integer not null default 0,
            bgjobstatus integer not null default 0,
            field1 integer,
            field2 varchar(254),
            field3 varchar(254),
            primary key(edporder_id)
        )""")
        cursor.execute("create index i0000843 on edporder(store_id,order_id)")
    
    def edprelease(self):
        "this table stores the information of the value object container Release in the payment rules."
        cursor.execute("""create table edprelease(
            edprelease_id bigint not null,
            edporder_id bigint,
            release_id bigint not null,
            totalamount decimal(20,5)not null default 0.00000,
            reservationamount decimal(20,5)not null default 0.00000,
            finalizationamount decimal(20,5)not null default 0.00000,
            reservingamount decimal(20,5)not null default 0.00000,
            finalizingamount decimal(20,5)not null default 0.00000,
            markfordelete integer not null default 0,
            requestfinalamt decimal(20,5)not null default 0.00000,
            field1 decimal(20,5),
            field2 decimal(20,5),
            field3 varchar(254),
            primary key(edprelease_id)
        )""")
        cursor.execute("create index i0000847 on edprelease(edporder_id)")
        # CONSTRAINT
    
    def edpatmpay(self):
        """this table stores the value object PaymentInstruction which contains the detailed information
        required by plugins to process financial transactions. the amount in the PI can be used by
        plug-ins to determine what is the maximum target amount the payment subsystem intends to consume collectively."""
        cursor.execute("""create table edpatmpay(
            edpatmpay_id bigserial not null,
            edppayinst_id bigint,
            totalamount decimal(20,5)not null default 0.00000,
            validationamount decimal(20,5)not null,
            reservationamount decimal(20,5)not null default 0.00000,
            finalizationamount decimal(20,5)not null default 0.00000,
            validatingamount decimal(20,5)not null default 0.00000,
            reservingamount decimal(20,5)not null default 0.00000,
            finalizingamount decimal(20,5)not null default 0.00000,
            markfordelete integer not null default 0,
            backendpaymentid varchar(64),
            field1 decimal(20,5),
            field2 decimal(20,5),
            field3 varchar(254),
            primary key(edpatmpay_id)
        )""")
        cursor.execute("create index i0000846 on edpatmpay(edppayinst_id)")
        # CONSTRAINTS
    
    def edppayhist(self):
        """this table keeps the payment activity history for all committed operations
        on payment instructions and financial transactions."""
        cursor.execute("""create table edppayhist(
            edppayhist_id bigserial not null,
            order_id bigint,
            rma_id bigint,
            store_id integer,
            histtimestamp timestamp not null,
            amount decimal(20,5)not null default 0.00000,
            operationname varchar(64)not null,
            operationresult varchar(64)not null,
            readablestatus varchar(64),
            recordtype varchar(64),
            backendpiid varchar(64),
            backendpaymentid varchar(64),
            account varchar(64),
            edppayinst_id bigint,
            field1 integer,
            field2 varchar(254),
            field3 varchar(254),
            primary key(edppayhist_id)
        )""")
        cursor.execute("create index i0000850 on edppayhist(order_id,store_id)")
        cursor.execute("create index i0000910 on edppayhist(edppayhist_id)")
        # CONSTRAINT
    
    def edprelhist(self):
        "this table keeps the history for all operations on releases in PaymentRules"
        cursor.execute("""create table edprelhist(
            edppayhist_id bigint not null,
            order_id bigint not null,
            release_id bigserial not null,
            store_id integer not null,
            field1 integer,
            field2 varchar(254),
            field3 varchar(254),
            primary key(edppayhist_id,order_id,release_id,store_id)
        )""")
        cursor.execute("create index i0000852 on edprelhist(order_id,release_id,store_id)")
        # CONSTRAINT
    
    def edpatmref(self):
        """this table stores the value object PaymentInstruction which contains the detailed information
        required by plugins to process financial transactions. the amount in the payment instruction can be used
        by plug-ins to determine what is the max target amount the payments subsystem intends to consume collectively."""
        cursor.execute("""create table edpatmref(
            edpatmref_id bigserial not null,
            edprefinst_id bigint,
            totalamount decimal(20,5)not null default 0.0000,
            refundingamount decimal(20,5)not null default 0.00000,
            markfordelete integer not null default 0,
            backendrefundid varchar(64),
            field1 decimal(20,5),
            field2 decimal(20,5),
            field3 varchar(254),
            primary key(edpatmref_id)
        )""")
        cursor.execute("create index i0000851 on edpatmref(edprefinst_id)")
        # CONSTRAINTS
    
    def edprefinst(self):
        """this table stores the information of the value object container
        RefundInstruction in PaymentRules"""
        cursor.execute("""create table edprefinst(
            edprefinst_id bigserial not null,
            edprma_id bigint,
            amount decimal(20,5)not null,
            sequencenumber integer not null,
            priority integer not null,
            markfordelete integer not null default 0,
            deprecated integer not null default 0,
            dirty integer not null default 0,
            pending integer not null default 0,
            paymentsystem varchar(64)not null,
            refundmethod varchar(64)not null,
            backendriid varchar(64),
            policy_id bigint not null,
            field1 integer,
            field2 varchar(254),
            field3 varchar(254),
            primary key(edprefinst_id)
        )""")
        cursor.execute("create index i0000849 on edprefinst(edprma_id)")
        # CONSTRAINT
    
    def edprma(self):
        """this table stores the information of the value object container Refund in PaymentRules."""
        cursor.execute("""create table edprma(
            edprma_id bigserial not null,
            rma_id bigint,
            store_id integer not null,
            amount decimal(20,5)not null default 0.00000,
            currency char(3)not null,
            markfordelete integer not null default 0,
            blocked integer not null default 0,
            bgjobstatus integer not null default 0,
            field1 integer,
            field2 varchar(254),
            field3 varchar(254),
            primary key(edprma_id)
        )""")
        cursor.execute("create index i0000848 on edprma(store_id,rma_id)")

class PaymentPluginController:
    def ppcpayment(self):
        """this table stores the information of the value object container
        Payment for payment-related transactions in the payments subsystem."""
        cursor.execute("""create table ppcpayment(
            ppcpayment_id bigint not null,
            ppcpayinst_id bigint not null,
            ppcpaytran_id bigint,
            avscommoncode smallint not null default 0,
            expectedamount decimal(20,5)not null,
            approvingamount decimal(20,5)not null default 0.00000,
            approvedamount decimal(20,5)not null default 0.00000,
            depositingamount decimal(20,5)not null default 0.00000,
            depositedamount decimal(20,5)not null default 0.00000,
            creditingamount decimal(20,5)not null default 0.00000,
            creditedamount decimal(20,5)not null default 0.00000,
            rvrsngapprvedamnt decimal(20,5)not null default 0.00000,
            state smallint not null,
            timeexpired timestamp,
            timecreated timestamp not null,
            timeupdated timestamp not null,
            markfordelete integer not null default 0,
            primary key(ppcpayment_id)
        )""")
        cursor.execute("create index i0000920 on ppcpayment(ppcpayinst_id)")
        # CONSTRAINT
    
    def ppcpayinst(self):
        """this table stores the value object PaymentInstruction in which contains the detailed information
        required by plug-ins to process financial transactions. the amount in the payment instruction can be
        used by plug-ins to determine what is the max target amount the payments subsystem intends to consume.
        collectively."""
        cursor.execute("""create table ppcpayinst(
            ppcpayinst_id bigserial not null,
            order_id bigint,
            rma_id bigint,
            store_id integer not null,
            amount decimal(20,5)not null,
            approvingamount decimal(20,5)not null default 0.00000,
            approvedamount decimal(20,5)not null default 0.00000,
            creditingamount decimal(20,5)not null default 0.00000,
            creditedamount decimal(20,5)not null default 0.00000,
            depositingamount decimal(20,5)not null default 0.00000,
            depositedamount decimal(20,5)not null default 0.00000,
            rvrsngapprvedamnt decimal(20,5)not null default 0.00000,
            rvrsngcredtedamnt decimal(20,5)not null default 0.00000,
            timecreated timestamp not null,
            currency char(3)not null,
            state smallint not null default 0,
            markfordelete integer not null default 0,
            pluginname varchar(64)not null,
            paymentsystemname varchar(64)not null,
            accountnumber varchar(512),
            payconfigid varchar(64)not null,
            primary key(ppcpayinst_id)
        )""")
        cursor.execute("create index i0000918 on ppcpayinst(order_id,markfordelete)")
        cursor.execute("create index i0000919 on ppcpayinst(rma_id,markfordelete)")
    
    def ppccredit(self):
        """this table stores the information of the value object container
        Credit for credit related transactions in the payment subsystem."""
        cursor.execute("""create table ppccredit(
            ppccredit_id bigserial not null,
            ppcpayinst_id bigint not null,
            ppcpayment_id bigint,
            expectedamount decimal(20,5)not null,
            creditingamount decimal(20,5)not null default 0.00000,
            rvrsngcrdtedamnt decimal(20,5)not null default 0.00000,
            state smallint not null,
            timecreated timestamp not null,
            timeupdated timestamp not null,
            markfordelete integer not null default 0,
            primary key(ppccredit_id)
        )""")
        cursor.execute("create index i0000922 on ppccredit(ppcpayinst_id)")
        cursor.execute("create index i0000923 on ppccredit(ppcpayment_id)")
        # CONSTRAINT

    def ppcpaytran(self):
        "stores the information of a financial transaction processed by a payment plug-in"
        cursor.execute("""create table ppcpaytran(
            ppcpaytran_id bigserial not null,
            ppcpayment_id bigint,
            ppccredit_id bigint,
            transactiontype smallint not null,
            requestedamount decimal(20,5)not null,
            processedamount decimal(20,5)not null default 0.00000,
            state smallint not null,
            timecreated timestamp not null,
            timeupdated timestamp not null,
            markfordelete integer not null default 0,
            responsecode varchar(25),
            reasoncode varchar(25),
            referencenumber varchar(64),
            trackingid varchar(64),
            ppcbatch_id bigint,
            primary key(ppcpaytran_id)
        )""")
        cursor.execute("create index i0000924 on ppcpaytran(ppcpayment_id)")
        cursor.execute("create index i0000925 on ppcpaytran(ppccredit_id)")
        cursor.execute("create index i0001103 on ppcpaytran(ppcbatch_id)")
        # CONSTRAINT
    
    def ppcextdata(self):
        """this table stores the non-standard protocol data required in the financial transaction
        which goes beyond the standard attributes defined in te payment instruction. it can be asociated
        with a payment instruction or a financial transaction. when associated with a payment instruction, it
        can be used by all the financial transactions executed against the same payment instruction. when associated
        with a financial transaction, this extra data can be used by the same transaction and subsequent transactions."""
        cursor.execute("""create table ppcextdata(
            ppcextdata_id bigserial not null,
            ppcpayinst_id bigint,
            ppcpaytran_id bigint,
            attributetype smallint not null,
            encrypted smallint not null default 0,
            markfordelete integer not null default 0,
            attributename varchar(64)not null,
            searchvalue varchar(64),
            datavalue varchar(4000),
            ppcbatch_id bigint,
            primary key(ppcextdata_id)
        )""")
        cursor.execute("create index i0000926 on ppcextdata(ppcpayinst_id)")
        cursor.execute("create index i0000927 on ppcextdata(ppcpaytran_id)")
        cursor.execute("create index i0000962 on ppcextdata(searchvalue)")
        cursor.execute("create index i0001106 on ppcextdata(ppcbatch_id)")
        # CONSTRAINT

class PaymentMerchantSupport:
    """the payment merchant support data model shows the relationship between database tables that contain
    information about payment merchant support. merchant information is used by the payment side to 
    facilitate payment operation and management."""
    def merchant(self):
        """this table stores the information of the value object container Credit 
        for credit-related transactions in the payments subsystem."""
        cursor.execute("""create table merchant(
            merchant_id bigserial not null,
            member_id bigint not null,
            name varchar(254)not null,
            state smallint default 1,
            field1 integer,
            field2 varchar(250),
            field3 varchar(250),
            primary key(merchant_id)
        )""")
        cursor.execute("create index i0001262 on merchant(member_id)")
        # CONSTRAINT
    
    def merchconf(self):
        """this table stores the information of the value container credit for
        credit-related transactions in the payments subsystem."""
        cursor.execute("""create table merchconf(
            merchconf_id bigserial not null,
            merchant_id bigint not null,
            paymentsystem varchar(64)not null,
            payconfgrp varchar(64)not null,
            field1 integer,
            field2 varchar(250),
            field3 varchar(250),
            primary key(merchconf_id)
        )""")
        cursor.execute("create unique index i0000972 on merchconf(merchant_id,paymentsystem,payconfgrp)")
        # CONSTRAINT
    
    def merchconfinfo(self):
        "this table stores the NVPs for properties of merchant information for a specific merchant configuration."
        cursor.execute("""create table merchconfinfo(
            merchconfinfo_id bigserial not null,
            merchconf_id bigint not null,
            property_name varchar(64)not null,
            property_value varchar(4000)not null,
            encrypted smallint not null default 1,
            primary key(merchconfinfo_id)
        )""")
        cursor.execute("create unique index i0000973 on merchconfinfo(merchconf_id,property_name)")
        # CONSTRAINTS
    
    def storemerch(self):
        "stores the mapping information to indicate which merchant id is used for a specific store."
        cursor.execute("""create table storemerch(
            store_id integer not null,
            merchant_id bigint not null,
            field1 integer,
            field2 varchar(250),
            field3 varchar(250),
            primary key(store_id)
        )""")
        cursor.execute("create index i0001289 on storemerch(merchant_id)")
        # CONSTRAINT
    
    def ppcbatch(self):
        "the batch object representing the bacth transaction"
        cursor.execute("""create table ppcbatch(
            ppcbatch_id bigserial not null,
            merchconf_id bigint not null,
            state smallint not null default 0,
            timecreated timestamp not null,
            timeupdated timestamp not null,
            timeclosed timestamp,
            markfordelete integer not null default 0,
            field1 integer,
            field2 varchar(254),
            field3 varchar(254),
            primary key(ppcbatch_id)
        )""")
        cursor.execute("create index i0001107 on ppcbatch(merchconf_id)")
        cursor.execute("create index i0001108 on ppcbatch(state)")
        # CONSTRAINT
    
if __name__=="__main__":
    p=PaymentRules()
    p.edprma()
    p.edprelhist()
    p.edprelease()
    p.edprefinst()
    p.edppayinst()
    p.edppayhist()
    p.edporder()
    p.edpatmref()
    p.edpatmpay()

    p=PaymentPluginController()
    p.ppccredit()
    p.ppcextdata()
    p.ppcpayinst()
    p.ppcpayment()
    p.ppcpaytran()

    p=PaymentMerchantSupport()
    p.merchant()
    p.merchconf()
    p.merchconfinfo()
    p.ppcbatch()
    p.storemerch()

