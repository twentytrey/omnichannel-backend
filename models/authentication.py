from db_con import createcon
con,cursor=createcon("retail","jmso","localhost","5432")
con.autocommit=True
from functions import build_constraint

class Authentication:
    """The authentication data model shows the relationship between database tables
    that contain information about security policies within the system."""
    def roleasnprm(self):
        """Role Assignment Permission table. the table specifies
        the roles that users with a particular assigning role
        are able to assign to other users"""
        cursor.execute("""create table roleasnprm(
        roleasnprm_id serial not null,
        assigning_role_id integer not null,
        orgentity_id bigint not null,
        assignable_role_id integer,
        primary key(roleasnprm_id)
        )""")
        cursor.execute("create unique index i0000967 on roleasnprm(assigning_role_id,orgentity_id,assignable_role_id)")
        cursor.execute("create index i0001284 on roleasnprm(orgentity_id)")
    #  CONSTRAINTS:
    
    def plcylckdsc(self):
        "holds language-dependent information related to an account lockout policy."
        cursor.execute("""create table plcylckdsc(
            plcyacclck_id bigint not null,
            language_id integer not null,
            description varchar(254),
            primary key(plcyacclck_id,language_id)
        )""")
    
    def plcypwddsc(self):
        "holds language-dependent information related to a password policy"
        cursor.execute("""create table plcypwddsc(
            plcypasswd_id bigint not null,
            language_id integer not null,
            description varchar(254),
            primary key(plcypasswd_id,language_id)
        )""")
        # CONSTRAINTS:
    
    def plcypasswd(self):
        "stores password policies"
        cursor.execute("""create table plcypasswd(
            plcypasswd_id bigserial not null,
            minpasswdlength integer default 8,
            minalphabetic integer default 1,
            minnumeric integer default 1,
            maxinstances integer default 1,
            maxconsecutivetype integer default 4,
            maxlifetime integer default 90,
            matchuserid integer default 0,
            reusepassword integer default 0,
            primary key(plcypasswd_id)
        )""")
    
    def plcyaccdsc(self):
        "language-dependent information related to an account policy."
        cursor.execute("""create table plcyaccdsc(
            plcyacct_id integer not null,
            language_id integer not null,
            description varchar(254),
            primary key(plcyacct_id,language_id)
        )""")
        # CONSTRAINTS
    
    def plcyacct(self):
        "stores user account policies that consist of an lockout policy and a password policy"
        cursor.execute("""create table plcyacct(
            plcyacct_id serial not null,
            plcyacclck_id bigint not null,
            plcypasswd_id bigint not null,
            primary key(plcyacct_id)
        )""")
        cursor.execute("create index i0000695 on plcyacct(plcyacclck_id)")
        cursor.execute("create index i0000696 on plcyacct(plcypasswd_id)")
        # CONSTRAINT:
    
    def plcyacclck(self):
        "contains the account lockout policies for users"
        cursor.execute("""create table plcyacclck(
            plcyacclck_id bigserial not null,
            lockoutthreshold integer default 6,
            waittime integer default 10,
            primary key(plcyacclck_id)
        )""")

if __name__=="__main__":
    a=Authentication()
    a.roleasnprm()
    a.plcylckdsc()
    a.plcypwddsc()
    a.plcypasswd()
    a.plcyaccdsc()
    a.plcyacct()
    a.plcyacclck()
