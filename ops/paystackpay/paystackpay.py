import random
import string
from paystack import util
from paystack.resource import (TransactionResource)
from paystack.client import (HTTPClient,RequestsClient)

class PaystackPlugin:
    def __init__(self,secret,email,amount,plan=None,ref=None,path='transaction'):
        self.secret=secret
        self.ref=ref
        self.email=email
        self.amount=amount
        self.path=path
        self.client=TransactionResource(secret,ref,path,verify_ssl=True)
    
    def initialize(self):
        return self.client.initialize(self.amount,self.email,ref=self.ref)
    
def execute():
    apikey="sk_live_f59a105218f513f8e60869703f091a758c8d56cf"
    email="tinigraph@gmail.com"
    amount=500
    ref=''.join([random.choice(string.ascii_letters+string.digits) for n in range(16)])
    p=PaystackPlugin(apikey,email,amount)
    response=p.initialize()
    print(response)
    # if response["status"]==True:
    #     p.verify(response["data"]["reference"])
    # print(response["status"])

execute()


