from db_con import con,cursor
from functions import build_constraint

class Members:
    """the members data model shows the relationship between database tables
    that contain information about users,organizational entities,user groups and roles."""
    def revokedtoken(self):
        cursor.execute("""create table token_revoked(token_id serial, jti varchar not null)""")
        cursor.execute("create index idx_revtk on token_revoked(jti)")

    def role(self):
        "this table stores roles defined in te system."
        cursor.execute("""create table role(
            role_id serial not null,
            name varchar(254)not null,
            description varchar(4000),
            primary key(role_id)
        )""")
        cursor.execute("create unique index i0000217 on role(name)")
    
    def roledesc(self):
        "stores translatable descriptions for roles."
        cursor.execute("""create table roledesc(
            role_id integer not null,
            language_id integer not null,
            displayname varchar(254)not null,
            description varchar(4000),
            primary key(role_id,language_id)
        )""")
        # CONSTRAINTS
    
    def mbrrole(self):
        """this table stores role assignment for member. each member can play 
        one or more roles in the system. when a member is assigned a role, the 
        orgentity for which the member plays that role can also be specified."""
        cursor.execute("""create table mbrrole(
            member_id bigserial not null,
            role_id integer not null,
            orgentity_id bigint not null,
            primary key(member_id,role_id,orgentity_id)
        )""")
        cursor.execute("create index i0000275 on mbrrole(member_id,orgentity_id)")
        cursor.execute("create index i0000329 on mbrrole(orgentity_id,role_id)")
        cursor.execute("create index i0000617 on mbrrole(role_id)")
        # CONSTRAINTS:
    
    def mbrgrpdesc(self):
        "contains locale specific information for the entries in the mbrgrp table"
        cursor.execute("""create table mbrgrpdesc(
            mbrgrp_id bigint not null,
            language_id integer not null,
            displayname varchar(254)not null,
            description varchar(4000),
            primary key(mbrgrp_id,language_id)
        )""")
        # CONSTRAINT
    
    def ccomment(self):
        """this table stores customer comments. these are 
        notes about interactions that a customer service representative has with a particular customer.
        or notes tha the customer requests be recorded as part of their profile."""
        cursor.execute("""create table ccomment(
            ccomment_id bigserial not null,
            customerid bigint not null,
            targetid bigint not null,
            authdomain bigint not null,
            createdby bigint not null,
            lastupdatedby bigint not null,
            createtimestamp timestamp not null,
            lastupdatetstmp timestamp not null,
            language_id integer not null,
            field1 varchar(254),
            field2 varchar(254),
            field3 varchar(254),
            commentdetail varchar(4000)not null,
            primary key(ccomment_id)
        )""")
        cursor.execute("create index i0000911 on ccomment(customerid)")
        cursor.execute("create index i0000912 on ccomment(targetid)")
        cursor.execute("create index i0000913 on ccomment(authdomain)")
        cursor.execute("create index i0000914 on ccomment(createdby)")
        cursor.execute("create index i0000915 on ccomment(lastupdatedby)")
        cursor.execute("create index i0000916 on ccomment(language_id)")
        # CONSTRAINTS:
    
    def repcustrel(self):
        """this table defines the relationship between a customer service rep
        or team of representatives and the customer or customer group that they are
        assigned to."""
        cursor.execute("""create table repcustrel(
            rep_id bigint not null,
            cust_id bigint not null,
            sequence float not null default 0,
            primary key(rep_id,cust_id)
        )""")
        cursor.execute("create index i0000965 on repcustrel(cust_id)")
        # CONSTRAINT
    
    def mbrgrpusg(self):
        "allows a member group to be associated with multiple group types (or multiple intended usages)"
        cursor.execute("""create table mbrgrpusg(
            mbrgrptype_id integer not null,
            mbrgrp_id bigint not null,
            field1 varchar(254),
            primary key(mbrgrptype_id,mbrgrp_id)
        )""")
        cursor.execute("create index i0000616 on mbrgrpusg(mbrgrp_id)")
        # CONSTRAINT

    def mbrgrptype(self):
        "stores intended usages that can be associated with member groups."
        cursor.execute("""create table mbrgrptype(
            mbrgrptype_id serial not null,
            description varchar(254),
            name varchar(254)not null,
            properties varchar(254),
            primary key(mbrgrptype_id)
        )""")
        cursor.execute("create unique index i0000153 on mbrgrptype(name)")
    
    def mbrgrp(self):
        """stores member groups defined in the system.
        a member group is a group of members. membership is restricted
        to users within the member group."""
        cursor.execute("""create table mbrgrp(
            mbrgrp_id bigint not null,
            owner_id bigint not null,
            field1 varchar(254),
            description varchar(512),
            field2 varchar(254),
            dn varchar(1000),
            mbrgrpname varchar(254)not null,
            field3 varchar(254),
            oid varchar(64),
            lastupdate timestamp,
            lastupdatedby varchar(254),
            primary key(mbrgrp_id)
        )""")
        cursor.execute("create unique index i0000152 on mbrgrp(owner_id,mbrgrpname)")
        # CONSTRAINT
    
    def mgpcondele(self):
        "stores member group condition elements"
        cursor.execute("""create table mgpcondele(
            mgpcondele_id bigserial not null,
            mbrgrp_id bigint not null,
            name varchar(254)not null,
            type varchar(254)not null,
            parent varchar(254),
            sequence float,
            variable varchar(254),
            operator varchar(64),
            value varchar(254),
            condname varchar(254),
            negate smallint not null default 0,
            primary key(mgpcondele_id)
        )""")
        cursor.execute("create unique index i0001230 on mgpcondele(name,mbrgrp_id)")
        cursor.execute("create index i0001231 on mgpcondele(mbrgrp_id)")
        # CONSTRAINTS:
    
    def mgpcondelenvp(self):
        "stores member group condition element values"
        cursor.execute("""create table mgpcondelenvp(
            mgpcondelenvp_id bigserial not null,
            mgpcondele_id bigint not null,
            name varchar(254)not null,
            value varchar(254)not null,
            primary key(mgpcondelenvp_id)
        )""")
        cursor.execute("create index i0001232 on mgpcondelenvp(mgpcondele_id)")
        # CONSTRAINTS:
    
    def mbrgrpcond(self):
        "stores the conditions for an implicit member group."
        cursor.execute("""create table mbrgrpcond(
            mbrgrp_id bigint not null,
            conditions text,
            field1 varchar(254),
            field2 varchar(254),
            primary key(mbrgrp_id,field1)
        )""")
        # CONSTRAINT:
    
    def mbrgrpmbr(self):
        """contains members that are explicitly included or excluded from a member group.
        this works in conjunction with the implicit inclusion rules that are specified
        by mbrgrpcond table. if both implicit and explicit rules are specified. then the following
        algorithm is ued to evaluate if a member belongs to a member group. explicit exclusion takes
        first precedence, then explicit inclusion, and then finally implicit exclusion."""
        cursor.execute("""create table mbrgrpmbr(
            member_id bigint not null,
            mbrgrp_id bigint not null,
            field1 varchar(254),
            customerid bigint,
            exclude char(1)not null default '0',
            primary key(member_id,mbrgrp_id)
        )""")
        # CONSTRAINTS:
    
    def mbrrel(self):
        """stores hierarchy relationships (ancestors and descendants) of 
        organizational entities and registered users. note that member groups
        are not part of member hierarchy."""
        cursor.execute("""create table mbrrel(
            descendant_id bigint not null,
            ancestor_id bigint not null,
            sequence integer,
            primary key(descendant_id,ancestor_id)
        )""")
        # CONSTRAINTS:
    
    def addrbook(self):
        """contains information about an address book. an address book is a container for
        addresses owned by a member. a member can only have one address book."""
        cursor.execute("""create table addrbook(
            addrbook_id bigserial not null,
            member_id bigint not null,
            type char(1),
            displayname varchar(254) not null,
            description varchar(254),
            primary key(addrbook_id)
        )""")
        cursor.execute("create unique index i0000013 on addrbook(addrbook_id,member_id)")
        cursor.execute("create index i0000014 on addrbook(member_id)")
        # CONSTRAINTS:
    
    def address(self):
        """this table stores the addresses of users or organizations in the system.
        the addresses can be the members' own addresses or for their friends,
        associates or clients and so on. some columns here replace columns in previous versions."""
        cursor.execute("""create table address(
            address_id bigserial not null,
            addresstype char(5),
            member_id bigint not null,
            addrbook_id bigint not null,
            orgunitname varchar(128),
            field3 varchar(64),
            billingcode char(2),
            billingcodetype char(2),
            status char(1),
            orgname varchar(128),
            isprimary integer,
            lastname varchar(128),
            persontitle varchar(50),
            firstname varchar(128),
            middlename varchar(128),
            businesstitle varchar(128),
            phone1 varchar(32),
            fax1 varchar(32),
            phone2 varchar(32),
            address1 varchar(256),
            fax2 varchar(32),
            nickname varchar(254)not null,
            address2 varchar(254),
            address3 varchar(254),
            city varchar(128),
            state varchar(128),
            country varchar(128),
            zipcode varchar(40),
            email1 varchar(256),
            email2 varchar(256),
            phone1type char(3),
            phone2type char(3),
            publishphone1 integer,
            publishphone2 integer,
            bestcallingtime char(1),
            packagesuppression integer,
            lastcreate timestamp,
            officeaddress varchar(128),
            selfaddress integer not null default 0,
            field1 varchar(254),
            field2 varchar(254),
            taxgeocode varchar(254),
            shippinggeocode varchar(254),
            mobilephone1 varchar(32),
            mobilephone1cntry varchar(128),
            primary key(address_id)
        )""")
        cursor.execute("create index i0000015 on address(addrbook_id,addresstype,isprimary,status)")
        cursor.execute("create index i0000016 on address(member_id,status,selfaddress,addresstype,isprimary)")
        cursor.execute("create index i0000346 on address(lastname)")
        cursor.execute("create index i0001521 on address(email1)")
        cursor.execute("create unique index idxad1 on address(nickname)")
        # CONSTRAINTS:
    
    def member(self):
        """stores the list of members (participants) of the system.
        a member is eiter a user, organizational entity or a member group."""
        cursor.execute("""create table member(
            member_id bigserial not null,
            type char(3)not null,
            state integer,
            primary key(member_id)
        )""")
        cursor.execute("create index i274130 on member(member_id,type)")
        # CONSTRAINTS:
    
    def attrtype(self):
        "holds the type identifier for product attributes"
        cursor.execute("""create table attrtype(
            attrtype_id char(16)not null,
            description varchar(254),
            oid varchar(64),
            primary key(attrtype_id)
        )""")
    
    def mbrattr(self):
        "contains custom member attributes to be assigned to users and organizations"
        cursor.execute("""create table mbrattr(
            mbrattr_id bigserial not null,
            attrtype_id char(16)not null,
            name varchar(254)not null,
            description varchar(254),
            primary key(mbrattr_id)
        )""")
        cursor.execute("create unique index i0000151 on mbrattr(name)")
        # CONSTRAINTS:
    
    def mbrattrval(self):
        "stores values of attributes which are defined in the mbrattr table for members."
        cursor.execute("""create table mbrattrval(
            mbrattrval_id bigserial not null,
            storeent_id integer,
            member_id bigint not null,
            attrtype_id char(16)not null,
            mbrattr_id bigint not null,
            floatvalue float,
            integervalue integer,
            stringvalue varchar(4000),
            datetimevalue timestamp,
            primary key(mbrattrval_id)
        )""")
        cursor.execute("create index i0000326 on mbrattrval(member_id,mbrattr_id)")
        cursor.execute("create index i0000327 on mbrattrval(storeent_id)")
        cursor.execute("create index i0000614 on mbrattrval(mbrattr_id)")
        # CONSTRAINTS:
    
    def storeent(self):
        """each row of this table represents a store entity.
        a store entity is an abstract superclass that can 
        represent either a store or a store group."""
        cursor.execute("""create table storeent(
            storeent_id serial not null,
            member_id bigint not null,
            type char(1)not null,
            setccurr char(3),
            identifier varchar(254)not null,
            markfordelete integer not null default 0,
            primary key(storeent_id)
        )""")
        cursor.execute("create unique index i0000240 on storeent(identifier,member_id)")
        cursor.execute("create index i0000787 on storeent(member_id)")
        # CONSTRAINTS:
    
    def language(self):
        """each row of this table represents a language. the system supports
        multiple languages. using predefined ISO codes can add other supported languages."""
        cursor.execute("""create table language(
            language_id serial not null,
            localename char(16),
            language varchar(254)not null,
            country varchar(254),
            encoding varchar(32),
            mimecharset varchar(32),
            primary key(language_id)
        )""")

    def setcurr(self):
        """contains information about the different national currencies.
        the currency alphabetic and numeric codes are derived from the ISO 4217 standard."""
        cursor.execute("""create table setcurr(
            setccurr char(3)not null,
            setccode integer not null,
            setcexp integer not null,
            setcnote varchar(40),
            primary key(setccurr)
        )""")
    
    def orgcode(self):
        """contains the unique identification of an organizational entity.
        under identification systems or domains. this can be used to identify buyer
        organizations and supplier organizations to each other in procurement systems."""
        cursor.execute("""create table orgcode(
            orgcode_id bigserial not null,
            orgentity_id bigint not null,
            codetype varchar(254)not null,
            code varchar(128)not null,
            primary key(orgcode_id)
        )""")
        cursor.execute("create unique index i0000181 on orgcode(codetype,code)")
        cursor.execute("create unique index i0000182 on orgcode(orgentity_id,codetype)")
        # CONSTRAINTS:
    
    def orgentity(self):
        """this table contains information on organizational entities.
        an org entity is either an organization, or an organization unit."""
        cursor.execute("""create table orgentity(
            orgentity_id bigserial not null,
            legalid varchar(128),
            orgentitytype char(3)not null,
            orgentityname varchar(128)not null,
            businesscategory varchar(128),
            description varchar(512),
            adminfirstname varchar(128),
            adminlastname varchar(128),
            adminmiddlename varchar(128),
            preferreddelivery varchar(1000),
            field1 varchar(64),
            field2 varchar(64),
            dn varchar(1000),
            taxpayerid varchar(254),
            field3 varchar(64),
            status integer not null default 0,
            primary key(orgentity_id)
        )""")
        cursor.execute("create index i0000970 on orgentity(dn)")
        # CONSTRAINTS
    
    def users(self):
        """contains users of the system. registered users,
        guest users and generic users."""
        cursor.execute("""create table users(
            users_id bigint not null,
            dn varchar(1000),
            registertype char(4)not null,
            profiletype char(2),
            language_id integer,
            field1 varchar(254),
            setccurr char(3),
            field3 varchar(254),
            field2 varchar(254),
            lastorder timestamp,
            registration timestamp,
            lastsession timestamp,
            registrationupdate timestamp,
            registrationcancel timestamp,
            prevlastsession timestamp,
            personalizationid varchar(30),
            primary key(users_id)
        )""")
        cursor.execute("create index i0000969 on users(dn)")
        cursor.execute("create index i0000971 on users(registertype)")
        cursor.execute("create index i0001109 on users(personalizationid)")
        cursor.execute("create index i348118 on users(profiletype,registertype,users_id)")
        # CONSTRAINTS:
    
    def userreg(self):
        "stores user authentication information"
        cursor.execute("""create table userreg(
            users_id bigint not null,
            status integer,
            plcyacct_id integer,
            logonid varchar(254)not null,
            logonpassword text,
            passwordexpired integer,
            challengequestion varchar(254),
            challengeanswer varchar(254),
            timeout bigint not null default 1,
            salt varchar(254),
            passwordcreation timestamp,
            passwordinvalid timestamp,
            primary key(users_id)
        )""")
        cursor.execute("create unique index i0000260 on userreg(logonid)")
        cursor.execute("create index i0000330 on userreg(plcyacct_id)")
        cursor.execute("create index i716117 on userreg(logonid,users_id)")
        # CONSTRAINTS
    
    def userprof(self):
        "contains basic registrered user profile information"
        cursor.execute("""create table userprof(
            users_id bigint not null,
            photo varchar(254),
            description varchar(4000),
            displayname varchar(128),
            preferredcomm char(2),
            preferreddelivery varchar(1000),
            preferredmeasure char(15),
            field1 varchar(254),
            taxpayerid varchar(254),
            field2 varchar(254),
            rcvsmsnotification smallint not null default 0,
            primary key(users_id)
        )""")
        # CONSTRAINTS:
    
    def busprof(self):
        """stores business profile information for a user.
        it is populated by the user registration commands.
        it is intended to be populated for users with profile type 'B'
        signifying that they are a business user."""
        cursor.execute("""create table busprof(
            users_id bigint not null,
            employeeid varchar(50),
            org_id bigint,
            orgunit_id bigint,
            employeetype varchar(128),
            departmentnum varchar(128),
            alternateid varchar(20),
            manager varchar(254),
            secretary varchar(254),
            requisitionerid varchar(128),
            primary key(users_id)
        )""")
        cursor.execute("create index i0000324 on busprof(requisitionerid)")
        cursor.execute("create index i0000486 on busprof(orgunit_id)")
        cursor.execute("create index i0000487 on busprof(org_id)")
        # CONSTRAINTS:
    
    def userdemo(self):
        "stores demographics information for users."
        cursor.execute("""create table userdemo(
            users_id bigint not null,
            gender char(1),
            age integer,
            income integer,
            maritalstatus char(1),
            incomecurrency char(3),
            children integer,
            household integer,
            companyname varchar(128),
            hobbies varchar(254),
            orderbefore char(1),
            field1 char(1),
            timezone char(5),
            field2 char(1),
            field7 varcHar(64),
            field3 char(1),
            field4 char(1),
            field5 varchar(254),
            field6 integer,
            dateofbirth date,
            primary key(users_id)
        )""")
        # CONSTRAINTS:

if __name__=="__main__":
    m=Members()
    m.revokedtoken()
    m.role()
    m.roledesc()
    m.mbrrole()
    m.mbrgrpdesc()
    m.ccomment()
    m.repcustrel()
    m.mbrgrpusg()
    m.mbrgrptype()
    m.mbrgrp()
    m.mgpcondele()
    m.mgpcondelenvp()
    m.mbrgrpcond()
    m.mbrgrpmbr()
    m.mbrrel()
    m.addrbook()
    m.address()
    m.member()
    m.attrtype()
    m.mbrattr()
    m.mbrattrval()
    # m.storeent()
    # m.language()
    m.setcurr()
    m.orgcode()
    m.orgentity()
    m.users()
    m.userreg()
    m.userprof()
    m.busprof()
    m.userdemo()
