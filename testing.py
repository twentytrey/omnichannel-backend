from ops.trading.trading import Trading,ExcludedItems
from ops.offers.offers import Offer
from ops.vendor.vendor import Vendor
from ops.inventory.inventory import Ra,Radetail,Receipt,ReceiveInventory

d=ReceiveInventory(9)
print(d.data)