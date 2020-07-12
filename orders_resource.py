from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.orders.orders import Orders,Orderitems,EntryException,BuildMobileRa,BuildMobileRadetail
from ops.orders.orderhandler import OrderItem
from ops.calculations.shippingmethods import ShippingMethods
import json
from ops.accounting.accounting import Transaction,Facctransaction,Faccount
from ops.inventory.inventory import InventoryItem

class create_order(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("orderitems",action="append")
        super(create_order,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        orderitems=data["orderitems"]
        items=[json.loads(x.replace("\'", "\"")) for x in orderitems]
        # catentry_id,language_id,store_id,customer_id,owner_id,quantity
        # catentry_id,timeplaced,language_id,store_id,customer_id,buschn_id,costprice,owner_id,quantity
        orderitemsdata=[OrderItem(item["catentry_id"],item["language_id"],item["store_id"],item["customer_id"],
        item["owner_id"],item["timeplaced"],item["costprice"],item["quantity"],item["buschn_id"]).data for item in items]

        totalproduct=sum([x["totalproduct"] for x in orderitemsdata])
        identity=orderitemsdata[0]["identity"]
        totalshipping=0
        if identity!="Cash Customer":
            totalshipping=ShippingMethods(orderitemsdata[0]["storeent_id"],orderitemsdata[0]["member_id"],totalproduct).lookupvalue

        store_id=orderitemsdata[0]["storeent_id"]
        currency=orderitemsdata[0]["currency"]
        timeplaced=orderitemsdata[0]["lastcreate"]
        orderstatus=orderitemsdata[0]["status"]
        member_id=orderitemsdata[0]["member_id"]
        owner_id=orderitemsdata[0]["owner_id"]
        buschn_id=orderitemsdata[0]["buschn_id"]
        totaladjustment=sum([x["totaladjustment"] for x in orderitemsdata])
        ordersdata=dict(totalproduct=totalproduct,totalshipping=totalshipping,storeent_id=store_id,
        currency=currency,timeplaced=timeplaced,lastupdate=timeplaced,status=orderstatus,
        member_id=member_id,totaladjustment=totaladjustment,type="ORD",buschn_id=buschn_id,editor_id=owner_id)
        try:
            orders=Orders(ordersdata["member_id"],ordersdata["storeent_id"],totaladjustment=ordersdata["totaladjustment"],
                        type=ordersdata["type"],buschn_id=ordersdata["buschn_id"],currency=ordersdata["currency"],
                        timeplaced=ordersdata["timeplaced"],lastupdate=ordersdata["lastupdate"],status=ordersdata["status"],
                        totalproduct=ordersdata["totalproduct"],totalshipping=ordersdata["totalshipping"],
                        editor_id=ordersdata["editor_id"])
            orders_id=orders.save();[x.update(dict(orders_id=orders_id)) for x in orderitemsdata]
            [Orderitems(x["storeent_id"],x["orders_id"],x["member_id"],x["status"],x["quantity"],
            totaladjustment=x["totaladjustment"],inventorystatus=x["inventorystatus"],lastcreate=x["lastcreate"],
            lastupdate=x["lastupdate"],fulfillmentstatus=x["fulfillmentstatus"],offer_id=x["offer_id"],
            currency=x["currency"],totalproduct=x["totalproduct"],address_id=x["address_id"],price=x["price"],
            trading_id=x["trading_id"],itemspc_id=x["itemspc_id"],catentry_id=x["catentry_id"],partnum=x["partnum"],
            ffmcenter_id=x["ffmcenter_id"]).save() for x in orderitemsdata]

            # NOTE: ACCOUNTING
            transactionids=[Transaction("RCPT",owner_id,x["totalproduct"]-x["totaladjustment"],member_id,x["lastcreate"],None,
            "Ordered {},{} units".format(InventoryItem.productname(x["catentry_id"]),x["quantity"])).save() for x in orderitemsdata]
            cogstransactionids=[Transaction("RCPT",owner_id,x["costprice"],owner_id,x["lastcreate"],None,
            "Cost of Goods: {}".format(InventoryItem.productname(x["catentry_id"]))).save() for x in orderitemsdata]
            [Facctransaction(i,Faccount.getid("Inventory",owner_id),"C").save() for i in cogstransactionids]
            [Facctransaction(i,Faccount.getid("Cost of Goods Sold",owner_id),"D").save() for i in cogstransactionids ]
            [Facctransaction(i,Faccount.getid("Sales",owner_id),"C").save() for i in transactionids ]
            [Facctransaction(i,Faccount.getid("Cash",owner_id),"D").save() for i in transactionids ]
            
            return {"status":"OK","msg":"Successfully saved order","orders_id":orders_id},200
        except EntryException as e:
            return {"status":"ERR","msg":"Error {}".format(e.message)},422

class read_orders(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        super(read_orders,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        member_id=data["member_id"]
        return Orders.read(member_id,language_id),200

class read_orderitems(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("orders_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(read_orderitems,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        orders_id=data["orders_id"]
        language_id=data["language_id"]
        return Orderitems.read(language_id,orders_id),200

from ops.orders.orders import PayOrder
class pay_order(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("orders_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("customer_id",help="required field",required=True)
        super(pay_order,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        orders_id=data["orders_id"]
        language_id=data["language_id"]
        customer_id=data["customer_id"]
        return PayOrder(orders_id,customer_id,language_id).readorder(),200

