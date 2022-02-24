from ast import Not
import validators
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, JWTManager
from flaskr.constant.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from flaskr.model import db, User, TokenBlocklist

auth = Blueprint('auth', __name__, url_prefix="/api/v1/auth")

jwt = JWTManager()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

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
    
    user = User(username=username, email=email, password = hashed_pass, is_staff=True, is_admin=True)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': "User created",
        'user': {
            'username':user.username, 'email':user.email
        }
    }), HTTP_201_CREATED
    
@auth.post('/login')
def login():
    username = request.json['username']
    password = request.json['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user is None:
        return jsonify({'msg': "email or password is invalid"}), HTTP_400_BAD_REQUEST
    
    if user.is_admin == True:
        validate_password = check_password_hash(user.password, password)
        
        if validate_password:
            access_token = create_access_token(identity=user.username, fresh=True)
            refresh_token = create_refresh_token(identity=user.username)
            return jsonify({
                "user": {
                    'access_token':access_token,
                    'refresh_token': refresh_token,
                    'info':{
                        'username': user.username,
                        'email': user.email
                    }
                    
                }
            }), HTTP_200_OK
    else:
        return jsonify({
            "error": "Sorry You are not admin"
        })
        
@auth.route("/logout", methods=["DELETE"])
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(msg="JWT revoked")

        
@auth.post('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity=get_jwt_identity()
    access = create_access_token(identity=identity)
    
    return jsonify({
        'access':access
    }), HTTP_200_OK
        
@auth.get('/<int:id>')
@jwt_required()
def get_user(id):
    current_user = get_jwt_identity()
    
    user = User.query.filter_by(id=id).first()
    
    if user is None:
        return jsonify({'msg': "email or password is invalid"}), HTTP_400_BAD_REQUEST
    if user.username == current_user:
    
        return jsonify({
            'username':user.username,
            'email':user.email
        })
    else:
        return jsonify({
            'error':"You are not authenticate"
        })
        

    