
def createDataInUsers():
    query = "INSERT INTO users (username, listings, rating) VALUES ('quinns', 'quinns1128231300', 5.0);"

def createDataInListings():
    query = "INSERT INTO listings (listing, title, description, price, contact) VALUES ('quinns1128231300', 'lamp', 'plain black desk lamp', 5, 'quinns@carleton.edu');"

"INSERT INTO listings (listing, title, description, price, contact) VALUES ('laz1129231230', 'calculus textbook', 'Fundamentals of Calculus 9th edition', 50, 'laz@carleton.edu');"
"INSERT INTO users (username, listings, rating) VALUES ('laz', 'laz1129231230', 5.0);"