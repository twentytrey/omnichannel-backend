from ops.trading.trading import Trading,ExcludedItems,InstallPolicyTypes,Tradeposcn,IncludeItem,ReadCategoryExclusion
from ops.offers.offers import Offer
from ops.vendor.vendor import Vendor
from ops.inventory.inventory import Ra,Radetail,Receipt,ReceiveInventory,ItemPriceDefaultContract
from ops.uom.uom import InstallQtyunits
from ops.fulfillment.fulfillment import Inventory
from ops.helpers.functions import datetimestamp_now
from ops.payment.payment import PaymentPolicy
from ops.payment.payment import ReadPolicyTc
from ops.catalog.catalog import Catentry,ReadItemDiscounts,ItemDiscount
from ops.helpers.functions import CurrencyHelper
from ops.filehandlers.filehandlers import InstallCatalogs,InstallCatgroups,InstallCatentries
from ops.orders.orders import InstallBuschn,Buschn
from ops.orders.orderhandler import CartItem
from ops.calculations.discountcalculations import DiscountCalculations
from ops.members.members import UserProfile,UserSign
from ops.accounting.accounting import InstallAccountClasses,InstallAccounts,transaction_types,Faccount

# print( Faccount.readaccount(1,82,1) )

# print(Offer.offerforitem(700,None,'S'))

# i=InstallAccountClasses('accountclasses.csv',1,82)
# i.save()

# i=InstallAccounts("faccount_templates.csv",82,1)
# i.save()

[t.save() for t in transaction_types]

# i=ItemDiscount(325,28,39)
# print(i.calcode)

# r=ReadCategoryExclusion(39,"ProductSetExclusion",82)
# print(r.get_items())

# i=IncludeItem(39,'CustomizedProductSetExclusion')
# print(i.productset_id,)
# print(i.psettype)

# u=UserSign("+234 816 848 1909")
# print(u.logonid)
# print(u.member_id)
# print(u.roles)
# print(u.employer)
# print(u.language_id)
# print(u.profiletype)

# i=ItemPriceDefaultContract(1,'ABF Cream')
# print(i.catentry_id)
# print(i.listprice)
# print(i.contract_id)
# print(i.prices)

# print(Ra.open_or_closed(10))

# i=InstallCatalogs("catalogtemplates.csv",82)
# i.save()
# i=InstallCatgroups("categorytemplates.csv",82)
# i.save()

# drugspricelist.csv
# instrumentspricelist.csv
# v=InstallCatentries("drugspricelist.csv",82)
# v.save()

# c=CartItem(325,28,86,2,employer=86)
# d=DiscountCalculations(c.trading_item_discount,c.catentry_id,c.price,c.quantity,c.storeent_id,c.default_trading_id)
# d._execute()

# print( c.tdpos )
# print(c.getffmcenter(c.catentry_id))
# print(c.getaddress())
# print(c.qtyallocable())
# print(c.inventorystatus)
# print(c.totalproduct)
# print(c.catgroup_id)
# print(c.trading_item_discount)

