import psycopg2


DB_NAME = "carlmart"
DB_USER = "postgres"
DB_PASS = "carlsarecool"
DB_HOST = "db"
DB_PORT = "5432"

conn = None

def connect():
    try:
        global conn
        conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
        cur = conn.cursor()
        print("Connected to database!", flush=True)
        return cur, conn
    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL", error) 
        return 
    
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
                image bytea,
                tags text
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
        print("Table Created successfully")

    except:
        raise ConnectionError('PostgresSQL rejected connection. Trying again')
    return

def create_data():
    query = "INSERT INTO listings (listing, title, description, price, contact) SELECT 'laz1129231230', 'calculus textbook', 'Fundamentals of Calculus 9th edition', 50, 'laz@carleton.edu' WHERE NOT EXISTS (SELECT listing FROM listings WHERE listing = 'laz1129231230')"
    # query1 = "INSERT INTO users (username, listings, rating) VALUES ('laz', 'laz1129231230', 5.0);"
    # query2 = "INSERT INTO users (username, rating) VALUES ('nwikeb', 5.0);"
    # query3 = "INSERT INTO users (username, listings, rating) VALUES ('moranh', 'moranh1130230500', 5.0);"
    # query4 = "INSERT INTO listings (listing, title, description, price, contact) VALUES ('moranh1130231045', 'leather couch', 'gently used black leather couch', 30, 'moranh@carleton.edu');"
    cur, conn = connect()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
#grabs a specific column list from the specifed table.  
#Returns a list of tuples
def select_query(table, column):
    cur, conn = connect()
    query = 'SELECT ' + column + 'from ' + table
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
    query = 'SELECT * from ' + table + " WHERE " + column + " = " + id
    cur.execute(query) 
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

#Insert a tuple of data into a SQL table
#Format:
#-Users: (username, listings, rating)
#-Listings: (listing, title, description, price, contact, image)
def insert_row(table, data):
    cur, conn = connect()
    query = 'INSERT INTO ' + table + ' VALUES ' + data
    cur.execute(query)
    cur.close()
    conn.close()
    return

def select_all_listings():
    cur, conn = connect()
    query = 'SELECT * FROM "listings";'
    result = "no result yet"
    try:
        cur.execute(query) 
        result = cur.fetchall()
    except Exception as e:
        print("Error executing SQL query: ", e)
    cur.close()
    conn.close()
    return result



if __name__ == "__main__":
    connect()