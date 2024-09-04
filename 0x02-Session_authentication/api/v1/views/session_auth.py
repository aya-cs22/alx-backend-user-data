#!/usr/bin/env python3
"""New view for Session Authentication"""
from flask import Blueprint, request, jsonify
from os import getenv
from api.v1.app import auth
from models.user import User

session_auth = Blueprint('session_auth', __name__)

@session_auth.route('/auth_session/login', methods=['POST'])
def login():
    """Handle user login and session creation"""
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Validate password
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve User instance based on email
    user = User.search(email=email)
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    # Validate password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a Session ID
    session_id = auth.create_session(user.id)

    # Prepare the response
    response = jsonify(user.to_json())
    cookie_name = getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(cookie_name, session_id)

    return response

# #!/usr/bin/env python3
# """New view for Session Authentication"""
# from flask import Blueprint, request, jsonify, make_response
# import json
# from os import getenv
# from api.v1.app import auth
# from models.user import User
# session_auth = Blueprint('session_auth', __name__)
# @session_auth.route('/auth_session/login', methods=['POST'])
# def login():
#     """Handle user login and session creation"""
#     email = request.form.get('email')
#     password = request.form.get('password')
#     if not email:
#         return jsonify({ "error": "email missing" }), 400
#     if not password:
#         return jsonify({ "error": "password missing" }), 400
#     user = User.search(email=email)
#     if not user:
#         return jsonify({ "error": "no user found for this email" }), 404
#     if not user.is_valid_password(password):
#         return jsonify({ "error": "wrong password" }), 401
#     session_id = auth.create_session(user.id)
#     response = jsonify(user.to_json())
#     cookie_name = getenv('SESSION_NAME', '_my_session_id')
#     response.set_cookie(cookie_name, session_id)
    
#     return response