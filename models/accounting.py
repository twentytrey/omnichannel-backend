from db_con import createcon
con,cursor=createcon("retail","jmso","localhost","5432")
con.autocommit=True
from functions import build_constraint

class Accounting:
    def acclass(self):
        cursor.execute("""create table if not exists acclass(
            acclass_id bigserial not null,
            name varchar(254)not null,
            rangestart bigint,
            rangeend bigint,
            timecreated timestamp,
            member_id bigint not null,
            primary key(acclass_id)
        )""")
        cursor.execute("create unique index ac_01 on acclass(name,member_id)")
        cursor.execute(build_constraint("acclass","a_001","member_id","member","member_id"))
    
    def acclassdsc(self):
        cursor.execute("""create table if not exists acclassdsc(
            acclass_id bigint not null,
            language_id integer not null,
            description varchar(512),
            primary key(acclass_id,language_id)
        )""")
        cursor.execute(build_constraint("acclassdsc","a_001","acclass_id","acclass","acclass_id"))
        cursor.execute(build_constraint("acclassdsc","a_002","language_id","language","language_id"))
    
    def acclassrel(self):
        cursor.execute("""create table if not exists acclassrel(
            parent_id bigint not null,
            child_id bigint not null,
            primary key(parent_id,child_id)
        )""")
        cursor.execute(build_constraint("acclassrel","a_003","parent_id","acclass","acclass_id"))
        cursor.execute(build_constraint("acclassrel","a_004","child_id","acclass","acclass_id"))
    
    def faccount(self):
        cursor.execute("""create table if not exists faccount(
            faccount_id bigserial not null,
            accountnumber varchar(254) not null,
            identifier varchar(254)not null,
            member_id bigint not null,
            routingnumber varchar(254),
            setccurr char(3),
            primary key(faccount_id)
        )""")
        cursor.execute("create unique index ac_02 on faccount(accountnumber,identifier,member_id)")
        cursor.execute("create index if not exists ac_03 on faccount(routingnumber)")
        cursor.execute("create index if not exists ac_04 on faccount(setccurr)")
        cursor.execute(build_constraint("faccount","a_005","member_id","member","member_id"))
        cursor.execute(build_constraint("faccount","a_006","setccurr","setcurr","setccurr"))
    
    def faccountdsc(self):
        cursor.execute("""create table if not exists faccountdsc(
            faccount_id bigint not null,
            language_id integer not null,
            description varchar(512),
            primary key(faccount_id,language_id)
        )""")
        cursor.execute(build_constraint("faccountdsc","a_007","language_id","language","language_id"))
        cursor.execute(build_constraint("faccountdsc","a_008","faccount_id","faccount","faccount_id"))

    def accountclassrel(self):
        cursor.execute("""create table if not exists accountclassrel(
            acclass_id bigint not null,
            faccount_id bigint not null,
            primary key(acclass_id,faccount_id)
        )""")
        cursor.execute(build_constraint("accountclassrel","a_009","acclass_id","acclass","acclass_id"))
        cursor.execute(build_constraint("accountclassrel","a_010","faccount_id","faccount","faccount_id"))

    def transactiontype(self):
        cursor.execute("""create table if not exists transactiontype(
            code varchar(64),
            description varchar(254),
            primary key(code)
        )""")
        cursor.execute("create index if not exists ac_05 on transactiontype(code)")
    
    def transaction(self):
        cursor.execute("""create table if not exists transaction(
            transaction_id bigserial not null,
            typecode varchar(64) not null,
            timecreated timestamp,
            timeupdated timestamp,
            amount decimal(20,5)not null,
            memo varchar(2000),
            primary key(transaction_id)
        )""")
        cursor.execute("create index if not exists ac_06 on transaction(typecode)")
        cursor.execute("create index if not exists ac_07 on transaction(amount)")
    
    def facctransaction(self):
        cursor.execute("""create table if not exists facctransaction(
            transaction_id bigint not null,
            faccount_id bigint not null,
            crdr char(1) not null,
            primary key(transaction_id,faccount_id)
        )""")
        cursor.execute("create index if not exists ac_08 on facctransaction(crdr)")
        cursor.execute(build_constraint("facctransaction","a_011","transaction_id","transaction","transaction_id"))
        cursor.execute(build_constraint("facctransaction","a_012","faccount_id","faccount","faccount_id"))
    
if __name__=="__main__":
    a=Accounting()
    a.acclass()
    a.acclassdsc()
    a.acclassrel()
    a.faccount()
    a.faccountdsc()
    a.accountclassrel()
    a.transactiontype()
    a.transaction()
    a.facctransaction()
