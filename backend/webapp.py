from flask import Flask, jsonify, request
import psycopg2
import functionality

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def homepage():
    functionality.create_tables()
    functionality.create_data()
    listings = functionality.select_all_listings()
    return {"home": listings}

@app.route('/new_item', methods=["POST"])
def create_item_listing():
    data = request.get_json()
    data_list = []
    for key in data:
        data_list.append(data[key])

    parsed_data = tuple(data_list)
    functionality.insert_row("Listings", parsed_data)

    #return render_template('home.html')
    return

@app.route('/new_user', methods=["POST"])
def create_user():
    data = request.get_json()
    data_list = []
    for key in data:
        data_list.append(data[key])

    parsed_data = tuple(data_list)
    functionality.insert_row("Users", parsed_data)

    #return render_template('home.html')
    return


#format: .../user?username=bobby
@app.route('/user')
def get_user_profile():
    user_name = request.args.get('username')
    row = functionality.select_data("Users", "username", user_name)
    #return render_template('home.html')
    return row

#Clicking a link to an item should open up that item's page with a url of /item?listing=quinns214532t645325
@app.route('/item')
def get_item():
    item = request.args.get('listing')
    row = functionality.select_data("Listings", "listing", item)
    #return render_template('home.html')
    return row

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")