from ops.trading.trading import Trading,ExcludedItems,InstallPolicyTypes,Tradeposcn,IncludeItem,ReadCategoryExclusion
from ops.offers.offers import Offer
from ops.vendor.vendor import Vendor
from ops.inventory.inventory import Ra,Radetail,Receipt,ReceiveInventory,ItemPriceDefaultContract,InventoryItem,InventoryItemIds,DisplayItems
from ops.uom.uom import InstallQtyunits
from ops.fulfillment.fulfillment import Inventory
from ops.helpers.functions import datetimestamp_now,todayplusdelta
from ops.payment.payment import PaymentPolicy
from ops.payment.payment import ReadPolicyTc
from ops.catalog.catalog import Catentry,ReadItemDiscounts,ItemDiscount,CatalogItem
from ops.helpers.functions import CurrencyHelper
from ops.filehandlers.filehandlers import InstallCatalogs,InstallCatgroups,InstallCatentries
from ops.orders.orders import InstallBuschn,Buschn,Orders,Orderitems
from ops.calculations.discountcalculations import DiscountCalculations
from ops.calculations.shippingmethods import ShippingMethods
from ops.members.members import UserProfile,UserSign,OTPLogin
from ops.accounting.accounting import InstallAccountClasses,InstallAccounts,transaction_types,Faccount,Transaction,Facctransaction
from ops.filehandlers.simpos import (normal_choice,items,vendors,raids,getitemspc,getffm,getname,getcatalog,getprice)
from requester import MakeRequests
from random import shuffle
import time
import datetime
from random import randrange
from ops.analytics.analytics import CatalogsPerformance,SalesByJurisdiction,min_max_dates
pronov_id,pronovstore_id=1,1
from ops.catalog.catalog import Catgroup,Catentry
from ops.stores.stores import StoresForMember,VendorsForMember


def customer_orders():
    # base=datetime.datetime.today()
    # datelist=[base-datetime.timedelta(days=x,minutes=randrange(1440)) for x in range(365)]
    # datelist=[x.strftime("%Y-%m-%d %H:%M:%S") for x in datelist];orderitems=list()
    for _ in range(normal_choice(range(20))):
        orderitems.append(dict(catentry_id=normal_choice(items),timeplaced=normal_choice(datelist),
                            language_id=1,store_id=1,customer_id=7,buschn_id=7,
                            owner_id=1,quantity=normal_choice(range(10))))
        shuffle(items)
    pload=dict(orderitems=orderitems)
    m=MakeRequests("/api/v1.0/create_order",pload,"POST")
    res=m._execute()
    print(res,"\n")

# for i in range(12):
#     customer_orders()



