from db_con import createcon
con,cursor=createcon("jno","tiniraph","localhost","5432")
con.autocommit=True
from functions import build_constraint
import psycopg2

class Accounting:
    def superclass(self):
        cursor.execute("""create table superclass(
            superclass_id bigserial not null,
            name varchar(254) not null,
            rangestart bigint not null,
            rangeend bigint not null,
            timecreated timestamp,
            timeupdated timestamp,
            member_id bigint not null,
            primary key(superclass_id)
        )""")
        cursor.execute("create unique index ac_01 on superclass(name,member_id)")
        cursor.execute("create index ac_02 on superclass(member_id)")
    
    def superclassdsc(self):
        cursor.execute("""create table superclassdsc(
            superclass_id bigint not null,
            language_id integer not null,
            description varchar(2000),
            primary key(superclass_id,language_id)
        )""")
    
    def subclass(self):
        cursor.execute("""create table subclass(
            subclass_id bigint not null,
            identifier varchar(254)not null,
            member_id bigint not null,
            acnumber varchar(254),
            routingnumber varchar(254),
            setccurr char(3)not null,
            primary key(subclass_id)
        )""")
        cursor.execute("create unique index ac_03 on subclass(subclass_id,identifier,member_id)")
        cursor.execute("create index ac_015 on subclass(acnumber)")
        cursor.execute("create index ac_016 on subclass(routingnumber)")
        cursor.execute("create index ac_017 on subclass(setccurr)")

    def subclassdsc(self):
        cursor.execute("""create table subclassdsc(
            language_id integer not null,
            subclass_id bigint not null,
            name varchar(254),
            lastupdate timestamp not null,
            description varchar(2000),
            primary key(language_id,subclass_id)
        )""")
        # CONSTRAINTS

    def supersubrel(self):
        cursor.execute("""create table supersubrel(
            superclass_id bigint not null,
            subclass_id bigint not null,
            lastupdate timestamp,
            field1 varchar(254),
            field2 integer,
            primary key(superclass_id,subclass_id)
        )""")

    def subsubrel(self):
        cursor.execute("""create table subsubrel(
            ancestor_id bigint not null,
            descendant_id bigint not null,
            primary key(ancestor_id,descendant_id)
        )""")
    
    def productsubclass(self):
        cursor.execute("""create table productsubclass(
            catentry_id bigint not null,
            assetsubclass bigint not null,
            incomesubclass bigint not null,
            expensesubclass bigint not null,
            primary key(catentry_id,assetsubclass,incomesubclass,expensesubclass)
        )""")
        # CONSTRAINTS

    def transactiontype(self):
        cursor.execute("""create table transactiontype(
            code varchar(64),
            description varchar(254),
            primary key(code)
        )""")
        cursor.execute("create index a_09 on transactiontype(code)")

    def po(self):
        """each row represents a purchase order that a buyer organization has defined
        and uses for trading with the seller organization."""
        cursor.execute("""create table po(
            poid bigserial not null,
            setccurr char(3),
            account_id bigint,
            ponumber varchar(128)not null,
            buyerpotyp_id integer,
            state integer default 0,
            amount decimal(20,5),
            primary key(po_id)
        )""")
        cursor.execute("create index i0000488 on po(account_id)")
        cursor.execute("create index i0000489 on po(buyerpotyp_id)")
        # CONSTRAINTS
        cursor.execute(build_constraint("po","f_135","buyerpotyp_id","buyerpotyp","buyerpotyp_id"))
        cursor.execute(build_constraint("po","f_136","setccurr","setcurr","setccurr"))
        cursor.execute(build_constraint("po","f_137","account_id","account","account_id"))

    def transaction(self):
        cursor.execute("""create table transaction(
            transaction_id bigserial not null,
            typecode varchar(64)not null,
            timecreated timestamp not null,
            timeupdated timestamp,
            openbalance decimal(20,5),
            duedate timestamp,
            status integer not null default 0,
            amount decimal(20,5) not null,
            description varchar(2000),
            primary key(transaction_id)
        )""")
        # cursor.execute("create unique index a_u009 on transaction(typecode,amount,description)")
        cursor.execute("create index a_010 on transaction(typecode)")
        cursor.execute("create index a_011 on transaction(amount)")
        cursor.execute("create index a_012 on transaction(description)")
        # CONSTRAINTS

    def subclasstransaction(self):
        cursor.execute("""create table subclasstransaction(
            transaction_id bigint not null,
            subclass_id bigint not null,
            cord integer not null,
            primary key(transaction_id,subclass_id,cord)
        )""")
        cursor.execute("create index a_018 on subclasstransaction(cord)")
        # CONSTRAINTS
    
    def transactionparties(self):
        cursor.execute("""create table transactionparties(
            transaction_id bigint not null,
            member_id bigint not null,
            primary key(transaction_id,member_id)
        )""")

    def journal(self):
        cursor.execute("""create table journal(
            entry_id bigserial not null,
            transaction_id bigint not null,
            primary key(entry_id,transaction_id)
        )""")
        cursor.execute("create index a_014b on journal(transaction_id)")
        # CONSTRAINTS

if __name__=="__main__":
    a=Accounting()
    # a.journal()
    # a.transactionparties()
    # a.subclasstransaction()
    # a.transaction()
    # a.transactiontype()
    # a.subsubrel()
    # a.productsubclass()
    # a.supersubrel()
    # a.subclassdsc()
    # a.subclass()
    # a.superclassdsc()
    # a.superclass()

