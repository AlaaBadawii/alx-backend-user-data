#!/usr/bin/env python3

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return None

    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))

        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv('SESSION_NAME'), session_id)
        return res

    return jsonify({"error": "wrong password"}), 401
