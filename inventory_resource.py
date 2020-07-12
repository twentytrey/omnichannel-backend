from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage,datetimestamp_now,datetimestamp_forever
from ops.inventory.inventory import DisplayItems,AllItemsForOrg,AllItemsByCategory,AllItemsByStore

class display_items(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("store_id",help="required field",required=True)
        self.parser.add_argument("customer_id",help="required field",required=True)
        self.parser.add_argument("quantity",help="required field",required=True)
        super(display_items,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=int(data["owner_id"])
        language_id=int(data["language_id"])
        store_id=int(data["store_id"])
        customer_id=int(data["customer_id"])
        quantity=int(data["quantity"])
        try:
            d=DisplayItems(owner_id,language_id,store_id,customer_id,quantity)._execute()
            return {"status":"OK","items":d},200
        except Exception as e:
            return {"status":"ERR","msg":str(e).strip()},422

class items_for_organization(Resource):
    def __init__(self,):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(items_for_organization,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=data["owner_id"]
        language_id=data["language_id"]
        return AllItemsForOrg(owner_id,language_id).get(),200

class items_for_organization_by_category(Resource):
    def __init__(self,):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("catgroup_id",help="required field",required=True)
        super(items_for_organization_by_category,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=int(data["owner_id"])
        language_id=int(data["language_id"])
        catgroup_id=int(data["catgroup_id"])
        return AllItemsByCategory(owner_id,language_id,catgroup_id).get(),200


class items_by_store(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("owner_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("store_id",help="required field",required=True)
        super(items_by_store,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        owner_id=int(data["owner_id"])
        language_id=int(data["language_id"])
        store_id=int(data["store_id"])
        return AllItemsByStore(owner_id,language_id,store_id).get(),200
