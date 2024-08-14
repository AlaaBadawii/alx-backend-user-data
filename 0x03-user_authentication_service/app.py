#!/usr/bin/env python3
""" app module
"""
from flask import (Flask, render_template, request,
                   jsonify, abort, redirect, url_for)
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register():
    email = request.form.get("email")
    password = request.form.get("password")

    auth_instance = Auth()

    try:
        user = auth_instance.register_user(email, password)
        return jsonify({"email": f"{user.email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /sessions
    Return:
        - The account login payload.
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """ Logout 
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    Auth.destroy_session(user.id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
