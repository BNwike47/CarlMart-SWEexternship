from flask import Flask, jsonify, request
import psycopg2
import functionality
from flask_cors import CORS  # Import CORS
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime


app = Flask(__name__)
CORS(app)
cloudinaryConfig = None

def initCloudinary():
    load_dotenv()
    return cloudinary.config(secure=True)

cloudinaryConfig = initCloudinary()

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def homepage():
    functionality.create_tables()
    functionality.create_data()
    sort_query = ''
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is not None:
            sort_query = data['sort']
            print("This is the sort in home endpoint: ", data['sort'], flush=True)
    listings = functionality.select_all_listings(sort_query)
    return {"home": listings}

@app.route('/sort', methods=["POST"])
def sort():
    sort_query=''
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is not None:
            print("This is the sort in sort endpoint: ", data['sort'], flush=True)
            sort = data['sort']
            sort_query = functionality.sort_options(sort)
    return {"sort": sort_query}

@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is not None:
            print("This is the data from the login page: ", flush=True)
            for key in data:
                print(key + ": " + str(data[key]))
            # Process the received data or perform necessary operations
            # For example: save data to a database, perform calculations, etc.
            return jsonify({"message": "Data received successfully"}) #200
        else:
            return jsonify({"message": "No Json data received"})  # Return a bad request status if no JSON data found. 400
    return jsonify({"login": "no info received"})

@app.route('/new-listing', methods=["POST"])
def post_item_listing():
    if request.method == "POST":
        data = request.get_json()
        if data is not None:
            columns, parsed_data = functionality.create_new_listing(data, cloudinaryConfig)
            functionality.insert_row("listings", columns, parsed_data)
            return jsonify({"message": "Json data received"})
        else:
            return jsonify({"message": "No Json data received"})  # Return a bad request status if no JSON data found. 400
    return

@app.route("/get-signature", methods=["GET"])
def get_signature():
    if cloudinaryConfig is None:
        return jsonify({"error": "Cloudinary configuration not initialized"}), 500
    upload_preset = "jqajmneh"
    timestamp = round(datetime.utcnow().timestamp())
    params = {'timestamp': timestamp, 'upload_preset': upload_preset}
    signature = cloudinary.utils.api_sign_request(params, cloudinaryConfig.api_secret)
    print("signature= ", signature,flush=True)
    return jsonify({'timestamp': timestamp, 'signature': signature})

@app.route('/signup', methods=["POST"])
def create_user():
    data = request.get_json()
    data_list = []
    for key in data:
        data_list.append(data[key])

    parsed_data = tuple(data_list)
    functionality.insert_row("users", parsed_data)

    #return render_template('home.html')
    return

@app.route('/search', methods = ["GET"])
def get_listings():
    id = request.args.get('item')
    #category = request.args.get("category")
    print("search id: ", id, flush=True)
    listings_title = functionality.select_data("listings", "title", id)
    
    return (listings_title)


# @app.route('/categories', methods=["POST"])
# def categories():
#     if request.method == "POST":
#         data = request.get_json(silent=True)
#         if data is not None:
#             for key in data['categories']:
#                 listings = functionality.select_data("listings", "category", key)
#     return {"listings": listings}

@app.route('/filter', methods = ["GET"])
def get_filtered_listings():
    filters = request.args.get('item')
    filters = filters.split(',')
    if filters != '':
        listings = functionality.filter("listings", filters)
    else:
        listings = functionality.select_all_listings()
    return (listings)

#format: .../user?username=bobby
@app.route('/user', methods = ["GET"])
def get_user_profile():
    user_name = request.args.get('username')
    row = functionality.select_data("users", "username", user_name)
    #return render_template('home.html')
    return jsonify(row)

#Clicking a link to an item should open up that item's page with a url of /item?listing=quinns214532t645325
@app.route('/item', methods=['GET'])
def get_item():
    # Assuming you want to fetch all items for the '/api/item' endpoint
    items = functionality.select_all_listings()
    return jsonify(items)

#def sort 

@app.route('/item/delete')
def delete_listing():
    item = request.args.get('listing')
    result = functionality.delete_data("listings", "listing", item)
    if result == 1:
        return "Data deleted successfully", 200
    else:
        return "Deletion failed", 400

#Debating whether to leave this as constructing the contact under the assumption that it's an email
@app.route('/my_items', methods =['GET'])
def view_items():
    id = request.args.get('username')
    user = id + "@carleton.edu"
    listings = None
    try:
        listings = functionality.select_data("listings", "contact", user)
        return jsonify(listings)
    except Exception as e:
        print("Error: ", e)
        return "No data at that location", 400 
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # The port is specified here