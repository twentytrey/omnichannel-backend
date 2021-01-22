from db_con import con,cursor
from functions import build_constraint

class ATPInventory:
    """the ATP inventory data model shows the relationship
    between database tables that contain information about ATP INVENTORY"""

    def distarrang(self):
        """each row of this table represents a distribution
        arrangement. enabling a store to sell its own inventory."""
        cursor.execute("""create table distarrang(
            distarrang_id bigserial not null,
            merchantstore_id integer not null,
            pickingmethod char(1),
            startdate timestamp not null,
            enddate timestamp not null,
            field1 varchar(254),
            field2 varchar(254),
            field3 varchar(254),
            wholesalestore_id integer not null,
            baseitem_id bigint not null,
            lastupdate timestamp,
            primary key(distarrang_id)
        )""")
        cursor.execute("create unique index i0000095 on distarrang(baseitem_id,merchantstore_id,wholesalestore_id,startdate,enddate)")
        cursor.execute("create index i0000347 on distarrang(distarrang_id,merchantstore_id)")
        cursor.execute("create index i0000560 on distarrang(merchantstore_id)")
        cursor.execute("create index i0000561 on distarrang(wholesalestore_id)")
        # CONSTRAINTS:
    
    def storeitem(self):
        """each row of this table contain attributes that affect how a particular store
        allocates inventory for the specified items of a particular base item. if there is 
        no row for the store, then the row for the store group is used."""
        cursor.execute("""create table storeitem(
            baseitem_id bigint not null,
            storeent_id integer not null,
            trackinginventory char(1)not null default 'Y',
            forcebackorder char(1)not null default 'N',
            releaseseparately char(1)not null default 'N',
            foreignsku char(20),
            foreignsystem bigint,
            lastupdate timestamp,
            creditable char(1)not null default 'Y',
            backorderable char(1)not null default 'Y',
            returnnotdesired char(1) default 'N',
            minqtyforsplit integer not null default 0,
            primary key(baseitem_id,storeent_id)
        )""")
        cursor.execute("create index i0000791 on storeitem(storeent_id)")
        # CONSTRAINTS
    
    def rcptavail(self):
        "defines which distarrang have access to received inventory"
        cursor.execute("""create table rcptavail(
            rcptavail_id bigserial not null,
            distarrang_id bigint not null,
            receipt_id bigint not null,
            precedence integer,
            lastupdate timestamp,
            primary key(rcptavail_id)
        )""")
        cursor.execute("create unique index i0000203 on rcptavail(distarrang_id,receipt_id)")
        cursor.execute("create index i0000714 on rcptavail(receipt_id)")
        # CONSTRAINTS
    
    def receipt(self):
        "each row contains information about receipt of an item at a ffmcenter"
        cursor.execute("""create table receipt(
            receipt_id bigserial not null,
            versionspc_id bigint not null,
            radetail_id bigint,
            store_id integer not null,
            setccurr char(3),
            ffmcenter_id integer not null,
            vendor_id bigint,
            receiptdate timestamp not null,
            qtyreceived integer not null default 0,
            qtyinprocess integer not null default 0,
            qtyonhand integer not null default 0,
            qtyinkits integer not null default 0,
            cost decimal(20,5),
            comment1 varchar(254),
            comment2 varchar(254),
            lastupdate timestamp,
            createtime timestamp not null,
            receipttype char(4)not null default 'ADHC',
            rtnrcptdsp_id bigint,
            primary key(receipt_id)
        )""")
        cursor.execute("create unique index i0000204 on receipt(versionspc_id,ffmcenter_id,store_id,createtime)")
        cursor.execute("create index i0000205 on receipt(receipt_id,radetail_id,receiptdate)")
        cursor.execute("create index i0000715 on receipt(radetail_id)")
        cursor.execute("create index i0000716 on receipt(ffmcenter_id)")
        cursor.execute("create index i0000717 on receipt(store_id)")
        cursor.execute("create index i0001276 on receipt(vendor_id)")
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
    
    def itemffmctr(self):
        """each row contains information about reserved quantities,amount on
        backorder, and amount allocated to backorders for items owned by a store
        at a fulfillment center"""
        cursor.execute("""create table itemffmctr(
            itemspc_id bigint not null,
            store_id integer not null,
            ffmcenter_id integer not null,
            qtybackordered integer not null default 0,
            qtyallocbackorder integer not null default 0,
            lastupdate timestamp,
            qtyreserved integer not null default 0,
            restocktime timestamp,
            primary key(itemspc_id,store_id,ffmcenter_id)
        )""")
        cursor.execute("create index i0000597 on itemffmctr(ffmcenter_id)")
        cursor.execute("create index i0000598 on itemffmctr(store_id)")
        # CONSTRAINTS
    
    def invreserve(self):
        """each row contains information about existing inventory that has been
        reserved for such purposes as auctions. this reserved inventory is not available
        for customer orders until the reservation is reversed."""
        cursor.execute("""create table invreserve(
            invreserve_id bigserial not null,
            invrsrvtyp_id bigint not null,
            quantity integer,
            description varchar(254),
            expiration timestamp,
            itemspc_id bigint,
            lastupdate timestamp,
            store_id integer,
            ffmcenter_id integer,
            primary key(invreserve_id)
        )""")
        cursor.execute("create index i0001260 on invreserve(itemspc_id,store_id,ffmcenter_id)")
        # CONSTRAINTS
    
    def invrsrvtyp(self):
        """each row contains user-defined reservation 
        types that can be used when reserving inventory."""
        cursor.execute("""create table invrsrvtyp(
            invrsrvtyp_id bigserial not null,
            primary key(invrsrvtyp_id)
        )""")

    def invrsrvdsc(self):
        """each row contains language-specific descriptions for
        the types of inventory reservations that the user has defined."""
        cursor.execute("""create table invrsrvdsc(
            invrsrvtyp_id bigint not null,
            language_id integer not null,
            name varchar(254),
            description varchar(254),
            primary key(invrsrvtyp_id,language_id)
        )""")
    
    def invitmvw(self):
        """this is a view derived from the receipt and itemffmctr tables which 
        contains the existing quantity available for an item across all stores
        and fulfillment centers."""
        cursor.execute("""create table invitmvw(
            itemspc_id bigint not null,
            receiptquantity integer,
            qtyavailable integer
        )""")
    
    def rcptitmvw(self):
        """a view which summarizes the quantity of inventory
        available from the receipt table for an item across all
        stores and fulfillment centers."""
        cursor.execute("""create table rcptitmvw(
            itemspc_id bigint not null,
            receiptquantity integer
        )""")
    
    def invstffmvw(self):
        """this is a view derived from the receipt and itemffmctr
        tables which contains the existing quantity available for an item
        at a store and fulfillment center."""
        cursor.execute("""create table invstffmvw(
            store_id integer not null,
            ffmcenter_id integer not null,
            itemspc_id bigint not null,
            qtyavailable integer
        )""")
    
    def rcptstffvw(self):
        """a view which summarizes the quantity of inventory
        available from the receipt table for an item owned 
        by a store at a fulfillment center."""
        cursor.execute("""create table rcptstffvw(
            itemspc_id bigint not null,
            store_id integer not null,
            ffmcenter_id integer not null,
            receiptquantity integer
        )""")
    
    def invstvw(self):
        """this is a view derived from the receipt and itemffmctr tables
        which contain the existing quantity available for an item for a given
        store across all fulfillment centers."""
        cursor.execute("""create table invstvw(
            store_id integer not null,
            itemspc_id bigint not null,
            qtyavailable integer,
            quantitymeasure char(16)not null
        )""")
    
    def rcptstvw(self):
        """a view which summarizes the quantity of inventory available from the receipt
        table for an item owned by a store across all fulfillment center."""
        cursor.execute("""create table rcptstvw(
            itemspc_id bigint not null,
            store_id integer not null,
            receiptquantity integer
        )""")

class ATPInventoryAdjustment:
    """this model shows the relationship between database tables
    that contain information about ATP inventory adjustments"""
    def invadjust(self):
        "this table records adjustments made to inventory"
        cursor.execute("""create table invadjust(
            invadjust_id bigserial not null,
            invadjustnum integer not null,
            invadjcode_id bigint not null,
            receipt_id bigint not null,
            adjustmentdate timestamp,
            quantity integer,
            adjustmentcomment varchar(562),
            lastupdate timestamp,
            primary key(invadjust_id,invadjustnum)
        )""")
        cursor.execute("create index i0000136 on invadjust(invadjust_id,invadjcode_id,adjustmentdate)")
        cursor.execute("create index i0000592 on invadjust(receipt_id)")
        cursor.execute("create index i0000593 on invadjust(invadjcode_id)")
        # CONSTRAINTS
    
    def invadjcode(self):
        """each row of this table defines an inventory adjustment code for a store
        or the stores in the store group. each code represents a reason for
        an inventory adjustment such as broken, lost or found."""
        cursor.execute("""create table invadjcode(
            invadjcode_id bigserial not null,
            adjustcode char(10)not null,
            lastupdate timestamp,
            storeent_id integer not null,
            markfordelete integer not null,
            primary key(invadjcode_id)
        )""")
        cursor.execute("create unique index i0000135 on invadjcode(adjustcode,storeent_id)")
        cursor.execute("create index i0000591 on invadjcode(storeent_id)")
        # CONSTRAINTS
    
    def invadjdesc(self):
        """each row of this table contains lang-dependent information 
        about an inventory adjustment code"""
        cursor.execute("""create table invadjdesc(
            invadjcode_id bigint not null,
            description varchar(512),
            language_id integer not null,
            lastupdate timestamp,
            primary key(invadjcode_id,language_id)
        )""")
    
class ATPExpectedInventory:
    """the ATP expected inventory datamodel shows the relationship
    between database tables that contain information about ATP expected inventory"""
    def ra(self):
        """records general information about inventory expected from a vendor
        RA stands for Replenishment Advisement. however the term expected inventory
        record is used to mean the same thing."""
        cursor.execute("""create table ra(
            ra_id bigserial not null,
            vendor_id bigint not null,
            store_id integer not null,
            orderdate timestamp not null,
            openindicator char(1),
            dateclosed timestamp,
            lastupdate timestamp,
            externalid char(50),
            markfordelete integer not null default 0,
            createtime timestamp not null,
            primary key(ra_id)
        )""")
        cursor.execute("create unique index i0000200 on ra(store_id,vendor_id,createtime)")
        cursor.execute("create index i0001275 on ra(vendor_id)")
        # CONSTRAINTS
    
    def radetail(self):
        "contains detailed info about items on an expected inv. record."
        cursor.execute("""create table radetail(
            radetail_id bigserial not null,
            ra_id bigint not null,
            ffmcenter_id integer,
            itemspc_id bigint not null,
            qtyordered integer not null default 0,
            qtyreceived integer not null default 0,
            qtyremaining integer not null default 0,
            qtyallocated integer not null default 0,
            expecteddate timestamp not null,
            radetailcomment varchar(254),
            lastupdate timestamp,
            markfordelete integer not null default 0,
            primary key(radetail_id)
        )""")
        cursor.execute("create index i0000201 on radetail(ra_id,ffmcenter_id,itemspc_id,expecteddate)")
        cursor.execute("create index i0000202 on radetail(ra_id,radetail_id,expecteddate)")
        cursor.execute("create index i0000712 on radetail(itemspc_id)")
        cursor.execute("create index i0000713 on radetail(ffmcenter_id)")
        # CONSTRAINTS
    
    def rabackallo(self):
        """each row contains information about how backorders
        are allocated against expected inventory"""
        cursor.execute("""create table rabackallo(
            rabackallonum serial not null,
            radetail_id bigint not null,
            itemspc_id bigint not null,
            orderitems_id bigint not null,
            qtyallocated integer,
            lastupdate timestamp,
            primary key(orderitems_id,rabackallonum)
        )""")
        cursor.execute("create index i0000710 on rabackallo(itemspc_id)")
        cursor.execute("create index i0000711 on rabackallo(radetail_id)")
        # CONSTRAINTS
    
class ATPFulfillment:
    """this data model shows the relationship between database tables that contain
    information about ATP inventory fulfillment."""
    def orders(self):
        "each row of this table represents an order in a store"
        cursor.execute("""create table orders(
            orders_id bigserial not null,
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
            comments varchar(512),
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
    
    def orderitems(self):
        "each row represents an order item in an order"
        cursor.execute("""create table orderitems(
            orderitems_id bigserial not null,
            storeent_id integer not null,
            orders_id bigint not null,
            termcond_id bigint,
            trading_id bigint,
            itemspc_id bigint,
            catentry_id bigint,
            partnum varchar(254),
            shipmode_id integer,
            ffmcenter_id integer,
            member_id bigint not null,
            address_id bigint,
            allocaddress_id bigint,
            price decimal(20,5),
            lineitemtype char(4),
            status char(1)not null,
            outputq_id bigint,
            inventorystatus char(4)not null default 'NALC',
            lastcreate timestamp,
            lastupdate timestamp,
            fulfillmentstatus char(4)not null default 'INT',
            lastallocupdate timestamp,
            offer_id bigint,
            timereleased timestamp,
            timeshipped timestamp,
            currency char(10),
            comments varchar(512),
            totalproduct decimal(20,5)default 0,
            quantity float not null,
            taxamount decimal(20,5),
            totaladjustment decimal(20,5)default 0,
            shiptaxamount decimal(20,5),
            estavailtime timestamp,
            field1 integer,
            description varchar(254),
            field2 varchar(254),
            allocationgroup bigint,
            shipcharge decimal(20,5),
            baseprice decimal(20,5),
            basecurrency char(3),
            tracknumber varchar(64),
            trackdate timestamp,
            prepareflags integer not null default 0,
            correlationgroup bigint,
            promisedavailtime timestamp,
            shippingoffset integer not null default 0,
            neededquantity integer not null default 0,
            allocquantity integer not null default 0,
            allocffmc_id integer,
            ordreleasenum integer,
            configurationid varchar(128),
            supplierdata varchar(512),
            supplierpartnumber varchar(254),
            availaquantity integer,
            isexpedited char(1)not null default 'N',
            requestedshipdate timestamp,
            tiecode smallint,
            primary key(orderitems_id)
        )""")
        cursor.execute("create index i0000173 on orderitems(orderitems_id,timereleased,timeshipped,inventorystatus)")
        cursor.execute("create index i0000360 on orderitems(orderitems_id,ordreleasenum,orders_id)")
        cursor.execute("create index i0000369 on orderitems(storeent_id)")
        cursor.execute("create index i0000639 on orderitems(allocaddress_id)")
        cursor.execute("create index i0000640 on orderitems(trading_id)")
        cursor.execute("create index i0000641 on orderitems(termcond_id)")
        cursor.execute("create index i0000642 on orderitems(shipmode_id)")
        cursor.execute("create index i0000643 on orderitems(ffmcenter_id)")
        cursor.execute("create index i0000644 on orderitems(offer_id)")
        cursor.execute("create index i0000645 on orderitems(catentry_id)")
        cursor.execute("create index i0000646 on orderitems(member_id)")
        cursor.execute("create index i0000647 on orderitems(address_id)")
        cursor.execute("create index i0000648 on orderitems(itemspc_id)")
        cursor.execute("create index i0000649 on orderitems(allocffmc_id)")
        cursor.execute("create index i172138 on orderitems(orders_id,ordreleasenum,storeent_id,ffmcenter_id)")
        # CONSTRAINTS
    
    def ordrelease(self):
        """each row of this table represents an order release. the release
        is a grouping of all order items in an order that are to be shipped
        on the same date to the same address. the order items also use the
        same shipping mode from the same fulfillment center."""
        cursor.execute("""create table ordrelease(
            ordreleasenum serial not null,
            orders_id bigint not null,
            ffmacknowledgement timestamp,
            status char(4),
            customerconfirm timestamp,
            field1 integer,
            field2 varchar(254),
            field3 varchar(254),
            pickbatch_id bigint,
            timeplaced timestamp,
            lastupdate timestamp,
            packslip text,
            capturedate timestamp,
            extordnum varchar(64),
            extref varchar(2048),
            ffmcenter_id integer,
            isexpedited char(1)not null default 'N',
            shipmode_id integer,
            address_id bigint,
            member_id bigint,
            storeent_id integer,
            primary key(orders_id,ordreleasenum)
        )""")
        cursor.execute("create index i0000180 on ordrelease(status,orders_id,ordreleasenum,pickbatch_id)")
        cursor.execute("create index i0000836 on ordrelease(ffmcenter_id)")
        cursor.execute("create index i0000837 on ordrelease(shipmode_id)")
        cursor.execute("create index i0000838 on ordrelease(address_id)")
        cursor.execute("create index i0000839 on ordrelease(member_id)")
        cursor.execute("create index i0000840 on ordrelease(storeent_id)")
        cursor.execute("create index i803140 on ordrelease(pickbatch_id)")
        # CONSTRAINTS:
    
    def manifest(self):
        """one record exists for each manifest (shipment confirmation) produced
        for an order release. if a release is packaged in two boxes there will
        be two rows in the manifest table."""
        cursor.execute("""create table manifest(
            manifest_id bigserial not null,
            ordreleasenum integer not null,
            weightmeasure char(16),
            setccurr char(3),
            shipmode_id integer,
            weight float,
            manifeststatus char(1)not null default 'S',
            shippingcosts decimal(20,5)not null,
            dateshipped timestamp not null,
            field1 varchar(254),
            lastupdate char(20),
            packageid char(20),
            trackingid varchar(40),
            pickuprecordid char(20),
            orders_id bigint not null,
            primary key(manifest_id)
        )""")
        cursor.execute("create index i0000364 on manifest(orders_id,ordreleasenum,manifeststatus)")
        cursor.execute("create index i0000609 on manifest(shipmode_id)")
        # CONSTRAINTS
    
    def ordshiphst(self):
        """each row contains information about inventory that has
        been released for fulfillment of an order item."""
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
        # CONSTRAINTS
    
    def ordpickhst(self):
        """details of how inventory was picked from the receipt
        level when available inventory is allocated to an order item."""
        cursor.execute("""create table ordpickhst(
            ordpickhstnum serial not null,
            orderitems_id bigint not null,
            versionspc_id bigint not null,
            receipt_id bigint,
            qtypicked integer,
            datepicked timestamp,
            orderpickingtype integer,
            lastupdate timestamp,
            primary key(orderitems_id,ordpickhstnum)
        )""")
        cursor.execute("create index i0000462 on ordpickhst(orderitems_id,versionspc_id,qtypicked)")
        cursor.execute("create index i0000671 on ordpickhst(receipt_id)")
        cursor.execute("create index i0000672 on ordpickhst(versionspc_id)")
        # CONSTRAINTS
    
    def pickbatch(self):
        """this table contains pick batch information. a pick batch groups together
        order releases for their processsing as a unit at a fulfillment center.
        it picks inventory for orderitems, packs them into boxes and ships to customer
        through selected carrier."""
        cursor.execute("""create table pickbatch(
            pickbatch_id bigserial not null,
            lastupdate timestamp,
            ffmcenter_id integer not null,
            member_id bigint,
            pickslip text,
            field1 integer,
            field2 varchar(254),
            field3 varchar(254),
            date1 timestamp,
            date2 timestamp,
            primary key(pickbatch_id)
        )""")
        cursor.execute("create index i0000691 on pickbatch(member_id)")
        cursor.execute("create index i0000692 on pickbatch(ffmcenter_id)")
        # CONSTRAINTS

class ATPInventoryOrders:
    """the ATP inventory data model shows the relationship
    between database tables that contain information about
    ATP inventory orders."""
    
    def storitmffc(self):
        """each row of this table contains information about a baseitem for
        a particular store (or all the stores in the storegroup) and the ffmcenter"""
        cursor.execute("""create table storitmffc(
            baseitem_id bigint not null,
            storeent_id integer not null,
            ffmcenter_id integer not null,
            shippingoffset integer not null default 86400,
            primary key(baseitem_id,storeent_id,ffmcenter_id)
        )""")
        cursor.execute("create index i0000797 on storitmffc(ffmcenter_id)")
        cursor.execute("create index i0000798 on storitmffc(storeent_id)")
        # CONSTRAINTS
    
    def bkorditem(self):
        "each row contains the expected ship date of a backordered item"
        cursor.execute("""create table bkorditem(
            orderitems_id bigint not null,
            dateexpected timestamp,
            lastupdate timestamp,
            primary key(orderitems_id)
        )""")
        # CONSTRAINTS
    
    def bkordalloc(self):
        """each row contains information about the quantity required
        for this backordered order item and the amount of available
        inventory allocated to this item."""
        cursor.execute("""create table bkordalloc(
            bkordnum serial not null,
            orderitems_id bigint not null,
            itemspc_id bigint not null,
            qtyneeded integer,
            qtyavailable integer,
            qtyallocated integer,
            lastupdate timestamp,
            primary key(orderitems_id,bkordnum)
        )""")
        cursor.execute("create index i0000481 on bkordalloc(itemspc_id)")
        # CONSTRAINTS

if __name__=="__main__":
    a=ATPInventoryOrders()
    a.storitmffc()
    a.bkorditem()
    a.bkordalloc()

    a=ATPFulfillment()
    a.manifest()
    a.orderitems()
    # a.orders()
    a.ordpickhst()
    a.ordrelease()
    # a.ordshiphst()
    a.pickbatch()

    a=ATPExpectedInventory()
    a.radetail()
    a.rabackallo()
    a.ra()

    a=ATPInventoryAdjustment()
    a.invadjust()
    a.invadjdesc()
    a.invadjcode()

    a=ATPInventory()
    a.storeitem()
    ## a.rtnrcptdsp()
    a.receipt()
    a.rcptstvw()
    a.rcptstffvw()
    a.rcptitmvw()
    a.rcptavail()
    a.itemffmctr()
    a.invstvw()
    a.invstffmvw()
    a.invrsrvtyp()
    a.invrsrvdsc()
    a.invreserve()
    a.invitmvw()
    a.distarrang()
