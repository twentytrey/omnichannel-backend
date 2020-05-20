from flask_restful import Resource,reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt,get_jwt_claims)
from flask_jwt_extended.exceptions import RevokedTokenError
from ops.helpers.functions import timestamp_forever,timestamp_now,defaultlanguage,datetimestamp_now,datetimestamp_forever
from ops.trading.trading import (EntryException,contractorigin,contractstate,contractusage,Tradeposcn,Tdpscncntr,
Termcond,tradingstate,creditallowed,Contract,Trading,Trddesc,Cntrname,Participnt,Account,Storecntr,Storedef,Productset,
Prodsetdsc,Prsetcerel,Psetadjmnt,ExcludedItems,Policytc,ApproveContract,SuspendContract,DeployContract,IncludeItem,
ReadCategoryExclusion)
from ops.catalog.catalog import Catgrptpc,Catalogtpc,Catentry,Catgrpps,ItemDiscount
from ops.pricing.pricing import Storetpc
from ops.offers.offers import Offer,Offerdesc,Offerprice
from ops.inventory.inventory import ItemPriceDefaultContract
import json

class contract_defaults(Resource):
    @jwt_required
    def get(self):
        return dict(contractorigins=contractorigin,contractstates=contractstate,contractusages=contractusage,
        tradingstates=tradingstate,creditallowed=creditallowed,contractcode=Contract.code()),200

class create_default_contract(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("comment",required=True,help="required field")
        self.parser.add_argument("cstate",required=True,help="required field")
        self.parser.add_argument("endtime",required=True,help="required field")
        self.parser.add_argument("language_id",required=True,help="required field")
        self.parser.add_argument("member_id",required=True,help="required field")
        self.parser.add_argument("name",required=True,help="required field")
        self.parser.add_argument("origin",required=True,help="required field")
        self.parser.add_argument("participant_id",required=True,help="required field")
        self.parser.add_argument("starttime",required=True,help="required field")
        self.parser.add_argument("state",required=True,help="required field")
        self.parser.add_argument("store_id",required=True,help="required field")
        self.parser.add_argument("timecreated",required=True,help="required field")
        self.parser.add_argument("timedeployed",required=True,help="required field")
        self.parser.add_argument("trdtype_id",required=True,help="required field")
        self.parser.add_argument("usage",required=True,help="required field")
        self.parser.add_argument("startsnow",required=True,help="required field")
        self.parser.add_argument("neverends",required=True,help="required field")
        super(create_default_contract,self).__init__()

    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        comment=data["comment"]
        cstate=data["cstate"]
        endtime=data["endtime"]
        language_id=data["language_id"]
        member_id=data["member_id"]
        name=data["name"]
        origin=data["origin"]
        participant_id=data["participant_id"]
        starttime=data["starttime"]
        state=data["state"]
        store_id=data["store_id"]
        timecreated=data["timecreated"]
        timedeployed=data["timedeployed"]
        trdtype_id=data["trdtype_id"]
        usage=data["usage"]
        startsnow=data["startsnow"]
        neverends=data["neverends"]
        if starttime==None:starttime=datetimestamp_now()
        if endtime==None:endtime=datetimestamp_forever()
        try:
            trading_id=Trading(trdtype_id,state=state,starttime=starttime,endtime=endtime).save()
            Trddesc(trading_id,language_id,longdescription=comment,timecreated=timestamp_now()).save()
            contract_id=Contract(trading_id,name,member_id,origin=origin,state=cstate,usage=usage,comments=comment,timecreated=starttime,timedeployed=timedeployed).save()
            Cntrname(name,member_id,origin).save()
            Participnt(participant_id,1,contract_id,timecreated=starttime).save()
            contracts=Trading.readcontracts(language_id);contracts.extend(Trading.readaccounts(language_id))
            Storedef(store_id,contract_id).save();Storecntr(contract_id,store_id).save()
            defaultcontracts=Trading.readdefaultcontracts(language_id)
            return {"msg":"Successfully saved contract information","defaultcontracts":defaultcontracts},200
        except EntryException as e:
            return {"msg":"Error saving contract information. Error {0}".format(e.message)},422

class create_contract(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("code",required=True,help="required field")
        self.parser.add_argument("comment",required=True,help="required field")
        self.parser.add_argument("cstate",required=True,help="required field")
        self.parser.add_argument("endtime",required=True,help="required field")
        self.parser.add_argument("language_id",required=True,help="required field")
        self.parser.add_argument("member_id",required=True,help="required field")
        self.parser.add_argument("name",required=True,help="required field")
        self.parser.add_argument("origin",required=True,help="required field")
        self.parser.add_argument("participant_id",required=True,help="required field")
        self.parser.add_argument("starttime",required=True,help="required field")
        self.parser.add_argument("state",required=True,help="required field")
        self.parser.add_argument("store_id",required=True,help="required field")
        self.parser.add_argument("timecreated",required=True,help="required field")
        self.parser.add_argument("timedeployed",required=True,help="required field")
        self.parser.add_argument("trdtype_id",required=True,help="required field")
        self.parser.add_argument("usage",required=True,help="required field")
        self.parser.add_argument("startsnow",required=True,help="required field")
        self.parser.add_argument("neverends",required=True,help="required field")
        super(create_contract,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        code=data["code"]
        comment=data["comment"]
        cstate=data["cstate"]
        endtime=data["endtime"]
        language_id=data["language_id"]
        member_id=data["member_id"]
        name=data["name"]
        origin=data["origin"]
        participant_id=data["participant_id"]
        starttime=data["starttime"]
        state=data["state"]
        store_id=data["store_id"]
        timecreated=data["timecreated"]
        timedeployed=data["timedeployed"]
        trdtype_id=data["trdtype_id"]
        usage=data["usage"]
        startsnow=data["startsnow"]
        neverends=data["neverends"]
        if startsnow=="No" and neverends=="No":
            try:
                trading_id=Trading(trdtype_id,state=state,starttime=starttime,endtime=endtime).save()
                Trddesc(trading_id,language_id,longdescription=comment,timecreated=starttime,description=code).save()
                contract_id=Contract(trading_id,name,member_id,origin=origin,state=cstate,usage=usage,comments=comment,timecreated=starttime,timedeployed=timedeployed).save()
                Cntrname(name,member_id,origin).save()
                Participnt(participant_id,3,contract_id,timecreated=starttime).save()
                contracts=Trading.readcontracts(language_id);contracts.extend(Trading.readaccounts(language_id))
                return {"msg":"Successfully saved contract information","contracts":contracts},200
            except EntryException as e:
                return {"msg":"Error saving contract information. Error {0}".format(e.message)},422
        elif startsnow=="Yes" and neverends=="Yes":
            try:
                trading_id=Trading(trdtype_id,state=state,starttime=timestamp_now(),endtime=timestamp_forever()).save()
                Trddesc(trading_id,language_id,longdescription=comment,timecreated=timestamp_now(),description=code).save()
                contract_id=Contract(trading_id,name,member_id,origin=origin,state=cstate,usage=usage,comments=comment,timecreated=timestamp_now(),timedeployed=timedeployed).save()
                Cntrname(name,member_id,origin).save()
                Participnt(participant_id,3,contract_id,timecreated=timestamp_now()).save()
                contracts=Trading.readcontracts(language_id);contracts.extend(Trading.readaccounts(language_id))
                return {"msg":"Successfully saved contract information","contracts":contracts},200
            except EntryException as e:
                return {"msg":"Error saving contract information. Error {0}".format(e.message)},422

class read_contract(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required field")
        self.parser.add_argument("trading_id",required=True,help="required field")
        super(read_contract,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        trading_id=data["trading_id"]
        return Trading.readcontract(trading_id,language_id),200

class read_trading(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required field")
        self.parser.add_argument("trading_id",required=True,help="required field")
        super(read_trading,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        trading_id=data["trading_id"]
        return Trading.read(trading_id,language_id),200

class read_contracts(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required field")
        super(read_contracts,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        return Trading.readcontracts(language_id),200

class read_accounts(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required field")
        super(read_accounts,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        return Trading.readaccounts(language_id),200

class read_default_contracts(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required field")
        super(read_default_contracts,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data['language_id']
        return Trading.readdefaultcontracts(language_id),200

class read_all_trading(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required field")
        super(read_all_trading,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data['language_id']
        # contracts=Trading.readcontracts(language_id)
        contracts=list()
        contracts.extend(Trading.readaccounts(language_id))
        return contracts,200

class create_accounts(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("acstate",help="required field",required=True)
        self.parser.add_argument("actimeapproved",help="required field",required=True)
        self.parser.add_argument("actimecreated",help="required field",required=True)
        self.parser.add_argument("actimeupdated",help="required field",required=True)
        self.parser.add_argument("comment",help="required field",required=True)
        self.parser.add_argument("currency",help="required field",required=True)
        self.parser.add_argument("endtime",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("name",help="required field",required=True)
        self.parser.add_argument("neverends",help="required field",required=True)
        self.parser.add_argument("participant_id",help="required field",required=True)
        self.parser.add_argument("startsnow",help="required field",required=True)
        self.parser.add_argument("starttime",help="required field",required=True)
        self.parser.add_argument("state",help="required field",required=True)
        self.parser.add_argument("store_id",help="required field",required=True)
        self.parser.add_argument("timecreated",help="required field",required=True)
        self.parser.add_argument("trdtype_id",help="required field",required=True)

        self.parser.add_argument("origin",required=True,help="required field")
        self.parser.add_argument("cstate",required=True,help="required field")
        self.parser.add_argument("usage",required=True,help="required field")
        self.parser.add_argument("timedeployed",required=True,help="required field")

        super(create_accounts,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        origin=data["origin"]
        cstate=data['cstate']
        usage=data['usage']
        timedeployed=data['timedeployed']
        acstate=data['acstate']
        actimeapproved=data['actimeapproved']
        actimecreated=data['actimecreated']
        actimeupdated=data['actimeupdated']
        comment=data['comment']
        currency=data['currency']
        endtime=data['endtime']
        language_id=data['language_id']
        member_id=data['member_id']
        name=data['name']
        neverends=data['neverends']
        participant_id=data['participant_id']
        startsnow=data['startsnow']
        starttime=data['starttime']
        state=data['state']
        store_id=data['store_id']
        timecreated=data['timecreated']
        trdtype_id=data['trdtype_id']
        if starttime==None:starttime=datetimestamp_now()
        if endtime==None:endtime=datetimestamp_forever()

        try:
            trading_id=Trading(trdtype_id,state=state,starttime=starttime,endtime=endtime).save()
            Trddesc(trading_id,language_id,longdescription=comment,timecreated=starttime).save()
            contract_id=Contract(trading_id,name,member_id,origin=origin,state=cstate,usage=usage,comments=comment,timecreated=starttime,timedeployed=timedeployed).save()
            Cntrname(name,member_id,origin).save()
            Account(trading_id,name,member_id,store_id,acstate,currency,timecreated=starttime).save()
            Participnt(participant_id,2,trading_id=trading_id,timecreated=starttime).save()
            contracts=Trading.readaccounts(language_id)
            return {"msg":"Successfully created customer account","contracts":contracts},200
        except EntryException as e:
            return {"msg":"Error saving customer account information. Error {0}".format(e.message)},422

class list_tradepositions(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("trading_id",help="required field",required=True)
        super(list_tradepositions,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=int(data["member_id"])
        trading_id=int(data["trading_id"])
        return Tradeposcn.read(member_id,trading_id),200

class trading_read_catentries(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("tdp1")
        self.parser.add_argument("tdp2")
        self.parser.add_argument("store_id")
        self.parser.add_argument("trading_id")
        super(trading_read_catentries,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        tdp1=data["tdp1"]
        tdp2=data["tdp2"]
        store_id=data["store_id"]
        trading_id=data["trading_id"]
        data=Catentry.read(member_id,language_id)
        # return [Offer.offerforitem(x['catentry_id'],tdp2,'S')for x in data],200
        [x.update(Offer.offerforitem(x['catentry_id'],tdp1,'C')) for x in data]
        [x.update(Offer.offerforitem(x['catentry_id'],tdp2,'S')) for x in data]

        [x.update(ItemDiscount(x['catentry_id'],store_id,trading_id).calcode) for x in data]
        return data,200

class trading_products_for_catalog(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("catalog_id",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("tradeposcn_id")
        super(trading_products_for_catalog,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        member_id=data["member_id"]
        language_id=data["language_id"]
        catalog_id=data['catalog_id']
        tradeposcn_id=data['tradeposcn_id']
        data=Catentry.read(member_id,language_id)
        # return data,200
        filtered=[x for x in data if int(x['catalog_id'])==int(catalog_id)]
        [x.update(Offer.offerforitem(x['catentry_id'],tradeposcn_id,'S')) for x in filtered]
        # offers=[Offer.offerforitem(x['catentry_id'],tradeposcn_id) for x in filtered]
        return filtered,200
        # return offers,200

class term_customized_price_list(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("trading_id",help="required field",required=True)
        self.parser.add_argument("items",action="append")
        self.parser.add_argument("name",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("description",help="required field",required=True)
        self.parser.add_argument("type",help="required field",required=True)
        self.parser.add_argument("store_id",help="required field",required=True)
        self.parser.add_argument("published",help="required field",required=True)
        self.parser.add_argument("lastupdate",help="required field",required=True)
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("changeable",help="required field",required=True)        
        self.parser.add_argument("tcsubtype_id",help="required field",required=True)
        super(term_customized_price_list,self).__init__()

    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        changeable=data['changeable']
        description=data['description']
        items=data['items']
        language_id=data['language_id']
        lastupdate=data['lastupdate']
        member_id=data['member_id']
        name=data['name']
        published=data['published']
        store_id=data['store_id']
        tcsubtype_id=data['tcsubtype_id']
        trading_id=data['trading_id']
        type=data['type']
        items=[json.loads(x.replace("\'", "\"").replace("None", "null")) for x in items]
        try:
            tradeposcn_id=Tradeposcn(member_id,name,description=description,ttype=type).save()
            Storetpc(store_id,tradeposcn_id).save()
            Tdpscncntr(tradeposcn_id,trading_id).save()
            Termcond(tcsubtype_id,trading_id,timecreated=timestamp_now(),stringfield1=name).save()
            offerids=[Offer(tradeposcn_id,x['catentry_id'],published=published,lastupdate=timestamp_now()).save() for x in items]
            [Offerdesc(offerids[i],language_id,description=name).save() for i in range(len(offerids))]
            [Offerprice(offerids[i],items[i]['currency'],items[i]['custom']).save() for i in range(len(offerids))]
            return {"msg":"Successfully saved custom pricing information"},200
        except EntryException as e:
            return {"msg":"{}".format(e.message)},422        

class term_catalog_with_adjustment(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("catalog_id",help="required field",required=True)
        self.parser.add_argument("changeable",help="required field",required=True)
        self.parser.add_argument("description",help="required field",required=True)
        self.parser.add_argument("items",action="append")
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("lastupdate",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("name",help="required field",required=True)
        self.parser.add_argument("published",help="required field",required=True)
        self.parser.add_argument("store_id",help="required field",required=True)
        self.parser.add_argument("tcsubtype_id",help="required field",required=True)
        self.parser.add_argument("trading_id",help="required field",required=True)
        self.parser.add_argument("type",help="required field",required=True)
        super(term_catalog_with_adjustment,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        catalog_id=data['catalog_id']
        changeable=data['changeable']
        description=data['description']
        items=data['items']
        language_id=data['language_id']
        lastupdate=data['lastupdate']
        member_id=data['member_id']
        name=data['name']
        published=data['published']
        store_id=data['store_id']
        tcsubtype_id=data['tcsubtype_id']
        trading_id=data['trading_id']
        type=data['type']
        items=[json.loads(x.replace("\'", "\"").replace("None", "null")) for x in items]
        try:
            tradeposcn_id=Tradeposcn(member_id,name,description=description,ttype=type).save()
            Catalogtpc(catalog_id,tradeposcn_id,store_id).save()
            Storetpc(store_id,tradeposcn_id).save()
            Tdpscncntr(tradeposcn_id,trading_id).save()
            Termcond(tcsubtype_id,trading_id,timecreated=timestamp_now(),stringfield1=name).save()
            offerids=[Offer(tradeposcn_id,x['catentry_id'],published=published,lastupdate=timestamp_now()).save() for x in items]
            [Offerdesc(offerids[i],language_id,description=name).save() for i in range(len(offerids))]
            [Offerprice(offerids[i],items[i]['currency'],items[i]['offerprice']).save() for i in range(len(offerids))]
            return {"msg":"Successfully saved offer pricing information"},200
        except EntryException as e:
            return {"msg":"{}".format(e.message)},422

class excluded_items(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("trading_id",help="required field",required=True)
        self.parser.add_argument("tcsubtype_id",help="required field",required=True)
        super(excluded_items,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        trading_id=data['trading_id']
        tcsubtype_id=data["tcsubtype_id"]
        return {"items":ExcludedItems(trading_id,tcsubtype_id).get_items()},200

class custom_pset_exclusion(Resource):
    def __init__(self,):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("adjustment",help="required field",required=True)
        self.parser.add_argument("changeable",help="required field",required=True)
        self.parser.add_argument("description",help="required field",required=True)
        self.parser.add_argument("items",action="append",required=True,help="required field")
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("mandatory",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("name",help="required field",required=True)
        self.parser.add_argument("precedence",help="required field",required=True)
        self.parser.add_argument("publishtime")
        self.parser.add_argument("tcsubtype_id",help="required field",required=True)
        self.parser.add_argument("timecreated")
        self.parser.add_argument("trading_id",help="required field",required=True)
        self.parser.add_argument("type",help="required field",required=True)
        super(custom_pset_exclusion,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        adjustment=data["adjustment"]
        changeable=data["changeable"]
        description=data["description"]
        items=data["items"]
        language_id=data["language_id"]
        mandatory=data["mandatory"]
        member_id=data["member_id"]
        name=data["name"]
        precedence=data["precedence"]
        publishtime=data["publishtime"]
        tcsubtype_id=data["tcsubtype_id"]
        timecreated=data["timecreated"]
        trading_id=data["trading_id"]
        type=data["type"]
        items=[json.loads(x.replace("\'", "\"").replace("None", "null")) for x in items]
        try:
            productset_id=Productset(member_id,name,publishtime=timestamp_now(),).save()
            Prodsetdsc(productset_id,language_id,description).save()
            termcond_id=Termcond(tcsubtype_id,trading_id,mandatory,changeable,timestamp_now(),stringfield1=name).save()
            Psetadjmnt(termcond_id,productset_id,type).save()
            [Prsetcerel(productset_id,items[i]['catentry_id']).save() for i in range(len(items))]
            return {"msg":"Successfully saved excluded products."},200
        except EntryException as e:
            return {"msg":"Error: {}".format(e.message)}

class catgroup_pset_exclusion(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("adjustment",help="required field",required=True)
        self.parser.add_argument("catalog_id",help="required field",required=True)
        self.parser.add_argument("catgroup_id",help="required field",required=True)
        self.parser.add_argument("changeable",help="required field",required=True)
        self.parser.add_argument("description",help="required field",required=True)
        self.parser.add_argument("items",action="append",required=True,help="required field")
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("mandatory",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("name",help="required field",required=True)
        self.parser.add_argument("precedence",help="required field",required=True)
        self.parser.add_argument("publishtime")
        self.parser.add_argument("tcsubtype_id",help="required field",required=True)
        self.parser.add_argument("timecreated")
        self.parser.add_argument("trading_id",help="required field",required=True)
        self.parser.add_argument("type",help="required field",required=True)
        super(catgroup_pset_exclusion,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        adjustment=data["adjustment"]
        catalog_id=data["catalog_id"]
        catgroup_id=data["catgroup_id"]
        changeable=data["changeable"]
        description=data["description"]
        items=data["items"]
        language_id=data["language_id"]
        mandatory=data["mandatory"]
        member_id=data["member_id"]
        name=data["name"]
        precedence=data["precedence"]
        publishtime=data["publishtime"]
        tcsubtype_id=data["tcsubtype_id"]
        timecreated=data["timecreated"]
        trading_id=data["trading_id"]
        type=data["type"]
        items=[json.loads(x.replace("\'", "\"").replace("None", "null")) for x in items]
        try:
            productset_id=Productset(member_id,name,publishtime=timestamp_now()).save()
            Prodsetdsc(productset_id,language_id,description).save()
            termcond_id=Termcond(tcsubtype_id,trading_id,mandatory,changeable,timestamp_now(),stringfield1=name).save()
            Psetadjmnt(termcond_id,productset_id,type).save()
            [Prsetcerel(productset_id,items[i]['catentry_id']).save() for i in range(len(items))]
            Catgrpps(catalog_id,catgroup_id,productset_id).save()
            return {"msg":"Successfully saved excluded category"},200
        except EntryException as e:
            return {"msg":"Error: {}".format(e.message)},422

class read_category_exclusion(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("trading_id",help="required field",required=True)
        self.parser.add_argument("tcsubtype_id",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        super(read_category_exclusion,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        trading_id=data["trading_id"]
        tcsubtype_id=data["tcsubtype_id"]
        member_id=data["member_id"]
        r=ReadCategoryExclusion(trading_id,tcsubtype_id,member_id)
        if r.termcond_id!=None and r.catgroup_id!=None and r.productset_id!=None:
            try:
                items=r.get_items()
                return {"items":items},200
            except EntryException as e:
                return {"msg":"ERROR {}".format(e.message)},422
        return {"items":list()},200

class create_payment_tc(Resource):
    def __init__(self,):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("changeable",help="required field",required=True)
        self.parser.add_argument("description",help="required field",required=True)
        self.parser.add_argument("items",action="append",required=True,help="required field")
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("mandatory",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("tcsubtype_id",help="required field",required=True)
        self.parser.add_argument("trading_id",help="required field",required=True)
        super(create_payment_tc,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        changeable=data["changeable"]
        description=data["description"]
        items=data["items"]
        language_id=data["language_id"]
        mandatory=data["mandatory"]
        member_id=data["member_id"]
        tcsubtype_id=data["tcsubtype_id"]
        trading_id=data["trading_id"]
        items=[json.loads(x.replace("\'", "\"").replace("None", "null")) for x in items]
        try:
            termcond_id=Termcond(tcsubtype_id,trading_id,mandatory,changeable,datetimestamp_now(),datetimestamp_now()).save()
            [Policytc(termcond_id,items[i]['policy_id']).save() for i in range(len(items))]
            return {"msg":"Successfully saved payment methods"},200
        except EntryException as e:
            return {"msg":"Error saving payment methods. Error {}".format(e.message)},422

class create_shipping_tc(Resource):
    def __init__(self,):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("changeable",help="required field",required=True)
        self.parser.add_argument("description",help="required field",required=True)
        self.parser.add_argument("items",action="append",required=True,help="required field")
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("mandatory",help="required field",required=True)
        self.parser.add_argument("member_id",help="required field",required=True)
        self.parser.add_argument("tcsubtype_id",help="required field",required=True)
        self.parser.add_argument("trading_id",help="required field",required=True)
        super(create_shipping_tc,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        changeable=data["changeable"]
        description=data["description"]
        items=data["items"]
        language_id=data["language_id"]
        mandatory=data["mandatory"]
        member_id=data["member_id"]
        tcsubtype_id=data["tcsubtype_id"]
        trading_id=data["trading_id"]
        items=[json.loads(x.replace("\'", "\"").replace("None", "null")) for x in items]
        try:
            termcond_id=Termcond(tcsubtype_id,trading_id,mandatory,changeable,datetimestamp_now(),datetimestamp_now()).save()
            [Policytc(termcond_id,items[i]['policy_id']).save() for i in range(len(items))]
            return {"msg":"Successfully saved shipping methods"},200
        except EntryException as e:
            return {"msg":"Error saving shipping methods. Error {}".format(e.message)},422

class read_account(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",required=True,help="required field")
        self.parser.add_argument("trading_id",required=True,help="required field")
        super(read_account,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        trading_id=data["trading_id"]
        return Trading.readaccount(trading_id,language_id),200

class item_price_default_trading(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("language_id",help="required field",required=True)
        self.parser.add_argument("name")
        self.parser.add_argument("catentry_id")
        super(item_price_default_trading,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        language_id=data["language_id"]
        name=data["name"]
        catentry_id=data["catentry_id"]
        return ItemPriceDefaultContract(language_id,name,catentry_id).prices,200

class approve_contract(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("trading_id",help="required field",required=True)
        self.parser.add_argument("has_account",help="required field",required=True)
        super(approve_contract,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        trading_id=data["trading_id"]
        has_account=int(data["has_account"])
        try:
            approve=ApproveContract(trading_id,datetimestamp_now())
            approve.approve_contract()
            return {"msg":"Successfully approved contract"},200
        except EntryException as e:
            return {"msg":"ERROR {}".format(e.message)},422

class deploy_contract(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("trading_id",help="required field",required=True)
        self.parser.add_argument("has_account",help="required field",required=True)
        super(deploy_contract,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        trading_id=data["trading_id"]
        has_account=int(data["has_account"])
        if has_account > 0:
            try:
                deploy=DeployContract(trading_id,datetimestamp_now())
                deploy.activate_trading()
                deploy.activate_contract()
                deploy.activate_account()
                return {"msg":"Successfully deployed contract"},200
            except EntryException as e:
                return {"msg":"ERROR {}".format(e.message)},422
        elif has_account <= 0:
            try:
                deploy=DeployContract(trading_id,datetimestamp_now())
                deploy.activate_trading()
                deploy.activate_contract()
                return {"msg":"Successfully deployed contract"},200
            except EntryException as e:
                return {"msg":"ERROR {}".format(e.message)},422

class suspend_contract(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("trading_id",help="required field",required=True)
        self.parser.add_argument("has_account",help="required field",required=True)
        super(suspend_contract,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        trading_id=data["trading_id"]
        has_account=int(data["has_account"])
        if has_account > 0:
            try:
                suspend=SuspendContract(trading_id)
                suspend.suspend_trading()
                suspend.suspend_contract()
                suspend.suspend_account()
                return {"msg":"Contract suspended"},200
            except EntryException as e:
                return {"msg":"ERROR {}".format(e.message)},422
        elif has_account <= 0 :
            try:
                suspend=SuspendContract(trading_id)
                suspend.suspend_trading()
                suspend.suspend_contract()
                return {"msg":"Contract suspended"},200
            except EntryException as e:
                return {"msg":"ERROR {}".format(e.message)},422
        
class include_item(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("trading_id",help="required field",required=True)
        self.parser.add_argument("tcsubtype_id",help="required field",required=True)
        self.parser.add_argument("catentry_id",help="required field",required=True)
        super(include_item,self).__init__()
    
    @jwt_required
    def post(self):
        data=self.parser.parse_args()
        trading_id=data["trading_id"]
        tcsubtype_id=data["tcsubtype_id"]
        catentry_id=data["catentry_id"]
        i=IncludeItem(trading_id,tcsubtype_id,catentry_id)
        if i.termcond_id!=None and i.productset_id !=None and i.psettype in [1,3]:
            try:
                i.include_item()
                return {"msg":"Item successfully included"},200
            except EntryException as e:
                return {"ERROR {}".format(e.message)},422
