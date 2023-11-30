from flask import Flask, jsonify, request
import psycopg2
import functionality

app = Flask(__name__)

# app = Flask(__name__, 
#         static_url_path='/static',
#         static_folder='static',
#         template_folder='templates')

@app.route('/')
@app.route('/home')
def homepage():
    #return render_template('home.html')
    return {"home": ["backend info 1", "backend info 2", "backend info 3"]}

#@app.route('/home', methods=["GET", "POST"])
#def display_data():
#    data = request.get_json()
#    print("This is the data that Hannah sent: ")
#    for key in data:
#        print(key + ": " + data[key])
#    #return render_template('home.html')
#    return

@app.route('/home', methods=["GET", "POST"])
def display_data():
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is not None:
            print("This is the data that Hannah sent: ")
            for key in data:
                print(key + ": " + str(data[key]))
            # Process the received data or perform necessary operations
            # For example: save data to a database, perform calculations, etc.
            return "Data received successfully", 200
        else:
            return "No JSON data received", 400  # Return a bad request status if no JSON data found
    else:
        return {"home": ["backend info 1", "backend info 2", "backend info 3"]}


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