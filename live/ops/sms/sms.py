# from .db_con import createcon
# from db_con import createcon
import psycopg2
# con,cursor=createcon('retail','jmso','localhost','5432')
from ops.connector.connector import evcon
con,cursor=evcon()

import pandas as pd
import numpy as np
import os,re
import json,urllib.request
from ops import CurrencyHelper,humanize_date,timestamp_forever,timestamp_now

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Sms:
    def __init__(self,sms_to,sms_body,sms_from="PronovApp",dnd=2,api_token="O7csPy8LWqUqvg3qBrIuPOS33T4olZt63GilMSQxo5dPnEDQTHQcGcZDMRoh"):
        self.api_token=api_token
        self.sms_from=sms_from
        self.sms_to=sms_to
        self.sms_body=sms_body
        self.dnd=dnd
        self.msg_url="https://www.bulksmsnigeria.com/api/v1/sms/create?api_token={}&from={}&to={}&body={}&dnd={}".format(self.api_token,self.sms_from,self.sms_to,urllib.parse.quote(self.sms_body),self.dnd)
    
    def send(self):
        sms_request=urllib.request.urlopen(self.msg_url)
        raw_data=sms_request.read()
        encoding=sms_request.info().get_content_charset('utf8')
        data=json.loads(raw_data.decode(encoding))
        sms_status=data["data"]["status"]
        sms_message=data["data"]["message"]
        return sms_status,sms_message
