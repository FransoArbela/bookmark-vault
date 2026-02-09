from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from utils import require_login
from bookmarks_seed import seed_user_bookmarks

bp = Blueprint("auth", __name__)

@bp.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    existing = db.execute("SELECT id FROM users WHERE username = ?", username)
    if existing:
        return jsonify({"error": "username already taken"}), 400

    password_hash = generate_password_hash(password, method="pbkdf2:sha256")
    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)

    # Get the newly created user
    new_user = db.execute("SELECT id FROM users WHERE username = ?", username)
    if new_user:
        user_id = new_user[0]["id"]
        # Automatically seed sample bookmarks for new users
        seed_user_bookmarks(user_id, db)

    return jsonify({"ok": True}), 201

@bp.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    # Check if user exists and password matches
    user_records = db.execute("SELECT id, hash FROM users WHERE username = ?", username)
    if not user_records or not check_password_hash(user_records[0]["hash"], password):
        return jsonify({"error": "invalid credentials"}), 401

    user_id = user_records[0]["id"]
    session["user_id"] = user_id
    user = db.execute("SELECT id, username FROM users WHERE id = ?", user_id)[0]
    return jsonify({"ok": True, "user": user}), 200

@bp.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"ok": True}), 200

@bp.get("/api/me")
def me():
    user_id = require_login()
    if not user_id:
        return jsonify({"user": None}), 200

    user = db.execute("SELECT id, username FROM users WHERE id = ?", user_id)[0]
    return jsonify({"user": user}), 200
