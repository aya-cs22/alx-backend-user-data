#!/usr/bin/env python3
"""Flask app"""
from auth import Auth
from flask import (Flask,
                   jsonify,
                   request,
                   abort,
                   make_response)

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello_world() -> str:
    """Base route"""
    msg = {"message": "Bienvenue"}
    return jsonify(msg)


@app.route('/users', methods=['POST'])
def users():
    """POST /users endpoint to register a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    # if not email or not password:
    #     return jsonify({"message": "email and password are required"}), 400
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'])
def login():
    """Handles login and session creation"""
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not AUTH.valid_login(email, password):
        abort(401)
    
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
