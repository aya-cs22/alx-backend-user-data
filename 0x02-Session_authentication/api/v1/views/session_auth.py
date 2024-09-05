#!/usr/bin/env python3
""" Module of Session authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /auth_session/login
    Return
        - Logged in user
    """
    email = request.form.get('email')

    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')

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
    session_id = auth.create_session(user.id)

    SESSION_NAME = getenv("SESSION_NAME")

    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /auth_session/logout
    Return:
        - Empty dictionary if succesful
    """
    from api.v1.app import auth

    deleted = auth.destroy_session(request)

    if not deleted:
        abort(404)

    return jsonify({}), 200
#!/usr/bin/env python3
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
#         return jsonify({"error": "email missing"}), 400
#     if not password:
#         return jsonify({"error": "password missing"}), 400
#     user = User.search(email=email)
#     if not user:
#         return jsonify({"error": "no user found for this email"}), 404
#     if not user.is_valid_password(password):
#         return jsonify({"error": "wrong password"}), 401
#     session_id = auth.create_session(user.id)
#     response = jsonify(user.to_json())
#     cookie_name = getenv('SESSION_NAME', '_my_session_id')
#     response.set_cookie(cookie_name, session_id)

#     return response