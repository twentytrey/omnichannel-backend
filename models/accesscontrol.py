from db_con import con,cursor
from functions import build_constraint

class AccessControl:
    """the access control data model shows relationships between the access control
    policy tables. an access control policy is composed of a member group, resource group
    and action group. it can optionally contain a relationship group as well. access control 
    policies are grouped into policy groups, to which organizations subscribe."""
    def acplgpdesc(self):
        "stores locale-specific information for te acpolgrp table."
        cursor.execute("""create table acplgpdesc(
            acpolgrp_id integer not null,
            language_id integer not null,
            displayname varchar(254)not null,
            description varchar(700),
            primary key(acpolgrp_id,language_id)
        )""")
        # CONSTRAINTS
    
    def acpolsubgp(self):
        "parent child-relationships between access control policy groups"
        cursor.execute("""create table acpolsubgp(
            child_id integer not null,
            parent_id integer not null,
            primary key(child_id,parent_id)
        )""")
        cursor.execute("create index i0000441 on acpolsubgp(parent_id)")
        # CONSTRAINTS
    
    def acpolgrp(self):
        """stores all the access control policy groups in the system.
        each row in this table represents a policy group."""
        cursor.execute("""create table acpolgrp(
            acpolgrp_id serial not null,
            name varchar(128)not null,
            member_id bigint not null,
            primary key(acpolgrp_id)
        )""")
        cursor.execute("create unique index i0000306 on acpolgrp(name,member_id)")
        cursor.execute("create index i0000439 on acpolgrp(member_id)")
        # CONSTRAINTS:
    
    def acplgpsubs(self):
        """stores the association between access control policy groups and 
        organizational entities. an organizational entity that is associated with 
        a policy group is said to subscribe to that policy group. the access control policies
        belonging to that policy group will apply to that organization. an organization
        can subscribe to multiple policy groups and multiple organizations can subscribe to the same
        policy group."""
        cursor.execute("""create table acplgpsubs(
            acpolgrp_id integer not null,
            orgentity_id bigint not null,
            primary key(orgentity_id,acpolgrp_id)
        )""")
        cursor.execute("create index i0000437 on acplgpsubs(acpolgrp_id)")
        # CONSTRAINTS:
    
    def acpolgppol(self):
        """stores the association between access control policy groups
        and access control policies. an access control policy that belongs
        to a policy group will be applied to all the organizxations that
        subscribe to that policy group."""
        cursor.execute("""create table acpolgppol(
            acpolicy_id integer not null,
            acpolgrp_id integer not null,
            primary key(acpolicy_id,acpolgrp_id)
        )""")
        cursor.execute("create index i0000438 on acpolgppol(acpolgrp_id)")
        # CONSTRAINTS:
    
    def acresgrp(self):
        """stores all the access control resource groups in the system.
        the conditions column stores text document containing the constraints
        and the attributes value pairs used for grouping the resources."""
        cursor.execute("""create table acresgrp(
            acresgrp_id serial not null,
            member_id bigint not null,
            grpname varchar(254)not null,
            description varchar(254),
            conditions text,
            field1 varchar(254),
            field2 varchar(254),
            primary key(acresgrp_id)
        )""")
        cursor.execute("create unique index i0000010 on acresgrp(grpname)")
        cursor.execute("create index i0000446 on acresgrp(member_id)")
        # CONSTRAINTS:
    
    def acresgpdes(self):
        "stores locale-specific display information for the acresgrp table"
        cursor.execute("""create table acresgpdes(
            acresgrp_id integer not null,
            displayname varchar(700) not null,
            description varchar(700),
            language_id integer not null,
            primary key(acresgrp_id,language_id)
        )""")
        # CONSTRAINTS:
    
    def acactgrp(self):
        """stores all the access control policies in the system.
        every policy refers to an action group, a member group,
        a resource group and optionally, a relationship."""
        cursor.execute("""create table acactgrp(
            acactgrp_id serial not null,
            groupname varchar(128)not null,
            member_id bigint not null,
            field1 varchar(128),
            primary key(acactgrp_id)
        )""")
        cursor.execute("create unique index i0000001 on acactgrp(groupname)")
        cursor.execute("create index i0000427 on acactgrp(member_id)")
        # CONSTRAINTS:
    
    def acacgpdesc(self):
        """stores all the access control policies in the system.
        every policy refers to an action group, a member group, a resource group
        and optionally a relationship."""
        cursor.execute("""create table acacgpdesc(
            acactgrp_id integer not null,
            displayname varchar(700),
            description varchar(700),
            language_id integer not null,
            primary key(acactgrp_id,language_id)
        )""")
        # CONSTRAINTS:
    
    def acactdesc(self):
        """stores locale-specific information
        for the access control actions which are stored in the acaction table."""
        cursor.execute("""create table acactdesc(
            acaction_id integer not null,
            displayname varchar(700)not null,
            description varchar(700),
            language_id integer not null,
            primary key(acaction_id,language_id)
        )""")
        # CONSTRAINTS:
    
    def acactactgp(self):
        """stores all the access control policies in the system.
        every policy refers to an action group. a member group, a resource group.
        and optinally,  a relationship"""
        cursor.execute("""create table acactactgp(
            acactgrp_id integer not null,
            acaction_id integer not null,
            field1 varchar(128),
            primary key(acactgrp_id,acaction_id)
        )""")
        cursor.execute("create index i0000426 on acactactgp(acaction_id)")
        # CONSTRAINTS:
    
    def acpolicy(self):
        """stores all the access control policies in the system.
        every policy refers to an action group, a member group 
        and a resource group and optinally, a relationship."""
        cursor.execute("""create table acpolicy(
            acpolicy_id serial not null,
            policyname varchar(128),
            acrelgrp_id integer,
            acactgrp_id integer not null,
            acresgrp_id integer not null,
            acrelation_id integer,
            policytype integer,
            field1 varchar(128),
            mbrgrp_id bigint not null,
            member_id bigint not null,
            primary key(acpolicy_id)
        )""")
        cursor.execute("create unique index i0000006 on acpolicy(policyname,member_id)")
        cursor.execute("create index i0000316 on acpolicy(acresgrp_id)")
        cursor.execute("create index i0000317 on acpolicy(member_id)")
        cursor.execute("create index i0000318 on acpolicy(acrelation_id)")
        cursor.execute("create index i0000319 on acpolicy(mbrgrp_id)")
        cursor.execute("create index i0000320 on acpolicy(acactgrp_id)")
        cursor.execute("create index i0000440 on acpolicy(acrelgrp_id)")
        # CONSTRAINTS:
    
    def acpoldesc(self):
        "stores locale-specific info for the acpolicy table"
        cursor.execute("""create table acpoldesc(
            acpolicy_id integer not null,
            language_id integer not null,
            displayname varchar(700)not null,
            description varchar(700),
            primary key(acpolicy_id,language_id)
        )""")
        # CONSTRAINTS:
    
    def acorgpol(self):
        "do not apply template policies referenced here to organizational entities referenced here."
        cursor.execute("""create table acorgpol(
            acpolicy_id integer not null,
            member_id bigint not null,
            primary key(acpolicy_id,member_id)
        )""")
        cursor.execute("create index i0000436 on acorgpol(member_id)")
        # CONSTRAINTS
    
    def acresgpres(self):
        """associates control resource groups with resource categories. or calsses of resources.
        you can use this table to group various resources together based on teir class names."""
        cursor.execute("""create table acresgpres(
            acresgrp_id integer not null,
            acrescgry_id integer not null,
            field1 varchar(128),
            primary key(acresgrp_id,acrescgry_id)
        )""")
        cursor.execute("create index i0000445 on acresgpres(acrescgry_id)")
        # CONSTRAINTS:
    
    def acaction(self):
        "stores all the access control actions in the system"
        cursor.execute("""create table acaction(
            acaction_id serial not null,
            action varchar(254)not null,
            primary key(acaction_id)
        )""")
        cursor.execute("create unique index i0000002 on acaction(action)")
    
    def acreldesc(self):
        """stores the locale-specific information for the access control
        relationships which are stored in the acrelation table."""
        cursor.execute("""create table acreldesc(
            acrelation_id integer not null,
            displayname varchar(254)not null,
            description varchar(254),
            language_id integer not null,
            primary key(acrelation_id,language_id)
        )""")
        # CONSTRAINTS:
    
    def acrelation(self):
        """a master list of all the access control relationships that exist in
        the system. these relationships are between resources that are protected
        and the members in the system."""
        cursor.execute("""create table acrelation(
            acrelation_id serial not null,
            relationname varchar(128)not null,
            primary key(acrelation_id)
        )""")
        cursor.execute("create index i0000007 on acrelation(relationname)")
    
    def acresrel(self):
        """associates an access control resource with the relationships
        that it supports. given a resource, you can find out the possile relationships
        that it can have and also the table and the columns in which these relationships are stored."""
        cursor.execute("""create table acresrel(
            acrelation_id integer not null,
            acrescgry_id integer not null,
            resreltable varchar(64)not null,
            resrelmemcol varchar(64)not null,
            resrelkeycol varchar(64),
            resrelcol varchar(64),
            resjoincol varchar(64),
            field1 varchar(128),
            resourcetype varchar(64),
            primary key(acrelation_id,acrescgry_id)
        )""")
        cursor.execute("create index i0000448 on acresrel(acrescgry_id)")
        # CONSTRAINTS:
    
    def acrescgry(self):
        """stores all the access control resource entries in the system.
        and the meta data information about them. the meta data includes information about the
        table and the columns that store the resources belonging to the resource category."""
        cursor.execute("""create table acrescgry(
            acrescgry_id serial not null,
            resprimarytable varchar(64),
            resownertable varchar(64),
            resownercol varchar(64),
            reskeyowncol varchar(64),
            field1 varchar(128),
            resclassname varchar(254)not null,
            resjoinkey varchar(64),
            primary key(acrescgry_id)
        )""")
        cursor.execute("create unique index i0000009 on acrescgry(resclassname)")
    
    def acresact(self):
        """captures the relationship between access control resources and actions.
        given a resource, you can find out the associated actions from this table."""
        cursor.execute("""create table acresact(
            acrescgry_id integer not null,
            acaction_id integer not null,
            primary key(acrescgry_id,acaction_id)
        )""")
        cursor.execute("create index i0000443 on acresact(acaction_id)")
        # CONSTRAINTS:
    
    def acrescgdes(self):
        "locale-specific data for acresgry table"
        cursor.execute("""create table acrescgdes(
            language_id integer not null,
            acrescgry_id integer not null,
            displayname varchar(700)not null,
            description varchar(700),
            primary key(language_id,acrescgry_id)
        )""")
        cursor.execute("create index i0000949 on acrescgdes(acrescgry_id)")
        # CONSTRAINTS:
    
    def acattrdesc(self):
        """stores all the access control policies in the system
        every policy refers to an action group, a member group,
        a resource group and optionally, a relationship."""
        cursor.execute("""create table acattrdesc(
            acattr_id bigint not null,
            displayname varchar(254)not null,
            description varchar(254),
            language_id integer not null,
            primary key(acattr_id,language_id)
        )""")
    
    def acattr(self):
        """stores all the access control policies in the system.
        every policy refers to an action group, a member group, 
        and a resource group and optinoally,  a relationship"""
        cursor.execute("""create table acattr(
            acattr_id bigserial not null,
            attrname varchar(128)not null,
            datatype integer not null,
            field1 varchar(128)not null,
            primary key(acattr_id)
        )""")
        cursor.execute("create unique index i0000003 on acattr(attrname)")

    def acresmemrl(self):
        "stores resource-member relationships for resources of different types"
        cursor.execute("""create table acresmemrl(
            resourceid bigint,
            acresmemrl_id bigserial not null,
            member_id bigint not null,
            acrelation_id integer not null,
            acrescgry_id integer not null,
            primary key(acresmemrl_id)
        )""")
        cursor.execute("create unique index i0000011 on acresmemrl(member_id,resourceid,acrelation_id,acrescgry_id)")
        cursor.execute("create index i0000012 on acresmemrl(resourceid,acrelation_id,acrescgry_id)")
        cursor.execute("create index i0000447 on acresmemrl(acrescgry_id)")
        # CONSTRAINTS:
    
    def acresatrel(self):
        """stores the relationship between access control resources and attributes.
        these attributes are used to implicitly group resources.
        given a resource, you can find out the supported attributes from this table.
        the metadata about attributes is used in the GUI for definiing resource groups and als
        for generating SQL statements for filtering."""
        cursor.execute("""create table acresatrel(
            acattr_id bigint not null,
            acrescgry_id integer not null,
            attrtblname varchar(64)not null,
            attrcolname varchar(64)not null,
            reskeycolname varchar(64)not null,
            field1 varchar(128),
            primary key(acattr_id,acrescgry_id)
        )""")
        cursor.execute("create index i0000444 on acresatrel(acrescgry_id)")
        # CONSTRAINTS:
    
    def acresprim(self):
        """Stores the primary resource column names for an access control resource.
        a given resource can have more thean one primary column"""
        cursor.execute("""create table acresprim(
            acrescgry_id integer not null,
            resprimarycol varchar(64)not null,
            field1 varchar(128),
            primary key(acrescgry_id)
        )""")
        # CONSTRAINT:
    
    def acrelgrp(self):
        """master list of all the access control relationship groups that
        exist in the system. these relationship groups are between 
        resources that are protected and users in the system"""
        cursor.execute("""create table acrelgrp(
            acrelgrp_id serial not null,
            member_id bigint not null,
            grpname varchar(2500),
            field1 varchar(64),
            description varchar(254),
            primary key(acrelgrp_id)
        )""")
        cursor.execute("create unique index i0000008 on acrelgrp(grpname,member_id)")
        cursor.execute("create index i0000442 on acrelgrp(member_id)")
        # CONSTRAINTS:

if __name__=="__main__":
    a=AccessControl()
    a.acplgpdesc()
    a.acpolsubgp()
    a.acpolgrp()
    a.acplgpsubs()
    a.acpolgppol()
    a.acresgrp()
    a.acresgpdes()
    a.acactgrp()
    a.acacgpdesc()
    a.acactdesc()
    a.acactactgp()
    a.acpolicy()
    a.acpoldesc()
    a.acorgpol()
    a.acresgpres()
    a.acaction()
    a.acreldesc()
    a.acrelation()
    a.acresrel()
    a.acrescgry()
    a.acresact()
    a.acrescgdes()
    a.acattrdesc()
    a.acattr()
    a.acresmemrl()
    a.acresatrel()
    a.acresprim()
    a.acrelgrp()
