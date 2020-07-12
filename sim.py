from ops.filehandlers.simpos import *
from requester import MakeRequests
from random import choice,shuffle,randrange
import time,datetime
from ops.helpers.functions import datetimestamp_now,todayplusdelta
from ops.filehandlers.filehandlers import InstallCatentries,cursor,con
from ops.fulfillment.fulfillment import Inventory
from ops.catalog.catalog import CatalogItem
from ops.calculations.shippingmethods import ShippingMethods
from ops.helpers.functions import datetimestamp_now,timestamp_now,datetimestamp_forever,human_format
from ops.inventory.inventory import InventoryItem,Ra,DisplayItems
from ops.stores.stores import MDefaultContract
from ops.analytics.analytics import RFM,DashboardCounts,SalesMatrix,SalesByJurisdiction,DaysPerformance,RateCategories,RateItems,RateStores,min_max_dates,OER,OERScores
from ops.orders.orders import Orderitems,PayOrder
from ops.helpers.functions import CurrencyHelper
from ops.inventory.inventory import AllItemsForOrg,AllItemsByCategory,AllItemsByStore
from ops.stores.stores import MStoreent
from ops.catalog.catalog import AddItemToContract
from ops.accounting.accounting import Faccount
from ops.trading.trading import Trading
from ops.trading.trading import Creditline
from ops.payment.payment import PaymentPolicy

# p=PaymentPolicy(1,'Payment')
# print(p.read())

class CustomerMarkupMod:
    def __init__(self,catalog_id,markup,customer_id,store_id):
        self.catalog_id=catalog_id
        self.markup=markup
        self.customer_id=customer_id
        self.contract_id=self.getcontract()
        self.name="Offer Price"
        self.description="Sales price for all items within the Medicines Catalog"
        self.type="S"
        self.store_id=store_id
        self.published=1
        self.lastupdate=datetimestamp_now()
        self.language_id=1
        self.changeable=1
        self.tcsubtype_id="CatalogWithAdjustment"
        self.items=self.applymarkup(self.getitems())

    def _execute(self):
        d={"trading_id":self.contract_id,"items":self.items,"name":self.name,"member_id":self.customer_id,
        "description":self.description,"type":self.type,"catalog_id":self.catalog_id,"store_id":self.store_id,
        "published":self.published,"lastupdate":self.lastupdate,
        "language_id":self.language_id,"changeable":self.changeable,"tcsubtype_id":self.tcsubtype_id}
        m=MakeRequests("/api/v1.0/term_catalog_with_adjustment",payload=d,rtype="POST")._execute()
        print(m)

    def applymarkup(self,items):
        [x.update(dict(offerprice=(self.markup/100)*x['price']+x['price'])) for x in items]
        return items
    
    def getitems(self):
        cursor.execute("""select catentry.catentry_id,listprice.currency::text,listprice.listprice::float
        from catentry inner join listprice on catentry.catentry_id=listprice.catentry_id where 
        catentry.member_id=%s""",(self.customer_id,));res=cursor.fetchall()
        if len(res)<=0:return None
        elif len(res)>0:return [dict(catentry_id=x[0],currency=x[1],price=x[2]) for x in res]
    
    def getcontract(self):
        cursor.execute("""select contract.contract_id from contract inner join orgentity 
        on orgentity.orgentity_id=contract.member_id where contract.usage=0 and contract.
        member_id=%s""",(self.customer_id,));res=cursor.fetchone()
        if res==None:return None
        elif res!=None:return res[0]

# CustomerMarkupMod(3,30,4,2)._execute()
# time.sleep(2)
# CustomerMarkupMod(4,40,4,2)._execute()
# time.sleep(2)
# CustomerMarkupMod(6,30,5,3)._execute()
# time.sleep(2)
# CustomerMarkupMod(5,30,5,3)._execute()
# time.sleep(2)
# CustomerMarkupMod(8,30,6,4)._execute()
# time.sleep(2)
# CustomerMarkupMod(7,30,6,4)._execute()
# time.sleep(2)
# CustomerMarkupMod(10,30,7,5)._execute()
# time.sleep(2)
# CustomerMarkupMod(9,30,7,5)._execute()

def install_items(filename,member_id):
    # drugspricelist.csv
    # instrumentspricelist.csv
    v=InstallCatentries(filename,member_id,)
    v.save()

# member_id=1
# install_items("instrumentspricelist.csv",member_id)
# time.sleep(5)
# install_items("drugspricelist.csv",member_id)

class CashCustomer:
    def __init__(self):
        self.type="U";self.state=1

    def savemember(self):
        cursor.execute("insert into member(type,state)values(%s,%s)returning member_id",
        (self.type,self.state,));con.commit();return cursor.fetchone()[0]

    def saveusers(self,users_id):
        cursor.execute("""insert into users(users_id,registertype,profiletype,language_id,field1,
        setccurr,field3,registration)values(%s,%s,%s,%s,%s,%s,%s,%s)""",(users_id,"R","C",1,"Cash",
        "NGN","Customer",datetimestamp_now(),));con.commit()

    def saveuserreg(self,users_id):
        cursor.execute("insert into userreg(users_id,logonid)values(%s,%s)",
        (users_id,"Cash Customer",));con.commit()

# c=CashCustomer()
# users_id=c.savemember()
# c.saveusers(users_id)
# c.saveuserreg(users_id)

class CreditCash:
    def __init__(self,owner_id,amount,memo):
        self.owner_id=owner_id
        self.amount=amount
        self.memo=memo
    
    def execute(self):
        payload={"owner_id":self.owner_id,"amount":self.amount,"memo":self.memo}
        m=MakeRequests("/api/v1.0/credit_cash",payload,"POST")._execute()
        print(m)

# c=CreditCash(7,1500000,"Opening Balance of Cash Account")
# c.execute()

class PurchaseOrders:
    def __init__(self,creator_id,store_id,vendor_id):
        self.store_id=store_id
        self.vendor_id=vendor_id
        self.creator_id=creator_id
        self.items=getcatentries(creator_id)
        self.raids=raids(store_id)
        self.drugsvendors=[2,3]
        self.instrumentsvendors=[2,3]

    def create_customer_po(self):
        openindicator="N";externalid=None
        payload={"member_id":self.creator_id,"store_id":self.store_id,"vendor_id":self.vendor_id,
                "openindicator":openindicator,"externalid":externalid}
        m=MakeRequests("/api/v1.0/create_ra",payload,"POST")._execute()
        print(m["msg"]);print("\n\n");time.sleep(2)

    def create_pronov_po(self):
        openindicator="Y";externalid=None
        payload={"member_id":self.creator_id,"store_id":self.store_id,"vendor_id":self.vendor_id,
        "openindicator":openindicator,"externalid":externalid}
        m=MakeRequests("/api/v1.0/create_ra",payload,"POST")._execute()
        print(m);print("\n\n");time.sleep(2)

    def transposeitem(self,catentry_id,newowner_id):
        cursor.execute("""with itemname as (select catentdesc.name from catentdesc where
        catentdesc.catentry_id=%s)select itemname.name,catentdesc.catentry_id from itemname inner 
        join catentdesc on itemname.name=catentdesc.name inner join catentry on catentdesc.catentry_id=
        catentry.catentry_id where catentry.member_id=%s and catentdesc.name=itemname.name""",
        (catentry_id,newowner_id,));res=cursor.fetchone()
        if res==None:return res
        elif res!=None:return res[1]

    def populate_customer_po(self):
        def vendorstore(vendor_id):
            cursor.execute("select storeent_id from storeent where member_id=%s",(vendor_id,))
            return cursor.fetchone()[0]
        supplyingstore_id=vendorstore(self.vendor_id);itemsoninv=itemsoninventory(supplyingstore_id)
        catentry_id=choice(itemsoninv);shuffle(itemsoninv);ra_id=choice(self.raids)
        qtyavailable=Inventory.getitemquantity(catentry_id,supplyingstore_id)
        transposed_catentry_id=self.transposeitem(catentry_id,self.creator_id)
        if qtyavailable !=None and qtyavailable > 0 and transposed_catentry_id!=None:
            if qtyavailable==1:qtyord=1;qtyrec=qtyord;qrem=qtyord-qtyrec
            else:qtyord=choice(range(1,12));qtyrec=qtyord;qrem=qtyord-qtyrec
            openindicator="Y";externalid=None;base=datetime.datetime.today()
            datelist=[base-datetime.timedelta(days=x,minutes=randrange(1440)) for x in range(730)]
            datelist=[x.strftime("%Y-%m-%d %H:%M:%S") for x in datelist];orderitems=list()
            name=getname(catentry_id) #;catalog=getcatalog(catentry_id,self.vendor_id)

            print(catentry_id,transposed_catentry_id,qtyord,qtyrec,name,qrem)

            invitem=InventoryItem(catentry_id,1,supplyingstore_id,self.creator_id,self.vendor_id,)
            price=invitem.price["price"];discount=invitem.totaladjustment;price=price-discount;costprice=invitem.costprice

            popayload={"catentry_id":transposed_catentry_id,"cost":price,"expecteddate":todayplusdelta(choice(range(0,5))),
            "ffmcenter_id":getffm(self.creator_id),"itemspc_id":getitemspc(transposed_catentry_id),"lastupdate":datetimestamp_now(),
            "qtyordered":qtyord,"qtyreceived":qtyrec,"qtyremaining":qrem,"ra_id":ra_id,"radetailcomment":
            "Ordered {} quantities of {} and received {}".format(qtyord,name,qtyrec),"setccurr":"NGN","store_id":self.store_id,
            "vendor_id":self.vendor_id,"qtyallocated":0,"member_id":self.creator_id}

            orderitems.append(dict(catentry_id=catentry_id,timeplaced=choice(datelist),
                            language_id=1,store_id=supplyingstore_id,customer_id=self.creator_id,buschn_id=7,
                            owner_id=self.vendor_id,quantity=qtyord,costprice=costprice ))
            pload=dict(orderitems=orderitems)
            m1=MakeRequests("/api/v1.0/create_order",pload,"POST")._execute()
            print(m1["msg"]);time.sleep(2)
            m2=MakeRequests("/api/v1.0/create_radetail",popayload,"POST")._execute()
            print(m1["msg"],"\n",m2["msg"],"\n\n");time.sleep(2)

    def populate_pronov_po(self):
        catentry_id=choice(self.items)
        shuffle(self.items)
        qord=choice(range(1,100))
        qrec=choice(range(0,qord))
        name=getname(catentry_id)
        qrem=qord-qrec;ra_id=choice(self.raids)
        catalog=getcatalog(catentry_id,self.creator_id)
        price=getprice(catentry_id)
        if catalog=="Medicines Catalog":vendor_id=choice(self.drugsvendors)
        elif catalog=="Medical Equipment":vendor_id=choice(self.instrumentsvendors)

        print(catentry_id,qord,qrec,name,qrem,price,catalog,)

        payload={"catentry_id":catentry_id,"cost":price,"expecteddate":todayplusdelta(choice(range(0,15))),
        "ffmcenter_id":getffm(self.creator_id),"itemspc_id":getitemspc(catentry_id),
        "lastupdate":datetimestamp_now(),"qtyordered":qord,"qtyreceived":qrec,
        "qtyremaining":qrem,"ra_id":ra_id,"radetailcomment":"Ordered {} quantities of {} and received {}".
        format(qord,name,qrec),"setccurr":"NGN","store_id":self.store_id,
        "vendor_id":vendor_id,"qtyallocated":0,"member_id":self.creator_id}
        m=MakeRequests("/api/v1.0/create_radetail",payload,"POST")._execute()
        print(m["msg"]);print("\n\n");time.sleep(2)

# for i in range(280):
#     try:
#         (4,2,1),(5,3,1),(6,4,1),(7,5,1)
#         p=PurchaseOrders(4,2,1)
#         # p.create_pronov_po()
#         # p.populate_pronov_po()
#         # p.create_customer_po()
#         p.populate_customer_po()
#     except Exception as e:
#         print(str(e),"\n")
#         continue

class CustomerSales:
    def __init__(self,customer_id,store_id,):
        self.customer_id=customer_id
        self.store_id=store_id
        self.owner_id=self.storeorg()
        self.orderitems=list()

    def storeorg(self):
        cursor.execute("select member_id from storeent where storeent_id=%s",(self.store_id,))
        return cursor.fetchone()[0]

# orderitems.append(dict(catentry_id=catentry_id,timeplaced=choice(datelist),
#                             language_id=1,store_id=supplyingstore_id,customer_id=self.creator_id,buschn_id=7,
#                             owner_id=self.vendor_id,quantity=qtyord,costprice=costprice ))
#             pload=dict(orderitems=orderitems)

    def populate_customer_order(self):
        itemsoninv=itemsoninventory(self.store_id)
        catentry_id=choice(itemsoninv);shuffle(itemsoninv)
        qtyavailable=Inventory.getitemquantity(catentry_id,self.store_id)
        if qtyavailable !=None and qtyavailable > 0:
            if qtyavailable==1:qtyord=1;qtyrec=qtyord;qrem=qtyord-qtyrec
            else:qtyord=choice(range(1,12));qtyrec=qtyord;qrem=qtyord-qtyrec
            name=getname(catentry_id);base=datetime.datetime.today();costprice=getprice(catentry_id)
            datelist=[base-datetime.timedelta(days=x,minutes=randrange(1440)) for x in range(365)]
            datelist=[x.strftime("%Y-%m-%d %H:%M:%S") for x in datelist]

            # invitem=InventoryItem(catentry_id,1,self.store_id,self.customer_id,self.owner_id,)
            # price=invitem.price["price"];discount=invitem.totaladjustment;price=price-discount
            # catentry_id,timeplaced,language_id,store_id,customer_id,buschn_id,owner_id,quantity

            self.orderitems.append(dict(catentry_id=catentry_id,timeplaced=choice(datelist),
                            language_id=1,store_id=self.store_id,customer_id=self.customer_id,
                            buschn_id=choice([2,7]),owner_id=self.owner_id,quantity=qtyord,costprice=costprice ))

    def _execute(self):
        pload=dict(orderitems=self.orderitems)
        m1=MakeRequests("/api/v1.0/create_order",pload,"POST")._execute()
        print(m1);time.sleep(2)

# stores:2,3,4,5
# for i in range(1200):
#     c=CustomerSales(8,choice([2,3,4,5]))
#     for i in range(choice(range(12))):
#         c.populate_customer_order()
#     c._execute()
