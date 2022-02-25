from crypt import methods
import validators
from werkzeug.security import generate_password_hash
from flask import Blueprint, jsonify, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flaskr.constant.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from flaskr.model import Position, User, db
from flask_cors import CORS

dashboard = Blueprint('dashboard', __name__, url_prefix='/api/v1/dashboard')
CORS(dashboard)
@dashboard.get('/')
def home():

    return jsonify({
        'msg':'This is dashboard'
    }), HTTP_200_OK

@dashboard.route('/staff', methods=['GET', 'POST'])
@jwt_required()
def users():
    
    if request.method == 'POST':
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
        
        user = User(username=username, email=email, password = hashed_pass, is_staff=True)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': "User created",
            'user': {
                'username':user.username, 'email':user.email
            }
        }), HTTP_201_CREATED
    else:
        users = User.query.all()
        
        data= []
        
        for user in users:
            data.append({
                'id':user.id,
                'username':user.username,
                'email': user.email
            })
            
        return jsonify({'data':data}), HTTP_200_OK
    
@dashboard.get('/staff/<int:id>')
@jwt_required()
def get_user(id):
    current_user = get_jwt_identity()
    
    user = User.query.filter_by(id=id).first()
    
    if user is None:
        return jsonify({'msg': "email or password is invalid"}), HTTP_400_BAD_REQUEST
    
    else:
        return jsonify({
            'username':user.username,
            'email':user.email
        })
@dashboard.put('/staff/<int:id>')
@dashboard.patch('/staff/<int:id>')
def edit_user(id):
    
    username = request.json['username']
    email = request.json['email']
    
    user = User.query.filter_by(id=id).first()
    
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
        
        
    user.username = username
    user.email = email
    
    db.session.commit()
    
    return jsonify({
            'username':user.username,
            'email':user.email
        }), HTTP_201_CREATED
    


@dashboard.delete('/staff/<int:id>')
@jwt_required()
def delete_staff(id):
    current_user = get_jwt_identity()
    
    user = User.query.filter_by(id=id).first()
    
    if user.id == current_user:
        return jsonify({
            'msg': "Lol, You can not delete your self"
        })
    else:
        
        db.session.delete(user)
        db.session.commit()
            
        return jsonify({
            'msg':"User has been delete"
        })
    

@dashboard.route('/position', methods=["GET", "POST"])
@jwt_required()
def position():
    if request.method == 'POST':
        name = request.get_json().get('name', '')
        
        if len(name) < 3:
            return jsonify({'error': 'Position name should not empty'}), HTTP_400_BAD_REQUEST
        
        if Position.query.filter_by(name=name).first():
            return jsonify({'error': 'Position name already exist'})
        
        position = Position(name=name)
        
        db.session.add(position)
        db.session.commit()
        
        return jsonify({
            'name':position.name,
            'slug':position.slug
        })
    else:
        data_positions = Position.query.all()
        
        position = []
        
        for d in data_positions:
            position.append({
                'id': d.id,
                'name': d.name,
                'slug': d.slug,
            })
        
        return jsonify({'position':position})
    
@dashboard.route('/position/<int:id>', methods=["GET", "DELETE"])
@jwt_required()
def position_get_or_delete(id):
    
    if request.method == 'DELETE':
        postiton = Position.query.filter_by(id=id).first()
        
        db.session.delete(postiton)
        db.session.commit()
            
        return jsonify({
            'msg':"Item has been delete"
        })

    else:
        postiton = Position.query.filter_by(id=id).first()
        if postiton is None:
            return jsonify({
                'msg': "That position is not exist"
            })
        
        return jsonify({
            'id': postiton.id,
            'name':postiton.name,
            'slug':postiton.slug
        })