from flask import Blueprint, request, session, jsonify
from app.db import get_connection
from app import limiter

comments_bp = Blueprint("comments", __name__)


@comments_bp.route("/create/<int:post_id>", methods=["POST"])
@limiter.limit("10 per minute")
def create_comment(post_id):

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    content = request.form["content"].strip()

    if len(content) < 1 or len(content) > 300:
        return jsonify({"error": "Invalid length"}), 400

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO comments (post_id, user_id, content)
        VALUES (?, ?, ?)
        """,
        (post_id, session["user_id"], content)
    )

    conn.commit()

    comment = conn.execute(
        """
        SELECT comments.*, users.username
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.id = last_insert_rowid()
        """
    ).fetchone()

    conn.close()

    return jsonify({
        "username": comment["username"],
        "content": comment["content"],
        "created_at": comment["created_at"]
    })

@comments_bp.route("/more/<int:post_id>")
def load_more_comments(post_id):

    conn = get_connection()

    offset = request.args.get("offset", 0, type=int)
    limit = 5

    comments = conn.execute("""
        SELECT comments.*, users.username
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.post_id = ?
        ORDER BY comments.created_at DESC
        LIMIT ? OFFSET ?
    """, (post_id, limit, offset)).fetchall()

    conn.close()

    return jsonify([
        {
            "id": c["id"],
            "username": c["username"],
            "content": c["content"],
            "created_at": c["created_at"]
        }
        for c in comments
    ])