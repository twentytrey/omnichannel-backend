import requests
from ops.helpers.functions import BASE_URL

class MakeRequests:
    def __init__(self,endpoint,payload=None,rtype=None):
        self.base_url=BASE_URL
        self.endpoint=endpoint
        self.token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTE4NzE2NzEsIm5iZiI6MTU5MTg3MTY3MSwianRpIjoiZjU4NWJhNjEtOTlhOS00OGRiLThiYmYtNGVlMTQ3MDM0NWY1IiwiZXhwIjoxNTkzNTk5NjcxLCJpZGVudGl0eSI6IisyMzQgODE2IDUwMSA0MTY1IiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIiwidXNlcl9jbGFpbXMiOnsicm9sZXMiOlt7InJvbGVfaWQiOjMsInJvbGVuYW1lIjoicGVybWlzc2lvbl9lZGl0b3IiLCJyb2xlZGlzcGxheW5hbWUiOiJQZXJtaXNzaW9uIEVkaXRvciJ9XSwidXNlcl9pZCI6MSwiZW1wbG95ZXIiOnsiZW1wbG95ZXIiOjEsImVtcGxveWVybmFtZSI6IlByb25vdiBDbyJ9LCJsYW5ndWFnZSI6MSwicHJvZmlsZSI6IkIifX0.DnS0iYydp0HitvN4XeR4ERdEv_BLZ84tlrPC6GOLgA8"
        self.headers={"content-type":"application/json","Accept-Charset":"UTF-8","Authorization":"Bearer {}".format(self.token)}
        self.payload=payload;self.rtype=rtype
    
    def _execute(self):
        if self.rtype=="POST":self.response=requests.post(self.base_url+self.endpoint,data=None,json=self.payload,headers=self.headers)
        elif self.rtype=="GET":self.response=requests.get(self.base_url+self.endpoint,data=None,headers=self.headers)
        return self.response.json()

# PLAN - https://api.paystack.co/plan
# PLAN PAYLOAD - { "name": "Monthly retainer", "interval": "monthly", "amount": "500000" }
class PaystackRequests:
    def __init__(self,endpoint,payload=None,rtype=None):
        self.endpoint=endpoint
        self.token="sk_live_f630153188d3fe949a6fb06771ea395f6667903f"
        self.headers={"content-type":"application/json","Authorization":"Bearer {}".format(self.token)}
        self.payload=payload;self.rtype=rtype
    
    def _execute(self):
        if self.rtype=="POST":self.response=requests.post(self.endpoint,data=None,json=self.payload,headers=self.headers)
        return self.response.json()
