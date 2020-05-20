from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.orders.orders import Orders,Orderitems,EntryException

class initialize_order(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("orgentity_id")
        self.parser.add_argument("totalproduct")
        self.parser.add_argument("totaltax")
        self.parser.add_argument("totalshipping")
        self.parser.add_argument("description")
        self.parser.add_argument("storeent_id",help="required field",required=True)
        self.parser.add_argument("currency")
        self.parser.add_argument("timeplaced")
        self.parser.add_argument("lastupdate")
        self.parser.add_argument("status")
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("address_id")
        self.parser.add_argument("totaladjustment")
        self.parser.add_argument("comments")
        self.parser.add_argument("type")
        self.parser.add_argument("buschn_id")
        self.parser.add_argument("editor_id")
        super(initialize_order,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        orgentity_id=data["orgentity_id"]
        totalproduct=data["totalproduct"]
        totaltax=data["totaltax"]
        totalshipping=data["totalshipping"]
        description=data["description"]
        storeent_id=data["storeent_id"]
        currency=data["currency"]
        timeplaced=data["timeplaced"]
        lastupdate=data["lastupdate"]
        status=data["status"]
        member_id=data["member_id"]
        address_id=data["address_id"]
        totaladjustment=data["totaladjustment"]
        comments=data["comments"]
        otype=data["type"]
        buschn_id=data["buschn_id"]
        editor_id=data["editor_id"]
        try:
            order=Orders(member_id,storeent_id,orgentity_id=orgentity_id,totalproduct=totalproduct,totaltax=totaltax,
            totalshipping=totalshipping,description=description,currency=currency,timeplaced=timeplaced,lastupdate=lastupdate,
            status=status,address_id=address_id,totaladjustment=totaladjustment,comments=comments,type=otype,buschn_id=buschn_id,
            editor_id=editor_id).save()
            return {"status":"OK","msg":"Successfully saved order"},200
        except EntryException as e:
            return {"msg":"Error {}".format(e.message),"status":"ERR"},422
