from flask import Blueprint, request, redirect, session, url_for
from app.db import get_connection

comments_bp = Blueprint("comments", __name__)


@comments_bp.route("/create/<int:post_id>", methods=["POST"])
def create_comment(post_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    content = request.form["content"]

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO comments (post_id, user_id, content)
        VALUES (?, ?, ?)
        """,
        (post_id, session["user_id"], content)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("posts.feed"))