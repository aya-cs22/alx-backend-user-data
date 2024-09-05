#!/usr/bin/env python3
"""New view for Session Authentication"""
from flask import request, jsonify, abort
from models.user import User
from os import getenv
from api.v1.views import app_views

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handle user login and session creation"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        found_users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not found_users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in found_users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    user = found_users[0]
# @app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
# def login():
#     """Handle user login and session creation"""
#     email = request.form.get('email')
#     password = request.form.get('password')
#     if not email:
#         return jsonify({"error": "email missing"}), 400
#     if not password:
#         return jsonify({"error": "password missing"}), 400
#     try:
#         user = User.search({'email':email})
#     except Exception:
#         return jsonify({"error": "no user found for this email"}), 404
#     if not user:
#         return jsonify({"error": "no user found for this email"}), 404
#     for u in user:    
#         if not user.is_valid_password(password):
#             return jsonify({"error": "wrong password"}), 401
#     from api.v1.app import auth
#     u = user[0]

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    cookie_name = getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(cookie_name, session_id)

    return response