from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage
from ops.catalog.catalog import (Catalog,Catalogdsc,EntryException,Catgroup,Catgrpdesc,Catentryattr,Storecat,Storecgrp,
Cattogrp,Catentry,Catentdesc,Itemspc,Catgpenrel,Listprice,Catentrel,Attrtype,Attr,Attrdesc,Attrval,Attrvaldesc,
Catencalcd,Catgpcalcd)
import json
from ops.offers.offers import Offer

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
        super(create_catentry,self).__init__()
    
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
            c=Catentry(member_id,catenttype_id,partnumber,name,itemspc_id=itemspc_id,mfpartnumber=mfpartnumber,mfname=mfname,lastupdate=lastupdate,availabilitydate=availabilitydate,endofservicedate=endofservicedate)
            nameexists=c.name_exists(name)
            if nameexists:return {"msg":"A product with that name already exists."},200
            elif nameexists==False:
                oldpart=c.initialpart();c.partnumber=oldpart;catentry_id=c.save();newpart=c.updatepart(catentry_id)
                itemspc_id=Itemspc(member_id,newpart,baseitem_id=catentry_id,lastupdate=timestamp_now()).save()
                c.update_itemspc(itemspc_id,catentry_id)
                Catentdesc(catentry_id,language_id,published,name=name,shortdescription=shortdescription,fullimage=fullimage,availabilitydate=availabilitydate).save()
                catgroup_id=Catgpenrel(catgroup_id,catalog_id,catentry_id).save()
                Listprice(catentry_id,currency,listprice).save()
                return {"msg":"Successfully saved product item information","entries":Catentry.readcatentry(member_id,language_id),
                "catentryitems":Catentry.read(member_id,language_id)},200
        except EntryException as e:
            return {"msg":"Error saving item information. Error {0}".format(e.message)}

class create_parent_composite(Resource):
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
        super(create_parent_composite,self).__init__()
    
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
            return {"msg":"Successfully saved product item information","entries":Catentry.readcontainers(member_id,language_id),
            "catentryitems":Catentry.read(member_id,language_id)},200
        except EntryException as e:
            return {"msg":"Error saving item information. Error {0}".format(e.message)}


class products_for_catalog(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("catalog_id",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(products_for_catalog,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        catalog_id=data['catalog_id']
        data=Catentry.read(member_id,language_id)
        filtered=[x for x in data if int(x['catalog_id'])==int(catalog_id)]
        return filtered,200

class read_catentries(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(read_catentries,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        data=Catentry.read(member_id,language_id)
        return data,200

class list_composite_containers(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        super(list_composite_containers,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        return Catentry.readcontainers(member_id,language_id),200

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

class read_attrtypes(Resource):
    @jwt_required
    def get(self):return Attrtype.read(),200

class create_attribute(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("identifier",help="required field",required=True)
        self.parser.add_argument("attrtype_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("description",help="required field",required=True)
        super(create_attribute,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        identifier=data['identifier']
        attrtype_id=data['attrtype_id']
        language_id=data['language_id']
        description=data['description']
        try:
            attr_id=Attr(identifier,attrtype_id).save()
            Attrdesc(attr_id,language_id,attrtype_id,name=identifier,description=description).save()
            return {"msg":"Successfully saved attribute","attrdata":Attr.read(language_id)},200
        except EntryException as e:return {"msg":"Error saving attribute. Error {0}".format(e.message)},422

class read_attr(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",help="required",required=True)
        super(read_attr,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        return Attr.read(language_id),200

class create_catentryattr(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("attr_id",help="compulsory field",required=True)
        self.parser.add_argument("attrtype_id",help="compulsory field",required=True)
        self.parser.add_argument("catentry_id",help="compulsory field",required=True)
        self.parser.add_argument("value",help="compulsory field",required=True)
        self.parser.add_argument("language_id",help="compulsory field",required=True)
        self.parser.add_argument("usage",help="compulsory field",required=True)
        super(create_catentryattr,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        attr_id=data["attr_id"]
        attrtype_id=data["attrtype_id"]
        catentry_id=data["catentry_id"]
        language_id=data["language_id"]
        value=data["value"]
        usage=data["usage"]
        if attrtype_id=='String':
            try:
                attrval_id=Attrval(attr_id).save()
                Attrvaldesc(attrval_id,language_id,attr_id,value=value,stringvalue=value).save()
                Catentryattr(catentry_id,attr_id,attrval_id,usage).save()
                return {"msg":"Successfully saved product attribute"},200
            except EntryException as e:
                return {"msg":"Error saving product attribute. Error {0}".format(e.message)},422
        elif attrtype_id=='Integer':
            try:
                attrval_id=Attrval(attr_id).save()
                Attrvaldesc(attrval_id,language_id,attr_id,value=value,integervalue=value).save()
                Catentryattr(catentry_id,attr_id,attrval_id,usage).save()
                return {"msg":"Successfully saved product attribute"},200
            except EntryException as e:
                return {"msg":"Error saving product attribute. Error {0}".format(e.message)},422
        elif attrtype_id=='Float':
            try:
                attrval_id=Attrval(attr_id).save()
                Attrvaldesc(attrval_id,language_id,attr_id,value=value,floatvalue=value).save()
                Catentryattr(catentry_id,attr_id,attrval_id,usage).save()
                return {"msg":"Successfully saved product attribute"},200
            except EntryException as e:
                return {"msg":"Error saving product attribute. Error {0}".format(e.message)},422
        elif attrtype_id=='Datetime':
            try:
                attrval_id=Attrval(attr_id).save()
                Attrvaldesc(attrval_id,language_id,attr_id,value=value,datetimevalue=value).save()
                Catentryattr(catentry_id,attr_id,attrval_id,usage).save()
                return {"msg":"Successfully saved product attribute"},200
            except EntryException as e:
                return {"msg":"Error saving product attribute. Error {0}".format(e.message)},422

class create_storecat(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("store_id",help="required field",required=True)
        self.parser.add_argument("catalog_id",help="required field",required=True)
        super(create_storecat,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        store_id=data['store_id']
        catalog_id=data['catalog_id']
        try:
            Storecat(catalog_id,store_id,lastupdate=timestamp_now()).save()
            return {"msg":"Successfully attached catalog to store."},200
        except EntryException as e:
            return {"msg":"Error attaching catalog to store. Error {0}".format(e.message)},422

class create_storecgrp(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("store_id",help="required field",required=True)
        self.parser.add_argument("catgroup_id",help="required field",required=True)
        super(create_storecgrp,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        store_id=data["store_id"]
        catgroup_id=data["catgroup_id"]
        try:
            Storecgrp(store_id,catgroup_id).save()
            return {"msg":"Successfully attached product category"},200
        except EntryException as e:
            return {"msg":"Error attaching product category. Error {0}".format(e.message)},422

class create_catgpcalcd(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("store_id",help="compulsory field",required=True)
        self.parser.add_argument("catgroup_id",help="compulsory field",required=True)
        self.parser.add_argument("trading_id",help="compulsory field",required=True)
        self.parser.add_argument("calcode_id",help="compulsory field",required=True)
        self.parser.add_argument("calflags")
        super(create_catgpcalcd,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        store_id=data["store_id"]
        catgroup_id=data["catgroup_id"]
        trading_id=data["trading_id"]
        calcode_id=data["calcode_id"]
        calflags=data["calflags"]
        try:
            Catgpcalcd(store_id,catgroup_id,trading_id,calcode_id,calflags).save()
            return {"msg":"Successfully attached discount to this category"},200
        except EntryException as e:return {"Error: {}".format(e.message)},422


class remove_catencalcd(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("store_id",help="compulsory field",required=True)
        self.parser.add_argument("trading_id",help="compulsory field",required=True)
        self.parser.add_argument("catentry_id",help="compulsory field",required=True)
        self.parser.add_argument("calcode_id",help="compulsory field",required=True)
        self.parser.add_argument("calflags")
        super(remove_catencalcd,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        store_id=data["store_id"]
        trading_id=data["trading_id"]
        catentry_id=data["catentry_id"]
        calcode_id=data["calcode_id"]
        calflags=data["calflags"]
        if calcode_id==None:return {"msg":"Successfully removed item discount"},200
        elif calcode_id!=None:
            try:
                Catencalcd(store_id,trading_id,catentry_id,calcode_id).remove()
                return {"msg":"Successfully removed item discount"},200
            except EntryException as e:
                return {"msg":"ERROR {}".format(e.message)},422

class create_catencalcd(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("store_id",help="compulsory field",required=True)
        self.parser.add_argument("trading_id",help="compulsory field",required=True)
        self.parser.add_argument("catentry_id",help="compulsory field",required=True)
        self.parser.add_argument("calcode_id",help="compulsory field",required=True)
        self.parser.add_argument("calflags")
        super(create_catencalcd,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        store_id=data["store_id"]
        trading_id=data["trading_id"]
        catentry_id=data["catentry_id"]
        calcode_id=data["calcode_id"]
        calflags=data["calflags"]
        try:
            Catencalcd(store_id,trading_id,catentry_id,calcode_id,calflags).save()
            return {"msg":"Successfully attached discount"},200
        except EntryException as e:return {"Error: {}".format(e.message)},422
