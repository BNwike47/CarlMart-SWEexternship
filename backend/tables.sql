"""THIS IS NOT ACTUALLY USED TO CREATE TABLES. JUST HERE TO HAVE THE CODE"""
CREATE TABLE IF NOT EXISTS 
            listings(
                listing varchar(30) PRIMARY KEY,
                title varchar(50),
                description varchar(150),
                price int,
                contact varchar(50),
                image bytea,
                tags text
            );

CREATE TABLE IF NOT EXISTS 
    users( 
        username varchar(50) PRIMARY KEY,
        listings text,
        rating real
    );