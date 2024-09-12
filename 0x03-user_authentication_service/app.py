#!/usr/bin/env python3
"""Flask app"""
from auth import Auth
from flask import (Flask,
                   jsonify,
                   request,
                   abort,
                   redirect)

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello_world() -> str:
    """Base route"""
    msg = {"message": "Bienvenue"}
    return jsonify(msg)

@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    Register new users
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})

# @app.route('/users', methods=['POST'])
# def users():
#     """POST /users endpoint to register a user"""
#     email = request.form.get('email')
#     password = request.form.get('password')
#     if not email or not password:
#         return jsonify({"message": "email and password are required"}), 400
#     try:
#         user = AUTH.register_user(email, password)
#         return jsonify({"email": user.email, "message": "user created"}), 201
#     except ValueError:
#         return jsonify({"message": "email already registered"}), 400
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
