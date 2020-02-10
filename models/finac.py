from db_con import createcon
con,cursor=createcon("jno","tiniraph","localhost","5432")
con.autocommit=True
from functions import build_constraint
import psycopg2

class Accounting:
    """a simple accounting system listing the chart of accounts for chart of accounts 
    listing all of the accounts in the general ledger. each account is accompanied by a
    reference number."""
    def account_group(self):
        cursor.execute("""create table account_group(
            account_group_id bigserial not null,
            first_ref bigint not null,
            last_ref bigint not null,
            timecreated timestamp,
            timeupdated timestamp,
            member_id bigint not null,
            identifier varchar(254),
            primary key(account_group_id)
        )""")
        cursor.execute("create unique index ac_01 on account_group(identifier,member_id)")
        cursor.execute("create index ac_02 on account_group(member_id)")
        # CONSTRAINTS
    
    def account_group_dsc(self):
        "language-specific description of an account group"
        cursor.execute("""create table account_group_dsc(
            language_id integer not null,
            account_group_id bigint not null,
            name varchar(254),
            description varchar(2000),
            primary key(account_group_id,language_id)
        )""")
    
    def account_group_rel(self):
        cursor.execute("""create table account_group_rel(
            account_group_id bigint not null,
            account_id bigint not null,
            lastupdate timestamp,
            field1 varchar(254),
            field2 integer,
            primary key(account_group_id,account_id)
        )""")
        # CONSTRAINTS

    def account_rel(self):
        cursor.execute("""create table account_rel(
            ancestor_id bigint not null,
            descendant_id bigint not null,
            primary key(ancestor_id,descendant_id)
        )""")
        # CONSTRAINTS
    
    def acct(self):
        cursor.execute("""create table acct(
            acct_id bigint not null,
            identifier varchar(254)not null,
            member_id bigint not null,
            acnumber varchar(254),
            routingnumber varchar(254),
            setccurr char(3)not null,
            primary key(acct_id)
        )""")
        cursor.execute("create unique index ac_03 on acct(acct_id,identifier,member_id)")
        cursor.execute("create index ac_015 on acct(acnumber)")
        cursor.execute("create index ac_016 on acct(routingnumber)")
        cursor.execute("create index ac_017 on acct(setccurr)")
        # CONSTRAINTS

    def acctdesc(self):
        cursor.execute("""create table acctdesc(
            language_id integer not null,
            acct_id bigint not null,
            name varchar(254),
            lastupdate timestamp not null,
            description varchar(2000),
            primary key(language_id,acct_id)
        )""")
        # CONSTRAINTS

    def transtype(self):
        cursor.execute("""create table transtype(
            transtypecode varchar(64),
            transtype_description varchar(254),
            primary key(transtypecode)
        )""")
        cursor.execute("create index a_09 on transtype(transtypecode)")
    
    def transaction(self):
        cursor.execute("""create table transaction(
            transaction_id bigserial not null,
            transtypecode varchar(64)not null,
            timecreated timestamp not null,
            timeupdated timestamp not null,
            amount decimal(20,5) not null,
            description varchar(2000),
            member_id bigint not null,
            cord integer not null,
            primary key(transaction_id)
        )""")
        cursor.execute("create index a_010 on transaction(transtypecode)")
        cursor.execute("create index a_011 on transaction(amount)")
        cursor.execute("create index a_012 on transaction(description)")
        cursor.execute("create index a_018 on transaction(cord)")
        # CONSTRAINTS
    
    def accounts_in_transaction(self):
        cursor.execute("""create table accounts_in_transaction(
            transaction_id bigint not null,
            acct_id bigint not null,
            primary key(transaction_id,acct_id)
        )""")
        # CONSTRAINTS

    def general_journal(self):
        cursor.execute("""create table general_journal(
            entry_id bigserial not null,
            transaction_id bigint not null,
            primary key(entry_id)
        )""")
        cursor.execute("create index a_014 on general_journal(transaction_id)")
        # CONSTRAINTS

class TransactionType:
    def __init__(self,code,name,description):
        self.code=code
        self.name=name
        self.description=description
        self.transtypecode=self.save_transtype()
    
    def save_transtype(self):
        try:
            cursor.execute("""insert into transtype(transtypecode,transtype_description)values(%s,%s)
            on conflict(transtypecode)do update set transtypecode=%s,transtype_description=%s 
            returning transtypecode""",(self.code,self.name,self.code,self.name,))
            con.commit();return cursor.fetchone()
        except (Exception, psycopg2.DatabaseError) as e:
            if con is not None:con.rollback()

if __name__=="__main__":
    a=Accounting()
    # a.acct()
    # a.acctdesc()
    # a.account_group()
    # a.account_group_dsc()
    # a.account_group_rel()
    # a.general_journal()
    # a.accounts_in_transaction()
    # a.transaction()
    # a.transtype()
    # a.account_rel()
    transaction_types=[
        TransactionType("PMT","Customer Payment","Customer payments"),
        TransactionType("STMTCHG","Statement Charge","Statement charge billed to a customer"),
        TransactionType("CREDMEM","Credit Memo","Credit memo issued by your business"),
        TransactionType("RCPT","Sales Receipt","Generic code for sales receipts"),
        TransactionType("ITMRCPT","Item Receipt","Specified an item receipt from a vendor without invoice"),
        TransactionType("TAXPMT","Sales Tax Payment","Sales Tax Payment"),
        TransactionType("BILL","Vendor Bill","Type represents a bill from a vendor that you're yet to play"),
        TransactionType("BILLPMT","Paid Vendor Bill","Represents a bill from a vendor that you have paid"),
        TransactionType("BILLCRED","Vendor Issued Credit","To show a credit given from a vendor"),
        TransactionType("INV","Invoice","Stands for an invoice that you have issued to a customer or a vendor"),
        TransactionType("PAYCHK","Paycheck","Identifies each paycheck issued to your employees"),
        TransactionType("CCCHRG","Credit Card Charge","Represents a credit card charge"),
        TransactionType("CCCRD","Credit Card Credit","Represents a credit card credit"),
        TransactionType("LIABCHK","Liability Transaction","Shows payroll tax and other liability transactions"),
        TransactionType("CHK","Check","Stands for checks"),
        TransactionType("DEP","Deposit","Represents a deposit you've made to the bank"),
        TransactionType("TRANSFR","Transfer","Represents a transfer you've made between two balance sheet registers"),
        TransactionType("DISC","Discount","Identifies a discount given for early payment either to customers or vendors"),
        TransactionType("GENJNRL","General Journal Entry","Stands for a general journal entry which you use when the other transaction types do not apply")]
