from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin, login_required, current_user, logout_user
from ml import predict
import os
from dotenv import load_dotenv
from convex import ConvexClient

# Loading environment variable
load_dotenv(".env.local")
load_dotenv()

# Creating convex client object
client = ConvexClient(os.getenv("CONVEX_URL"))

# Creating a flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Setting up encryption and session management libraries
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# User class for session management
class User(UserMixin):
    def __init__(self, id_of_user, username, email, password):
        self.id = id_of_user
        self.username = username
        self.email = email
        self.password = password

# ask utkarsh
@login_manager.user_loader
def load_user(use_id):
    exist_user=client.query("tasks:get_user", dict(_id=use_id))
    user = User(exist_user["_id"], exist_user["username"], exist_user["email"], exist_user["password"])
    return user

"""    
This route is for accessing model. The input format is JSON
Example input: 
{
    "input" : "your question"
}
Response:
{
    "result": "output"
}
"""
@app.route('/', methods=['POST'])
def home():
    if request.is_json:
        data = request.get_json()

        input = data.get('input', None)
        input = str(input)

        if input is None:
            return jsonify({'error': 'No input data provided'}),400
        else:
            output = predict(input)

        return jsonify({"result": output})

    else:
        return jsonify({"error": "Request must be JSON"}),400


"""    
This route is for creating a new account. The input format is JSON
Example input: 
{
    "username" : "your username"
    "email" : "email",
    "password" : "password"
}
Response:
{
    'message' : 'Successfully Registered'
}
"""
@app.route('/registration', methods=['POST'])
def registration():
    if request.is_json:
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')

        exist_user = client.query("tasks:check_email", dict(email=email))
        if exist_user:
            return jsonify({'error': 'Email already exist'})
        
        hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
        client.mutation("tasks:createAccount", dict(username=username, email=email, password=hashed_password))
        return jsonify({'message' : 'Successfully Registered'})

    else:
        return jsonify({"error": "Request must be JSON"}), 400


"""    
This route is for logging in an existing account. The input format is JSON
Example input: 
{
    "email" : "email",
    "password" : "password"
}
Response:
{
    "message": "Login successful"
}
"""
@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()

        email = data.get('email')
        exist_user = client.query("tasks:check_email", dict(email=email))
        if exist_user is None:
            return jsonify("error : Email is not registered")

        password = data.get('password')
        if bcrypt.check_password_hash(exist_user["password"] , password):
            user = User(exist_user["_id"], exist_user["username"], exist_user["email"], exist_user["password"])
            login_user(user)
            return jsonify({"message": "Login successful"})
        else:
            return jsonify("error : Invalid Password")

    else:
        return jsonify({"error": "Request must be JSON"}), 400

"""
This route is for logging out from currently logged in account
Response:
{
    'message': '{username} is logged out'
}
"""
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user_name = current_user.username
    logout_user()
    return jsonify({'message': '{} is logged out'.format(logout_user_name)})

"""
This route is for checking current user
Response:
{
    'message': '{username} is currently logged in'
}
"""
@app.route('/account', methods=['GET'])
@login_required
def account():
    return jsonify({"message" : "{} is currently logged in".format(current_user.username)})

if __name__ == '__main__':
    app.run(debug=True)