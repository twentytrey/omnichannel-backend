from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from jwt import ExpiredSignatureError
from flask_jwt_extended.exceptions import RevokedTokenError
from flask_cors import CORS
import os,datetime
from logging import Formatter,FileHandler
from werkzeug.utils import secure_filename
import config
from ops.members.members import RevokedToken

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
@app.before_first_request
def initializedefaults():
    ld=LanguageDefault('langdefaults.csv')
    if ld.isfilled:pass
    elif ld.isfilled==False:ld.save()
    cd=CurrencyDefaults('allcurrencycodes.csv')
    if cd.isfilled:pass
    elif cd.isfilled==False:cd.save()
    nd=NumberUsageDefaults('numberusage.csv')
    if nd.isfilled():pass
    elif nd.isfilled()==False:nd.save()
    dpp=DefaultPasswordPolicy('defaultpasswordpolicy.csv')
    if dpp.isfilled():pass
    elif dpp.isfilled()==False:dpp.save()
    dlp=DefaultLockoutPolicy('defaultlockoutpolicy.csv')
    if dlp.isfilled():pass
    elif dlp.isfilled()==False:dlp.save()

jwt=JWTManager(app)

@jwt.token_in_blacklist_loader
def banstatus(decryptedtoken):
    jti=decryptedtoken['jti']
    r=RevokedToken(jti)
    return r.isbanned()

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"status":401,"msg":"access token expired"}),401

@app.route("/")
def hello():
    return "ProNov RESTful API Server"

if __name__=='__main__':
    app.run(threaded=True)
