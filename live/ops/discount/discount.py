from .db_con import createcon
# from db_con import createcon
import psycopg2,json,math,os
con,cursor=createcon("retail","pronov","localhost","5432")
import  importlib

class EntryException(Exception):
    def __init__(self,message):
        self.message=message

class Calcodetxex:
    def __init__(self,calcode_id,taxcgry_id):
        self.calcode_id=calcode_id
        self.taxcgry_id=taxcgry_id
    
    def save(self):
        try:
            cursor.execute("""insert into calcodtxex(calcode_id,taxcgry_id)values(%s,%s) on conflict
            (calcode_id,taxcgry_id)do update set calcode_id=%s,taxcgry_id=%s returning calcode_id""",
            (self.calcode_id,self.taxcgry_id,self.calcode_id,self.taxcgry_id,));con.commit()
            return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])

class Calrulemgp:
    def __init__(self,calrule_id,mbrgrp_id):
        self.calrule_id=calrule_id
        self.mbrgrp_id=mbrgrp_id
    
    def save(self):
        try:
            cursor.execute("""insert into calrulemgp(calrule_id,mbrgrp_id)values(%s,%s)
            on conflict(mbrgrp_id,calrule_id)do update set calrule_id=%s,mbrgrp_id=%s
            returning calrule_id""",(self.calrule_id,self.mbrgrp_id,self.calrule_id,
            self.mbrgrp_id,));con.commit();return cursor.fetchone()[0]
        except(Exception,psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()
            raise EntryException(str(e).strip().split('\n')[0])
