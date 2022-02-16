import email
import functools
import validators
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.constant.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from flaskr.model import db, User

auth = Blueprint('auth', __name__, url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    if username is None or len(username) < 5:
        return jsonify({'error': "Username is required also greater than 5 character"}), HTTP_400_BAD_REQUEST
    elif User.query.filter_by(username=username).first() is not None:
        jsonify({'error': "Username is already exist"}), HTTP_409_CONFLICT
    elif not username.isalnum() or " "in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST
    elif not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST
    elif User.query.filter_by(email=email).first() is not None:
        jsonify({'error': "Email is already exist"}), HTTP_409_CONFLICT
    elif len(password) < 5:
        return jsonify({'error': "Password is to short"}), HTTP_400_BAD_REQUEST
    
    hashed_pass = generate_password_hash(password)
    
    user = User(username=username, email=email, password = hashed_pass, is_superuser=True, is_admin = True, is_staff=True)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': "User created",
        'user': {
            'username':user.username, 'email':user.email
        }
    }), HTTP_201_CREATED