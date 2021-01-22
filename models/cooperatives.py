from db_con import con,cursor
from functions import build_constraint

class Cooperatives:
    def creditstatus(self):
        cursor.execute("""create table creditstatus(
            credit_id bigint not null,
            status char(1) not null default 'N',
            primary key(credit_id,status)
        )""")
        # CONSTRAINTS

    def credit(self):
        """each row of this table represents a credit line the account holder
        (buyer organization) has with the seller organization. this credit line is
        associated with a specific business account"""
        cursor.execute("""create table credit(
            credit_id bigserial not null,
            setccurr char(3),
            member_id bigint not null,
            mbrgrp_id bigint not null,
            timecreated timestamp,
            timeupdated timestamp,
            nextduedate timestamp,
            tenure integer not null,
            rate decimal(20,1) not null,
            creditlimit decimal(20,5),
            decimalfield1 decimal(20,5),
            decimalfield2 decimal(20,5),
            plan_integration bigint,
            plan_code varchar(254),
            plan_id bigint,
            customer_code varchar(254),
            subscription_code varchar(254),
            email_token varchar(254),
            primary key(credit_id)
        )""")
        cursor.execute("create unique index i00jd00549 on credit(member_id)")
        cursor.execute("create index a8dpsvb2 on credit(plan_integration,plan_code,plan_id)")
        cursor.execute("create index a3vwds0w on credit(tenure,rate,decimalfield2)")
        cursor.execute("create index afjwgf92 on credit(customer_code,subscription_code,email_token)")
        # CONSTRAINTS


    def guarantor(self):
        cursor.execute("""create table guarantor(
            guarantor_id bigint not null,
            borrower_id bigint not null,
            credit_id bigint not null,
            status char(1)not null default 'N',
            transaction_id bigint,
            primary key(guarantor_id,borrower_id,credit_id)
        )""")
        # CONSTRAINTS
        cursor.execute(build_constraint("guarantor","f_sif227","transaction_id","transaction","transaction_id"))

if __name__=="__main__":
    c=Cooperatives()
    c.credit()
    c.creditstatus()
    c.guarantor()
