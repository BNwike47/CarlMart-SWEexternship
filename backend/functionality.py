import psycopg2
import psqlConfig
import dummydata

def database_exists(dbname, connection_params):
    try:
        with psycopg2.connect(**connection_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
                return cursor.fetchone() is not None
    except (Exception, psycopg2.Error) as error:
        print("Error checking database existence:", error)
        return False

def create_database(dbname, connection_params):
    try:
        with psycopg2.connect(**connection_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("CREATE DATABASE {};".format(dbname))
                print("Database '{}' created successfully.".format(dbname))
    except (Exception, psycopg2.Error) as error:
        print("Error creating database:", error)

# def execute_sql_script(script_path, connection_params):
#     try:
#         with psycopg2.connect(**connection_params) as conn:
#             with conn.cursor() as cursor:
#                 with open(script_path, "r") as script_file:
#                     sql_script = script_file.read()
#                     cursor.execute(sql_script)
#                 print("SQL script executed successfully.")
#     except (Exception, psycopg2.Error) as error:
#         print("Error executing SQL script:", error)

# def connect():
#     try:
#         conn = psycopg2.connect(dbname="postgres", 
#                                 user= psqlConfig.username, 
#                                 host = "localhost", 
#                                 port = 7777, 
#                                 password= psqlConfig.password)
#     except(Exception, psycopg2.Error) as error:
#                 print("Error connecting to PostgreSQL", error) 
#     cur = conn.cursor()
#     return cur

# #grabs a specific column list from the specifed table.  
# #Returns a list of tuples
# def select_query(table, column):
#     cur = connect()
#     query = 'SELECT ' + column + 'from ' + table
#     cur.execute(query)
#     results = cur.fetchall
#     return results

# #Fetches a row in the chosen table based on a specific column and id
# #Useful if looking for data related to a specifc user, item, etc.
# #Returns a list of tuples
# def select_data(table, column, id):
#     cur = connect()
#     query = 'SELECT * from ' + table + " WHERE " + column + " = " + id
#     cur.execute(query) 
#     result = cur.fetchall
#     return result

if __name__ == "__main__":
    conn = { "dbname": "postgres", 
                "user": psqlConfig.username, 
                "host" : "localhost", 
                "port" : 5432, 
                "password": psqlConfig.password}
    if not database_exists("carlmart", conn):
        create_database("carlmart", conn)
    # execute_sql_script("createtables.sql", conn)
    # dummydata.createDataInUsers()
    # dummydata.createDataInListings()
    # print(select_data("listings", "title", "lamp"))