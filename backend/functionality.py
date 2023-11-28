import psycopg2
import psqlConfig
import dummydata

conn = None
try:
    conn = psycopg2.connect(dbname="", 
                            user= psqlConfig.username, 
                            host = "localhost", 
                            port = 7777, 
                            password= psqlConfig.password)
except(Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL", error) 

#Creates a cursor 
cur = conn.cursor()

#grabs a specific column list from the specifed table.  
#Returns a list of tuples
def select_query(table, column):
    query = 'SELECT ' + column + 'from ' + table
    cur.execute(query)
    results = cur.fetchall
    return results

#Fetches a row in the chosen table based on a specific column and id
#Useful if looking for data related to a specifc user, item, etc.
#Returns a list of tuples
def select_data(table, column, id):
    query = 'SELECT * from ' + table + " WHERE " + column + " = " + id
    cur.execute(query) 
    result = cur.fetchall
    return result

if __name__ == "__main__":
      dummydata.createDataInUsers()
      dummydata.createDataInListings()
      print(select_data("listings", "title", "lamp"))