from flask import Blueprint, redirect, session, url_for, jsonify
from app.db import get_connection

interaction_bp = Blueprint("interactions", __name__)


@interaction_bp.route("/like/<int:post_id>", methods=["POST"])
def like_post(post_id):

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    conn = get_connection()

    existing_like = conn.execute(
        """
        SELECT * FROM likes
        WHERE user_id = ? AND post_id = ?
        """,
        (session["user_id"], post_id)
    ).fetchone()

    liked = False

    if existing_like:

        conn.execute(
            """
            DELETE FROM likes
            WHERE user_id = ? AND post_id = ?
            """,
            (session["user_id"], post_id)
        )

    else:

        conn.execute(
            """
            INSERT INTO likes (user_id, post_id)
            VALUES (?, ?)
            """,
            (session["user_id"], post_id)
        )

        liked = True

    conn.commit()

    likes_count = conn.execute(
        """
        SELECT COUNT(*) as count
        FROM likes
        WHERE post_id = ?
        """,
        (post_id,)
    ).fetchone()["count"]

    conn.close()

    return jsonify({
        "liked": liked,
        "likes_count": likes_count
    })