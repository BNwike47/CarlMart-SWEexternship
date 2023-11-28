import psycopg2


conn = psycopg2.connect(dbname="", 
                            user="tbd", 
                            host = 'tbd', 
                            port = 1234, 
                            password="tbd")

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
