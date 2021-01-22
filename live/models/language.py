from db_con import con,cursor
from functions import build_constraint

class Language:
    """the language data model shows that a store can specify
    alternative languages, in pairs."""

    def language(self):
        """Each row of this table represents a language. using the predefined ISO codes
        users can add supported languages."""
        cursor.execute("""create table language(
            language_id integer not null,
            localename char(16),
            language varchar(5),
            country char(5),
            variant char(10),
            encoding varchar(32),
            mimeset varchar(32),
            primary key(language_id)
        )""")

    def languageds(self):
        "each row of this table contains lang-dependent information for a particular language"
        cursor.execute("""create table languageds(
            language_id integer not null,
            description varchar(254)not null,
            language_id_desc integer,
            primary key(language_id)
        )""")
        # CONSTRAINTS:
    
    def langpair(self):
        """each row of this table represents an alternative language relationship
        for a particular store entity. when information is not available in the requested
        language, information in the alternative language is provided."""
        cursor.execute("""create table langpair(
            storeent_id integer not null,
            language_id integer not null,
            language_id_alt integer not null,
            sequence float not null default 0,
            primary key(language_id,language_id_alt,storeent_id)
        )""")
        cursor.execute("create index i0000603 on langpair(storeent_id)")
        # CONSTRAINTS:

    def country(self):
        """lists the country or region names in each of the supported languages identified by 
        language_id. note that some of the entries may store the region name rather than the
        official country name in the name column for historical reasons."""
        cursor.execute("""create table country(
            countryabbr char(5)not null,
            language_id integer not null,
            name varchar(254),
            callingcode varchar(64),
            primary key(countryabbr,language_id)
        )""")
        cursor.execute("create index i0000342 on country(language_id,name)")
        cursor.execute("create index i0000343 on country(name)")
        # CONSTRAINTS
    
    def stateprov(self):
        """lists the states and province names (by country or region) in each
        of the supported languages identified by language_id"""
        cursor.execute("""create table stateprov(
            stateprovabbr char(20)not null,
            language_id integer not null,
            name varchar(254),
            countryabbr char(5),
            primary key(stateprovabbr,language_id)
        )""")
        cursor.execute("create index i0000340 on stateprov(language_id,name)")
        cursor.execute("create index i0000341 on stateprov(language_id,name,countryabbr)")
        # CONSTRAINTS

if __name__=="__main__":
    l=Language()
    # drop prvious implementation of language table
    l.language()
    l.languageds()
    l.langpair()
    l.country()
    l.stateprov()
