from flask import request, jsonify, make_response
from app import bcrypt, api
from database import db
from flask_restful import fields, marshal, Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.model import User
from sqlalchemy.exc import SQLAlchemyError
import re


class Logiin(Resource):
    def post(self):

        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return make_response(jsonify({'message': 'Email and password are required!'}), 400)
            
            user = User.query.filter_by(email=email).first()
            if user:
                if bcrypt.check_password_hash(user.password, password):
                    access_token = create_access_token(identity=user.id)
                    return jsonify({'message': "Success! redirecting in 1sec..", 'access_token': access_token})
                else:
                    return(make_response(jsonify({'message': 'Incorrect Password!'}), 400))
            else:
                return(make_response(jsonify({'message': "User doesn't exists! Register First."}), 404))
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the session in case of an error
            return make_response(jsonify({'message': 'Database error occurred!'}), 500)
        except Exception as e:
            return make_response(jsonify({'message': 'An error occurred!'}), 500)   


    @jwt_required()
    def get(self):
        try:
            user_jwt = get_jwt_identity()
            user = User.query.filter_by(id=user_jwt).first()

            if user:
                return jsonify({'message': 'User found', 'name': user.name})
            else:
                return jsonify({'message': 'User not found'}), 404
        except Exception as e:
            return make_response(jsonify({'message': f'An error occurred: {str(e)}'}), 500)


class Register(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # Input validation
            if not username or not email or not password:
                return make_response(jsonify({'message': 'All fields are required!'}), 400)

            # Email format validation
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return make_response(jsonify({'message': 'Invalid email format!'}), 400)

            # Password strength validation (example: at least 3 characters)
            if len(password)  < 2:
                return make_response(jsonify({'message': 'Password must be at least 3 characters long!'}), 400)

            # Check if user already exists
            alr_user = User.query.filter_by(email=email).first()
            if alr_user:
                return make_response(jsonify({'message': 'Email Already Exists!'}), 400)

            # Hash the password using bcrypt
            pass_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            
            # Create new user
            user = User(name=username, email=email, password=pass_hash)
            db.session.add(user)
            db.session.commit()

            return jsonify({'message': 'Registered! You can log in 2sec....'})
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the session in case of an error
            return make_response(jsonify({'message': 'Database error occurred!'}), 500)
        except Exception as e:
            return make_response(jsonify({'message': 'An error occurred!'}), 500)
