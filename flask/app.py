from flask import Flask, request, jsonify, session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_cors import CORS, cross_origin
from emergency import e
from sentimental import analyze_sentiment




app = Flask(__name__)
CORS(app, supports_credentials=True)
CORS(app, resources={r"/analyze_sentiment": {"origins": "http://localhost:3000"}})


app.config["MONGO_URI"] = "mongodb://localhost:27017/selfheal"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)


app.config['SECRET_KEY'] = 'thisisasecretkey'


collection = mongo.db.sentimental


def check_db_connection():
    try:
        if mongo.db is not None:
            print("Connected to MongoDB")
        else:
            print("Failed to connect to MongoDB: mongo.db is None")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")


check_db_connection()


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


@app.route('/register', methods=['POST','OPTIONS','GET'])
@cross_origin()
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    dob = data.get('dob')
    phone = data.get('phone')
    emergency_contact = data.get('emergency_contact')


    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


    user_exists = mongo.db.users.find_one({'email': email})
    if user_exists:
        return jsonify({"message": "Email already exists"}), 400


    mongo.db.users.insert_one({
        'name': name,
        'email': email,
        'password': hashed_password,
        'dob': dob,
        'phone': phone,
        'emergency_contact': emergency_contact,
        'created_at': datetime.now()
    })


    return jsonify({"message": "Registered successfully"}), 201


@app.route('/login', methods=['POST','GET','OPTIONS'])
@cross_origin()
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = mongo.db.users.find_one({'email': email})


    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid email or password"}), 401


    # Initialize the session with user's email upon successful login
    session['email'] = email
    return jsonify({"message": "Logged in successfully"}), 200


@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    session.pop('email', None)
    return jsonify({"message": "Logged out successfully"}), 200




@app.route('/analyze_sentiment', methods=['POST'])
@cross_origin()
def analyze_sentiment_route():
    data = request.json
    text = data['text']
    email = data['email']
    
    existing_record = collection.find_one({'email': email})
    if existing_record:
        previous_score = existing_record.get('sentiment_score', 0)
        collection.update_one({'email': email}, {'$set': {'sentiment_score': previous_score}})
    else:
        previous_score = 0.0
        collection.insert_one({'email': email, 'sentiment_score': 0})

    sentiment, compound_score = analyze_sentiment(text)

    pass_previous_score_to_sentimental(previous_score)

    collection.update_one({'email': email}, {'$set': {'sentiment_score': compound_score}})

    return jsonify({'sentiment': sentiment, 'compound_score': compound_score})


def pass_previous_score_to_sentimental(previous_score):
    # Import the analyze_sentiment function from sentimental.py
    
    # Call analyze_sentiment with the previous score
    analyze_sentiment('Previous score: {}'.format(previous_score))


@app.route('/emergency', methods=['POST','GET','OPTIONS'])
@cross_origin(origins="*")
def emergency():
    #if request.method == 'OPTIONS':
        #return _build_cors_preflight_response()
    
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json()
    print('data', data)
    if len(data) == 0:
        return jsonify({"error": "Invalid JSON"}), 400
   
    user_email = data['email']
    if len(user_email) == 0:
        return jsonify({"error": "User not authenticated"}), 401

    print(user_email)
    e(user_email, mongo)
    # Handle emergency logic here

    return jsonify({"message": "Emergency alert sent"}), 200


'''def _build_cors_preflight_response():
    response = jsonify({'message': 'CORS preflight'})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response'''
    
if __name__ == '__main__':
    app.run(debug=True)


