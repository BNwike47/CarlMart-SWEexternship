from flask import Flask, jsonify, request
import psycopg2
import functionality


app = Flask(__name__, 
        static_url_path='/static',
        static_folder='static',
        template_folder='templates')

@app.route('/')
@app.route('/home')
def homepage():
    #return render_template('home.html')
    return

@app.route('/item')
def create_item_listing():
    #return render_template('home.html')
    return

@app.route('/user')
def user_profile(username):
    #return render_template('home.html')
    return

if __name__ == "__main__":
    app.run(debug=True, host='localhost')