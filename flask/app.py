from flask import Flask, request, jsonify, session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_cors import CORS, cross_origin
from emergency import e
from sentimental import analyze_sentiment
import re




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

    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{7,}$'
    if not re.match(password_regex, password):
        return jsonify({"message": "Password must be at least 7 characters long, contain at least one uppercase letter, one number, and one special character"}), 400

    # Date of birth validation
    dob_regex = r'^\d{2}-\d{2}-\d{4}$'
    try:
        datetime.strptime(dob, '%d-%m-%Y')
    except ValueError:
        return jsonify({"message": "Date of birth must be in the format dd-mm-yyyy"}), 400

    if not re.match(dob_regex, dob):
        return jsonify({"message": "Date of birth must be in the format dd-mm-yyyy"}), 400

    # Phone number validation
    phone_regex = r'^\d{10}$'
    if not re.match(phone_regex, phone):
        return jsonify({"message": "Phone number must be exactly 10 digits long"}), 400

    if not re.match(phone_regex, emergency_contact):
        return jsonify({"message": "Emergency contact must be exactly 10 digits long"}), 400

    if phone == emergency_contact:
        return jsonify({"message": "Phone number and emergency contact cannot be the same"}), 400
    
    
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
    else:
        previous_score = 0.0
        collection.insert_one({'email': email, 'sentiment_score': 0})

    current_score = analyze_sentiment(text)
    sentiment = determine_sentiment(previous_score, current_score)

    # Update the database with the current score
    collection.update_one({'email': email}, {'$set': {'sentiment_score': current_score}})

    return jsonify({'sentiment': sentiment, 'compound_score': current_score})

def determine_sentiment(previous_score, current_score):
    if current_score > previous_score:
        return "It's great to hear that you're feeling more positive than before! Keep up the good work!"
    elif current_score < previous_score:
        return "I'm sorry to hear that you're feeling less positive than before. Remember, ups and downs are normal, and it's okay to seek support when you need it."
    else:
        return "It sounds like your sentiment hasn't changed much since the last time. Remember to take care of yourself and reach out if you need help managing your emotions."

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


