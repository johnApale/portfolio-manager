# app.py
from flask import Flask, Blueprint, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables from the .env file
load_dotenv()

SECRET_KEY = os.urandom(32)
DATABASE_URL = os.getenv("DATABASE_URL")

# Define app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from routes.main_routes import main_bp
app.register_blueprint(main_bp)


#### ---------------------------------- DB Models ---------------------------------- #####
from datetime import datetime
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

from sqlalchemy import CheckConstraint

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    is_selected = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("section IN ('headline', 'bio')"),
    )


class ContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email_address = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    location = db.Column(db.String(255))

class SocialLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    contact_info_id = db.Column(db.Integer, db.ForeignKey('contact_info.id'))
    contact_info = db.relationship("ContactInfo", back_populates="social_links")

# Add a relationship from ContactInfo to SocialLink
ContactInfo.social_links = db.relationship("SocialLink", order_by=SocialLink.id, back_populates="contact_info")



#### ---------------------------------- API Routes ---------------------------------- #####


### ----- Users API Endpoints ----- ###

# Generate mock users endpoint
from faker import Faker
@app.route('/api/generate_mock_users')
def generate_mock_users():
        fake = Faker()

        for _ in range(10): 
            user = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password=fake.password(),
                is_admin=fake.random_element(elements=(True, False)),
                last_login=fake.date_time_this_decade(),
            )

            db.session.add(user)
        
        db.session.commit()
        return "Mock users generated and added to the database."

# Get All Users Endpoint (GET request)
@app.route('/api/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        user_list = [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'is_admin':user.is_admin, 'last_login': user.last_login} for user in users]
        return jsonify({'users': user_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create User Endpoint (POST request)
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json  # Assuming you are sending JSON data in the request

    if data['password'] != data['confirm_password']:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Check if the user with the given email already exists
    existing_user = User.query.filter_by(email=data['email']).first()

    if existing_user:
        return jsonify({'error': 'User with this email already exists.'}), 400


    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],
        is_admin=data['is_admin'],  # Assuming is_admin is a boolean
        last_login=null,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

# Get User by ID Endpoint (GET request)
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)

    if user:
        return jsonify({'user': {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin,
            'last_login': user.last_login
        }})

    # If the user with the given ID does not exist, return a 404 error
    abort(404)

# Update User Endpoint (PUT request)
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)

    if user:
        data = request.json
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.is_admin = data.get('is_admin', user.is_admin)

        db.session.commit()

        return jsonify({'message': 'User updated successfully', 'user': {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin,
            'last_login': user.last_login
        }})
    else:
        return jsonify({'error': 'User not found'}), 404

# Delete User Endpoint (DELETE request)
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully', 'deleted_user': {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin,
            'last_login': user.last_login
        }})
    else:
        return jsonify({'error': 'User not found'}), 404

### ----- End of Users API Endpoint ----- ###

### ------- Profile API Endpoints ------- ###


# Create Profile Endpoint (POST request)
@app.route('/api/add_profile', methods=['GET', 'POST'])
def add_profile():

    data = request.json

    # Check if content already exists
    existing_content = Profile.query.filter_by(content=data['content']).first()

    if existing_content:
        return jsonify({'error': 'Content already exists.'}), 400

    if(data['is_selected']):
        Profile.query.filter_by(section=data['section'], is_selected=True).update({'is_selected': False})

    new_profile = Profile(
        section=data['section'],
        content=data['content'],
        is_selected=data['is_selected'],
    )


    db.session.add(new_profile)
    db.session.commit()

    return jsonify({'message': 'Profile section added successfully', 'profile_id': new_profile.id}), 201


# Get Profile by Section Endpoint (GET request)
@app.route('/api/profiles/<section>', methods=['GET'])
def get_profiles_by_section(section):
    # Assuming 'section' is one of 'headline' or 'bio'
    if section not in ['headline', 'bio']:
        return jsonify({'error': 'Invalid section'}), 400

    profiles = Profile.query.filter_by(section=section).all()

    # You can customize the response format as needed
    profiles_data = [{'id': profile.id, 'content': profile.content, 'created_date': profile.created_date} for profile in profiles]

    return jsonify({'section': section, 'profiles': profiles_data})



if __name__ == '__main__':
    app.run(debug=True)

