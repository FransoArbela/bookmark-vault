from flask import Blueprint, jsonify, request, session

from db import db
from utils import require_login

bp = Blueprint("bookmarks", __name__)


@bp.get("/api/bookmarks")
def list_bookmarks():
    user_id = require_login()
    if not user_id:
        return jsonify({"error": "not logged in"}), 401

    search_query = (request.args.get("query") or "").strip()

    if search_query:
        # Search across all bookmark fields
        like_pattern = f"%{search_query}%"
        bookmarks = db.execute(
            """
            SELECT id, title, url, tags, note, is_favorite, created_at
            FROM bookmarks
            WHERE user_id = ?
              AND (title LIKE ? OR url LIKE ? OR tags LIKE ? OR note LIKE ?)
            ORDER BY is_favorite DESC, created_at DESC
            """,
            user_id,
            like_pattern,
            like_pattern,
            like_pattern,
            like_pattern,
        )
    else:
        bookmarks = db.execute(
            """
            SELECT id, title, url, tags, note, is_favorite, created_at
            FROM bookmarks
            WHERE user_id = ?
            ORDER BY is_favorite DESC, created_at DESC
            """,
            user_id,
        )

    return jsonify({"bookmarks": bookmarks}), 200


@bp.post("/api/bookmarks")
def create_bookmark():
    user_id = require_login()
    if not user_id:
        return jsonify({"error": "not logged in"}), 401

    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    url = (data.get("url") or "").strip()
    tags = (data.get("tags") or "").strip()
    note = (data.get("note") or "").strip()

    if not title:
        return jsonify({"error": "title required"}), 400
    if not url:
        return jsonify({"error": "url required"}), 400

    db.execute(
        """
        INSERT INTO bookmarks (user_id, title, url, tags, note)
        VALUES (?, ?, ?, ?, ?)
        """,
        user_id,
        title,
        url,
        tags,
        note,
    )

    return jsonify({"ok": True}), 201


@bp.put("/api/bookmarks/<int:bookmark_id>")
def update_bookmark(bookmark_id: int):
    user_id = require_login()
    if not user_id:
        return jsonify({"error": "not logged in"}), 401

    existing = db.execute(
        "SELECT id FROM bookmarks WHERE id = ? AND user_id = ?",
        bookmark_id,
        user_id,
    )
    if not existing:
        return jsonify({"error": "not found"}), 404

    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    url = (data.get("url") or "").strip()
    tags = (data.get("tags") or "").strip()
    note = (data.get("note") or "").strip()

    if not title or not url:
        return jsonify({"error": "title and url required"}), 400

    db.execute(
        """
        UPDATE bookmarks
        SET title = ?, url = ?, tags = ?, note = ?
        WHERE id = ? AND user_id = ?
        """,
        title,
        url,
        tags,
        note,
        bookmark_id,
        user_id,
    )

    return jsonify({"ok": True}), 200


@bp.delete("/api/bookmarks/<int:bookmark_id>")
def delete_bookmark(bookmark_id: int):
    user_id = require_login()
    if not user_id:
        return jsonify({"error": "not logged in"}), 401

    db.execute(
        "DELETE FROM bookmarks WHERE id = ? AND user_id = ?",
        bookmark_id,
        user_id,
    )
    return jsonify({"ok": True}), 200


@bp.patch("/api/bookmarks/<int:bookmark_id>/favorite")
def toggle_favorite(bookmark_id: int):
    user_id = require_login()
    if not user_id:
        return jsonify({"error": "not logged in"}), 401

    bookmark_record = db.execute(
        "SELECT is_favorite FROM bookmarks WHERE id = ? AND user_id = ?",
        bookmark_id,
        user_id,
    )
    if not bookmark_record:
        return jsonify({"error": "not found"}), 404

    # SQLite stores booleans as INTEGER (0 or 1), so we toggle between them
    current_favorite = int(bookmark_record[0]["is_favorite"])
    new_favorite = 0 if current_favorite == 1 else 1

    db.execute(
        "UPDATE bookmarks SET is_favorite = ? WHERE id = ? AND user_id = ?",
        new_favorite,
        bookmark_id,
        user_id,
    )

    return jsonify({"ok": True, "is_favorite": new_favorite}), 200
