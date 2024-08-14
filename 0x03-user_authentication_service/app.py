#!/usr/bin/env python3
""" app module
"""
from flask import Flask, render_template, request, jsonify, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def message():
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


@app.route('/sessions', methods=['POST'])
def sessions():
    """ create a new session for the user,
    store it the session ID as a cookie with key
    """
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not pwd or not email:
        abort(401)
    auth_instance = Auth()
    if auth_instance.valid_login(email=email, password=pwd):
        session_id = auth_instance.create_session(email=email)
        if session_id:
            response = jsonify({"email": "<user email>", "message": "logged in"})
            response.set_cookie("session_id",session_id)
            return response
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
