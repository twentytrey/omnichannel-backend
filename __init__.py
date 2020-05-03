from flask import Flask,jsonify,request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from jwt import ExpiredSignatureError
from flask_jwt_extended.exceptions import RevokedTokenError
from flask_cors import CORS
import os,datetime
from logging import Formatter,FileHandler
from werkzeug.utils import secure_filename
import config
from ops.members.members import RevokedToken,EntryException
from ops.helpers.functions import regularize


class ErrorFriendlyApi(Api):
    def error_router(self,original_handler,e):
        if type(e) is ExpiredSignatureError:return original_handler(e)
        elif type(e) is RevokedTokenError:return original_handler(e)
        else:return super(ErrorFriendlyApi,self).error_router(original_handler,e)

app=Flask(__name__)
CORS(app)
api=ErrorFriendlyApi(app)

basedir = os.path.abspath(os.path.dirname(__file__))
logtarget=os.path.join(basedir,"logs/")
if not os.path.isdir(logtarget):os.mkdir(logtarget)
handler=FileHandler(os.path.join(logtarget,"log.txt"),encoding="utf8")
handler.setFormatter(Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S"))

app.config.from_object(config.Config)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']

from ops.language.language import LanguageDefault
from ops.currency.currency import CurrencyDefaults
from ops.currency.currency import NumberUsageDefaults
from ops.authentication.authentication import DefaultPasswordPolicy
from ops.authentication.authentication import DefaultLockoutPolicy
from ops.authentication.authentication import DefaultAccountPolicy
from ops.members.members import RoleDefaults
from ops.countryandstate.countryandstate import CountryDefaults
from ops.countryandstate.countryandstate import StateprovDefaults
from ops.catalog.catalog import CatenttypeDefaults,AttrtypeDefaults,CatreltypeDefaults
from ops.calculations.calculations import CalusageDefaults
from ops.tax.tax import InstallTaxtype
from ops.accounting.accounting import InstallAccountClasses
from ops.trading.trading import InstallPartroles,InstallAttachusg,InstallTctypes,InstallTradetypes

@app.before_first_request
def initializedefaults():
    ld=LanguageDefault('langdefaults.csv')
    isfilled=ld.isfilled()
    if isfilled:pass
    elif isfilled==False:ld.save()

    cd=CurrencyDefaults('allcurrencycodes.csv')
    isfilled=cd.isfilled()
    if isfilled:pass
    elif isfilled==False:cd.save()

    nd=NumberUsageDefaults('numberusage.csv')
    isfilled=nd.isfilled()
    if isfilled:pass
    elif isfilled==False:nd.save()

    dpp=DefaultPasswordPolicy('defaultpasswordpolicy.csv')
    isfilled=dpp.isfilled()
    if isfilled:pass
    elif isfilled==False:dpp.save()

    dlp=DefaultLockoutPolicy('defaultlockoutpolicy.csv')
    isfilled=dlp.isfilled()
    if isfilled:pass
    elif isfilled==False:dlp.save()

    dap=DefaultAccountPolicy()
    isfilled=dap.isfilled()
    if isfilled:pass
    elif isfilled==False:dap.savedescription()

    rd=RoleDefaults('rolesdescriptions.csv')
    isfilled=rd.isfilled()
    if isfilled:pass
    elif isfilled==False:rd.save()

    cd=CountryDefaults('countrycodes.csv')
    isfilled=cd.isfilled()
    if isfilled:pass
    elif isfilled==False:cd.save()

    sd=StateprovDefaults('ngstatecodes.csv','NG')
    isfilled=sd.isfilled()
    if isfilled:pass
    elif isfilled==False:sd.save()

    c=CatenttypeDefaults()
    isfilled=c.isfilled()
    if isfilled:pass
    elif isfilled==False:c.save()

    a=AttrtypeDefaults()
    isfilled=a.isfilled()
    if isfilled:pass
    elif isfilled==False:a.enter()

    c=CatreltypeDefaults()
    isfilled=c.isfilled()
    if isfilled:pass
    elif isfilled==False:c.enter()

    cd=CalusageDefaults()
    isfilled=cd.isfilled()
    if isfilled:pass
    elif isfilled==False:cd.save()

    i=InstallTaxtype('taxtypes.csv')
    isfilled=i.isfilled()
    if isfilled:pass
    elif isfilled==False:i.save()

    # ## i=InstallAccountClasses('accountclasses.csv',1,1)
    # ## if i.isfilled():pass
    # ## elif i.isfilled()==False:i.save()

    i=InstallPartroles('partroles.csv')
    isfilled=i.isfilled()
    if isfilled:pass
    elif isfilled==False:i.save()

    i=InstallAttachusg('attachusg.csv')
    isfilled=i.isfilled()
    if isfilled:pass
    elif isfilled==False:i.save()

    i=InstallTctypes('tctypes.csv')
    isfilled=i.isfilled()
    if isfilled:pass
    elif isfilled==False:i.save()

    i=InstallTradetypes('tradetypes.csv')
    isfilled=i.isfilled()
    if isfilled:pass
    elif isfilled==False:i.save()

jwt=JWTManager(app)

@jwt.token_in_blacklist_loader
def banstatus(decryptedtoken):
    jti=decryptedtoken['jti']
    r=RevokedToken(jti)
    try:
        return r.isbanned()
    except EntryException as e:
        return jsonify({"status":422,"msg":"Error checking token status"}),422

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"status":401,"msg":"access token expired"}),401

@jwt.user_claims_loader
def add_claims_to_token(user):
    return {'roles':user.roles,'user_id':user.member_id,'employer':user.employer,
    'language':user.language_id,'profile':user.profiletype}

@jwt.user_identity_loader
def user_identity_loader(user):
    return user.logonid

@app.route("/")
def hello():return "ProNov RESTful API Server"

@app.route("/profileuploads",methods=["POST","GET"])
def uploads():
    if request.method=='POST':
        files=request.files["image"]
        if files and allowed_file(files.filename):
            filename = secure_filename( files.filename.split('.')[0]+'.'+files.filename.split('.')[-1] )
            app.logger.info("Filename: "+filename)
            updir=os.path.join(basedir,"static/profileuploads/")
            files.save(os.path.join(updir,filename))
            file_size = os.path.getsize(os.path.join(updir,filename))
            file_url="static/profileuploads/"+filename
            return jsonify(url=regularize(file_url),name=filename,size=file_size)

@app.route("/productuploads",methods=["POST","GET"])
def productuploads():
    if request.method=='POST':
        files=request.files["image"]
        if files and allowed_file(files.filename):
            filename = secure_filename( files.filename.split('.')[0]+'.'+files.filename.split('.')[-1] )
            app.logger.info("Filename: "+filename)
            updir=os.path.join(basedir,"static/productuploads/")
            files.save(os.path.join(updir,filename))
            file_size = os.path.getsize(os.path.join(updir,filename))
            file_url="static/productuploads/"+filename
            return jsonify(url=regularize(file_url),name=filename,size=file_size)


import resource,members_resource,catalog_resource,currency_resource,customer_resource,vendor_resource,store_resource,tax_resource,calculation_resource,shipping_resource,accounting_resource,trading_resource
api.add_resource(resource.default_password_policy,"/api/v1.0/default_password_policy",endpoint="default_password_policy")
api.add_resource(members_resource.create_organization,"/api/v1.0/create_organization",endpoint="create_organization")
api.add_resource(members_resource.login_organization,"/api/v1.0/login_organization",endpoint="login_organization")
api.add_resource(members_resource.UserIdentity,"/api/v1.0/useridentity",endpoint="useridentity")
api.add_resource(resource.list_countries,"/api/v1.0/list_countries",endpoint="list_countries")
api.add_resource(resource.list_states_for_country,"/api/v1.0/list_states_for_country",endpoint="list_states_for_country")
api.add_resource(resource.list_languages,"/api/v1.0/list_languages",endpoint="list_languages")
api.add_resource(resource.list_currencies,"/api/v1.0/list_currencies",endpoint="list_currencies")
api.add_resource(members_resource.read_organization,"/api/v1.0/read_organization",endpoint="read_organization")
api.add_resource(members_resource.update_orgentity,"/api/v1.0/update_orgentity",endpoint="update_orgentity")
api.add_resource(members_resource.update_address,"/api/v1.0/update_address",endpoint="update_address")
api.add_resource(members_resource.update_preferences,"/api/v1.0/update_preferences",endpoint="update_preferences")
api.add_resource(catalog_resource.create_catalog,"/api/v1.0/create_catalog",endpoint="create_catalog")
api.add_resource(catalog_resource.read_catalogs,"/api/v1.0/read_catalogs",endpoint="read_catalogs")
api.add_resource(catalog_resource.create_category,"/api/v1.0/create_category",endpoint="create_category")
api.add_resource(catalog_resource.read_categories,"/api/v1.0/read_categories",endpoint="read_categories")
api.add_resource(currency_resource.list_currs,"/api/v1.0/list_currs",endpoint="list_currs")
api.add_resource(catalog_resource.catgroups_for_catalog,"/api/v1.0/catgroups_for_catalog",endpoint="catgroups_for_catalog")
api.add_resource(catalog_resource.create_catentry,"/api/v1.0/create_catentry",endpoint="create_catentry")
api.add_resource(catalog_resource.list_catentries,"/api/v1.0/list_catentries",endpoint="list_catentries")
api.add_resource(catalog_resource.products_for_catalog,"/api/v1.0/products_for_catalog",endpoint="products_for_catalog")
api.add_resource(catalog_resource.create_composite,"/api/v1.0/create_composite",endpoint="create_composite")
api.add_resource(customer_resource.create_customer_organization,"/api/v1.0/create_customer_organization",endpoint="create_customer_organization")
api.add_resource(customer_resource._create_customer_organization,"/api/v1.0/_create_customer_organization",endpoint="_create_customer_organization")
api.add_resource(vendor_resource.create_vendor_organization,"/api/v1.0/create_vendor_organization",endpoint="create_vendor_organization")
api.add_resource(vendor_resource._create_vendor_organization,"/api/v1.0/_create_vendor_organization",endpoint="_create_vendor_organization")
api.add_resource(members_resource.list_all_members,"/api/v1.0/list_all_members",endpoint="list_all_members")
api.add_resource(members_resource.list_roles,"/api/v1.0/list_roles",endpoint="list_roles")
api.add_resource(members_resource.create_business_user,"/api/v1.0/create_business_user",endpoint="create_business_user")
api.add_resource(members_resource._create_business_user,"/api/v1.0/_create_business_user",endpoint="_create_business_user")
api.add_resource(members_resource.append_roles,"/api/v1.0/append_roles",endpoint="append_roles")
api.add_resource(members_resource.approve_member,"/api/v1.0/approve_member",endpoint="approve_member")
api.add_resource(members_resource.suspend_member,"/api/v1.0/suspend_member",endpoint="suspend_member")
api.add_resource(resource.user_identity,"/api/v1.0/user_identity",endpoint="user_identity")
api.add_resource(store_resource.create_store,"/api/v1.0/create_store",endpoint="create_store")
api.add_resource(store_resource.read_ffmcenter,"/api/v1.0/read_ffmcenter",endpoint="read_ffmcenter")
api.add_resource(store_resource.create_host_warehouse,"/api/v1.0/create_host_warehouse",endpoint="create_host_warehouse")
api.add_resource(tax_resource.read_jurst,"/api/v1.0/read_jurst",endpoint="read_jurst")
api.add_resource(tax_resource.read_jurstgroup,"/api/v1.0/read_jurstgroup",endpoint="read_jurstgroup")
api.add_resource(store_resource.list_stores,"/api/v1.0/list_stores",endpoint="list_stores")
api.add_resource(tax_resource.create_jurstgroup,"/api/v1.0/create_jurstgroup",endpoint="create_jurstgroup")
api.add_resource(tax_resource.create_jurst,"/api/v1.0/create_jurst",endpoint="create_jurst")
api.add_resource(tax_resource.read_taxtype,"/api/v1.0/read_taxtype",endpoint="read_taxtype")
api.add_resource(tax_resource.read_taxcgry,"/api/v1.0/read_taxcgry",endpoint="read_taxcgry")
api.add_resource(tax_resource.create_taxcgry,"/api/v1.0/create_taxcgry",endpoint="create_taxcgry")
api.add_resource(tax_resource.read_calcode,"/api/v1.0/read_calcode",endpoint="read_calcode")
api.add_resource(calculation_resource.read_calcodes,"/api/v1.0/read_calcodes",endpoint="read_calcodes")
api.add_resource(calculation_resource.read_calmethods,"/api/v1.0/read_calmethods",endpoint="read_calmethods")
api.add_resource(tax_resource.create_tax_calcode,"/api/v1.0/create_tax_calcode",endpoint="create_tax_calcode")
api.add_resource(tax_resource.read_taxcalrule,"/api/v1.0/read_taxcalrule",endpoint="read_taxcalrule")
api.add_resource(calculation_resource.methods_from_taxcat,"/api/v1.0/methods_from_taxcat",endpoint="methods_from_taxcat")
api.add_resource(tax_resource.create_taxcalrule,"/api/v1.0/create_taxcalrule",endpoint="create_taxcalrule")
api.add_resource(calculation_resource.read_calscale,"/api/v1.0/read_calscale",endpoint="read_calscale")
api.add_resource(tax_resource.create_taxcalscale,"/api/v1.0/create_taxcalscale",endpoint="create_taxcalscale")
api.add_resource(calculation_resource.read_calrange,"/api/v1.0/read_calrange",endpoint="read_calrange")
api.add_resource(calculation_resource.methods_from_calscale,"/api/v1.0/methods_from_calscale",endpoint="methods_from_calscale")
api.add_resource(tax_resource.create_taxcalrange,"/api/v1.0/create_taxcalrange",endpoint="create_taxcalrange")
api.add_resource(calculation_resource.read_calusage,"/api/v1.0/read_calusage",endpoint="read_calusage")
api.add_resource(shipping_resource.create_shpcalrule,"/api/v1.0/create_shpcalrule",endpoint="create_shpcalrule")
api.add_resource(shipping_resource.read_shpcalrule,"/api/v1.0/read_shpcalrule",endpoint="read_shpcalrule")
api.add_resource(shipping_resource.methods_from_calcode,"/api/v1.0/methods_from_calcode",endpoint="methods_from_calcode")
api.add_resource(accounting_resource.list_accounts,"/api/v1.0/list_accounts",endpoint="list_accounts")
api.add_resource(accounting_resource.list_acclasses,"/api/v1.0/list_acclasses",endpoint="list_acclasses")
api.add_resource(accounting_resource.create_account,"/api/v1.0/create_account",endpoint="create_account")
api.add_resource(trading_resource.contract_defaults,"/api/v1.0/contract_defaults",endpoint="contract_defaults")
api.add_resource(members_resource.list_organizations,"/api/v1.0/list_organizations",endpoint="list_organizations")
api.add_resource(trading_resource.create_contract,"/api/v1.0/create_contract",endpoint="create_contract")
api.add_resource(trading_resource.read_trading,"/api/v1.0/read_trading",endpoint="read_trading")
api.add_resource(catalog_resource.read_attrtypes,"/api/v1.0/read_attrtypes",endpoint="read_attrtypes")
api.add_resource(catalog_resource.create_attribute,"/api/v1.0/create_attribute",endpoint="create_attribute")
api.add_resource(catalog_resource.read_attr,"/api/v1.0/read_attr",endpoint="read_attr")
api.add_resource(catalog_resource.create_catentryattr,"/api/v1.0/create_catentryattr",endpoint="create_catentryattr")
api.add_resource(catalog_resource.list_composite_containers,"/api/v1.0/list_composite_containers",endpoint="list_composite_containers")
api.add_resource(catalog_resource.create_parent_composite,"/api/v1.0/create_parent_composite",endpoint="create_parent_composite")
api.add_resource(catalog_resource.read_catentries,"/api/v1.0/read_catentries",endpoint="read_catentries")
api.add_resource(trading_resource.read_contracts,"/api/v1.0/read_contracts",endpoint="read_contracts")
api.add_resource(customer_resource.list_storeorgs,"/api/v1.0/list_storeorgs",endpoint="list_storeorgs")
api.add_resource(store_resource.read_stores,"/api/v1.0/read_stores",endpoint="read_stores")
api.add_resource(trading_resource.create_accounts,"/api/v1.0/create_accounts",endpoint="create_accounts")
api.add_resource(trading_resource.read_accounts,"/api/v1.0/read_accounts",endpoint="read_accounts")
api.add_resource(trading_resource.read_all_trading,"/api/v1.0/read_all_trading",endpoint="read_all_trading")
api.add_resource(trading_resource.read_contract,"/api/v1.0/read_contract",endpoint="read_contract")
api.add_resource(store_resource.your_stores,"/api/v1.0/your_stores",endpoint="your_stores")
api.add_resource(store_resource.store_utilities,"/api/v1.0/store_utilities",endpoint="store_utilities")
api.add_resource(catalog_resource.create_storecat,"/api/v1.0/create_storecat",endpoint="create_storecat")
api.add_resource(catalog_resource.create_storecgrp,"/api/v1.0/create_storecgrp",endpoint="create_storecgrp")
api.add_resource(calculation_resource.discount_calcode_methods,"/api/v1.0/discount_calcode_methods",endpoint="discount_calcode_methods")
api.add_resource(calculation_resource.discount_calrule_methods,"/api/v1.0/discount_calrule_methods",endpoint="discount_calrule_methods")
api.add_resource(calculation_resource.discount_calscale_methods,"/api/v1.0/discount_calscale_methods",endpoint="discount_calscale_methods")
api.add_resource(calculation_resource.discount_calrange_methods,"/api/v1.0/discount_calrange_methods",endpoint="discount_calrange_methods")
api.add_resource(store_resource.create_discount,"/api/v1.0/create_discount",endpoint="create_discount")
api.add_resource(trading_resource.create_default_contract,"/api/v1.0/create_default_contract",endpoint="create_default_contract")
api.add_resource(trading_resource.read_default_contracts,"/api/v1.0/read_default_contracts",endpoint="read_default_contracts")
api.add_resource(trading_resource.term_catalog_with_adjustment,"/api/v1.0/term_catalog_with_adjustment",endpoint="term_catalog_with_adjustment")
api.add_resource(trading_resource.term_customized_price_list,"/api/v1.0/term_customized_price_list",endpoint="term_customized_price_list")
api.add_resource(trading_resource.trading_read_catentries,"/api/v1.0/trading_read_catentries",endpoint="trading_read_catentries")
api.add_resource(trading_resource.trading_products_for_catalog,"/api/v1.0/trading_products_for_catalog",endpoint="trading_products_for_catalog")
api.add_resource(trading_resource.list_tradepositions,"/api/v1.0/list_tradepositions",endpoint="list_tradepositions")
api.add_resource(calculation_resource.list_calcodes,"/api/v1.0/list_calcodes",endpoint="list_calcodes")
api.add_resource(catalog_resource.create_catgpcalcd,"/api/v1.0/create_catgpcalcd",endpoint="create_catgpcalcd")
api.add_resource(catalog_resource.create_catencalcd,"/api/v1.0/create_catencalcd",endpoint="create_catencalcd")
api.add_resource(trading_resource.custom_pset_exclusion,"/api/v1.0/custom_pset_exclusion",endpoint="custom_pset_exclusion")
api.add_resource(trading_resource.catgroup_pset_exclusion,"/api/v1.0/catgroup_pset_exclusion",endpoint="catgroup_pset_exclusion")
api.add_resource(shipping_resource.create_shipmode,"/api/v1.0/create_shipmode",endpoint="create_shipmode")
api.add_resource(trading_resource.excluded_items,"/api/v1.0/excluded_items",endpoint="excluded_items")
api.add_resource(vendor_resource.list_vendors,"/api/v1.0/list_vendors",endpoint="list_vendors")
api.add_resource(vendor_resource.create_ra,"/api/v1.0/create_ra",endpoint="create_ra")
api.add_resource(vendor_resource.read_ra,"/api/v1.0/read_ra",endpoint="read_ra")
api.add_resource(vendor_resource.get_ra,"/api/v1.0/get_ra",endpoint="get_ra")
api.add_resource(store_resource.get_store_image,"/api/v1.0/get_store_image",endpoint="get_store_image")
api.add_resource(vendor_resource.read_ra_detail,"/api/v1.0/read_ra_detail",endpoint="read_ra_detail")
api.add_resource(vendor_resource.create_radetail,"/api/v1.0/create_radetail",endpoint="create_radetail")
api.add_resource(vendor_resource.read_receipts,"/api/v1.0/read_receipts",endpoint="read_receipts")
api.add_resource(vendor_resource.receive_inventory,"/api/v1.0/receive_inventory",endpoint="receive_inventory")
api.add_resource(vendor_resource.inventory_receipt,"/api/v1.0/inventory_receipt",endpoint="inventory_receipt")






















if __name__=='__main__':
    app.run(threaded=True)
