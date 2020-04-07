from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.catalog.catalog import Catalog,Catalogdsc,EntryException,Catgroup,Catgrpdesc,Cattogrp,Catentry,Catentdesc,Itemspc,Catgpenrel,Listprice,Catentrel
import json

class create_catalog(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("identifier",help="required field",required=True)
        self.parser.add_argument("description")
        self.parser.add_argument("language_id",help="required",required=True)
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        identifier=data["identifier"]
        description=data["description"]
        language_id=data["language_id"]
        try:
            catalog_id=Catalog(member_id,identifier,description=description).save()
            Catalogdsc(catalog_id,language_id,identifier,shortdescription=description).save()
            returns=Catalog.readcatalogs(member_id,language_id)
            return {"msg":"Successfully saved new catalog","returns":returns},200
        except EntryException as e:
            return {"msg":"Error saving new catalog. Error {0}".format(e.message)},422

class read_catalogs(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(read_catalogs,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        return Catalog.readcatalogs(member_id,language_id),200

class create_category(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("identifier",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("description")
        self.parser.add_argument("parent_catalog",help="required field",required=True)
        self.parser.add_argument("published",help="required field",required=True)
        super(create_category,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        identifier=data["identifier"]
        language_id=data["language_id"]
        description=data["description"]
        parent_catalog=data["parent_catalog"]
        published=data["published"]
        if published=="Publish":data["published"]=1
        elif published=="Withold":data["published"]=0
        published=data["published"]
        try:
            catgroup_id=Catgroup(member_id,identifier).save()
            Catgrpdesc(language_id,catgroup_id,identifier,published,description).save()
            Cattogrp(parent_catalog,catgroup_id).save()
            returns=Catgroup.readcatgroups(member_id,language_id)
            return {"msg":"Successfully saved category information","returns":returns},200
        except EntryException as e:
            return {"msg":"Error saving category information. Error {0}".format(e.message)},422

class read_categories(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(read_categories,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        return Catgroup.readcatgroups(member_id,language_id),200

class catgroups_for_catalog(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("catalog_id",help="required field",required=True)
        super(catgroups_for_catalog,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        catalog_id=data["catalog_id"]
        return Catalog.catgroupforcatalog(catalog_id),200

class create_catentry(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("itemspc_id")
        self.parser.add_argument("catenttype_id")
        self.parser.add_argument("partnumber")
        self.parser.add_argument("mfpartnumber")
        self.parser.add_argument("mfname")
        self.parser.add_argument("currency")
        self.parser.add_argument("listprice")
        self.parser.add_argument("catalog_id")
        self.parser.add_argument("catgroup_id")
        self.parser.add_argument("lastupdate")
        self.parser.add_argument("endofservicedate")
        self.parser.add_argument("name")
        self.parser.add_argument("shortdescription")
        self.parser.add_argument("fullimage")
        self.parser.add_argument("available")
        self.parser.add_argument("published")
        self.parser.add_argument("availabilitydate")
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        itemspc_id=data["itemspc_id"]
        catenttype_id=data["catenttype_id"]
        partnumber=data["partnumber"]
        mfpartnumber=data["mfpartnumber"]
        mfname=data["mfname"]
        currency=Listprice.propercode(data["currency"])
        listprice=data["listprice"]
        catalog_id=data["catalog_id"]
        catgroup_id=data["catgroup_id"]
        lastupdate=data["lastupdate"]
        endofservicedate=data["endofservicedate"]
        name=data["name"]
        shortdescription=data["shortdescription"]
        fullimage=data["fullimage"]
        available=data["available"]
        published=data["published"]
        availabilitydate=data["availabilitydate"]
        try:
            c=Catentry(member_id,catenttype_id,partnumber,name,itemspc_id=itemspc_id,mfpartnumber=mfpartnumber,
            mfname=mfname,lastupdate=lastupdate,availabilitydate=availabilitydate,endofservicedate=endofservicedate)
            oldpart=c.initialpart();c.partnumber=oldpart;catentry_id=c.save();newpart=c.updatepart(catentry_id)
            itemspc_id=Itemspc(member_id,newpart,lastupdate=timestamp_now()).save()
            c.update_itemspc(itemspc_id,catentry_id)
            catentdesc_id=Catentdesc(catentry_id,language_id,published,name=name,shortdescription=shortdescription,
            fullimage=fullimage,availabilitydate=availabilitydate).save()
            catgroup_id=Catgpenrel(catgroup_id,catalog_id,catentry_id).save()
            catentry_listprice_id=Listprice(catentry_id,currency,listprice).save()
            return {"msg":"Successfully saved product item information","entries":Catentry.readcatentry(member_id,language_id)},200
        except EntryException as e:
            return {"msg":"Error saving item information. Error {0}".format(e.message)}

class list_catentries(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(list_catentries,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        return Catentry.readcatentry(member_id,language_id),200

class create_composite(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("components",action="append")
        super(create_composite,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        components=data["components"]
        rels=[json.loads(x.replace("\'", "\"")) for x in components]
        [Catentrel(Catentrel.propername(rel['container_product']),rel['catreltype_id'],
        Catentrel.propername(rel['content_product']),quantity=rel['quantity']).save() for rel in rels]
        return {"msg":"Successfully saved composite product"},200
