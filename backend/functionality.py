import psycopg2
from datetime import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api

DB_NAME = "carlmart"
DB_USER = "postgres"
DB_PASS = "carlsarecool"
DB_HOST = "db"
DB_PORT = "5432"

conn = None

#creates a connection to the database
def connect():
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)
        cur = conn.cursor()
        return cur, conn
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL", error)
        return None, None
    
#creating the tables in the database if they don't exist
def create_tables():
    """Creates SQL table. Restarts docker container if SQL hasn't initialized yet."""
    cur, conn = connect()
    try:
        # executing queries to create table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS 
            listings(
                listing varchar(30) PRIMARY KEY,
                title varchar(50),
                description varchar(150),
                price int,
                contact varchar(50),
                image text,
                category text,
                condition text,
                timestamp timestamp
            );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS 
            users( 
                username varchar(50) PRIMARY KEY,
                listings text,
                rating real
            );
        """)
        
        # commit the changes
        conn.commit()
        conn.close()
    except:
        raise ConnectionError('PostgresSQL rejected connection. Trying again')
    return

#inserting some data into the database if it doesn't already exist
def create_data():
    query = "INSERT INTO listings (listing, title, description, price, contact, image) SELECT 'laz1129231230', 'Calc Textbook', 'Fundamentals of Calculus 9th edition', 50, 'laz@carleton.edu', 'carlmart/calc_lebbeq'  WHERE NOT EXISTS (SELECT listing FROM listings WHERE listing = 'laz1129231230')"
    query1 = "INSERT INTO listings (listing, title, description, price, contact, image) SELECT 'moranh1130231045', 'Lamp', 'Used lamp', 10, 'moranh@carleton.edu', 'carlmart/lamp_dtrcpw' WHERE NOT EXISTS (SELECT listing FROM listings WHERE listing = 'moranh1130231045')"    
    query2 = "INSERT INTO listings (listing, title, description, price, contact, image) SELECT 'nwikeb1201231500', 'Cactus', 'Cute little cactus', 5, 'nwikeb@carleton.edu', 'carlmart/cactus_tjedp7' WHERE NOT EXISTS (SELECT listing FROM listings WHERE listing = 'nwikeb1201231500')"    
    query3 = "INSERT INTO listings (listing, title, description, price, contact, image) SELECT 'quinns0112230950', 'Nintendo Switch', 'used switch good condition', 45, 'quinns@carleton.edu', 'carlmart/nintendo_byntfb'  WHERE NOT EXISTS (SELECT listing FROM listings WHERE listing = 'quinns0112230950')"
    query4 = "INSERT INTO listings (listing, title, description, price, contact, image) SELECT 'quinns0112231000', 'Beanbag chair', 'black beanbag chair medium size', 30, 'quinns@carleton.edu', 'carlmart/beanbag_w6pryd'  WHERE NOT EXISTS (SELECT listing FROM listings WHERE listing = 'quinns0112231000')"
    query5 = "INSERT INTO listings (listing, title, description, price, contact, image) SELECT 'quinns0112231010', 'Ipad', 'like new ipad 10 in.', 800, 'quinns@carleton.edu', 'carlmart/ipad_oljnha'  WHERE NOT EXISTS (SELECT listing FROM listings WHERE listing = 'quinns0112231010')"

    queries = [query, query1, query2, query3, query4, query5]
    cur, conn = connect()
    for query in queries:
        cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

#grabs a specific column list from the specifed table.  
#Returns a list of tuples
def select_query(table, column):
    cur, conn = connect()
    query = "SELECT " + column + "FROM " + table + ";"
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

#Fetches a row in the chosen table based on a specific column and id
#Useful if looking for data related to a specifc user, item, etc.
#Returns a list of tuples
def select_data(table, column, id):
    cur, conn = connect()
    query = 'SELECT * FROM ' + table + " WHERE " + column + " = " + id + ";"
    cur.execute(query) 
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

#Insert a tuple of data into a SQL table
#Format:
#-Users: (username, listings, rating)
#-Listings: (listing, title, description, price, contact, image)
def insert_row(table, columns, data):
    cur, conn = connect()
    query = 'INSERT INTO ' + table + columns + ' VALUES ' + data + ";"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    return

#returns the title, description, price, contact, and image for all listings in the listings datatable
#returns a list of tuples
def select_all_listings(sort):
    cur, conn = connect()
    query = 'SELECT title, description, price, contact, image FROM "listings"' + sort
    result = "no result yet"
    try:
        cur.execute(query) 
        result = cur.fetchall()
    except Exception as e:
        print("Error executing SQL query: ", e)
    cur.close()
    conn.close()
    return result

def sort_by_price_low_to_high():
    return "ORDER BY price ASC"
def sort_by_price_high_to_low():
    return "ORDER BY price DESC"
def sort_by_date_newest():
    return "ORDER BY timestamp DESC"
def sort_by_date_oldest():
    return "ORDER BY price ASC"

def delete_data(table, column, id):
    cur, conn = connect()
    query = 'DELETE FROM '+ table + 'WHERE ' + column + " = " + id + ";"
    try:
        cur.execute(query)
        result = 1 
    except Exception as e:
        print("Error executing SQL query: ", e)
        result = 0

    cur.close()
    conn.close()
    return result

#TODO make listing id connect to signed-in username
def create_new_listing(data, cloudinaryConfig):
    data_list = []
    columns = "("
    for key in data:
        if key == 'image' and data[key] is not None:
            validation = validateSignature(data['image'], cloudinaryConfig)
            if validation:
                data_list.append(validation)
                columns += key + ", "
        elif data[key] != '' and data[key] is not None:
            data_list.append(data[key])
            columns += key + ", "
    columns += "listing, timestamp)"
    listing_id, now = create_listing_id("quinns")
    data_list.append(listing_id, now)
    parsed_data = str(tuple(data_list))
    return columns, parsed_data

def validateSignature(photoData, cloudinaryConfig):
    print("photodata: ", photoData, flush=True)
    public_id = photoData['public_id']
    version = photoData['version']
    signature = photoData['signature']
    params = { 'public_id': public_id, 'version': version }
    expectedSignature = cloudinary.utils.api_sign_request(params, cloudinaryConfig.api_secret)
    if expectedSignature == signature:
        print("public_id", public_id,flush=True)
        return public_id
    return False

#creates listing id and timestamp
def create_listing_id(username):
    now = datetime.now()
    dt_string = now.strftime("%m%d%Y%H%M%S")
    listing_id = username + dt_string
    return listing_id, now

if __name__ == "__main__":
    connect()