#!/usr/bin/env python3
""" app module
"""
from flask import Flask, render_template, request, jsonify
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
