from flask import Blueprint, render_template, request, redirect, url_for, session
from app.db import get_connection
from app import limiter

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/")
def feed():

    conn = get_connection()
    user_id = session.get("user_id")

    page = request.args.get("page", 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    posts_raw = conn.execute("""
        SELECT posts.*, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.created_at DESC
        LIMIT ? OFFSET ?
    """, (per_page, offset)).fetchall()

    total_posts = conn.execute("SELECT COUNT(*) as count FROM posts").fetchone()["count"]

    comments_raw = conn.execute("""
        SELECT comments.*, users.username
        FROM comments
        JOIN users ON comments.user_id = users.id
        ORDER BY created_at DESC
    """).fetchall()

    comments_map = {}

    for c in comments_raw:
        comments_map.setdefault(c["post_id"], []).append(dict(c))

    likes_raw = conn.execute("""
        SELECT post_id, COUNT(*) as count
        FROM likes
        GROUP BY post_id
    """).fetchall()

    likes_map = {
        like["post_id"]: like["count"]
        for like in likes_raw
    }

    posts = []

    for post in posts_raw:
        post_dict = dict(post)

        post_dict["likes_count"] = likes_map.get(post_dict["id"], 0)

        if user_id:
            like = conn.execute(
                """
                SELECT 1 FROM likes
                WHERE user_id = ? AND post_id = ?
                """,
                (user_id, post_dict["id"])
            ).fetchone()

            post_dict["liked_by_user"] = bool(like)
        else:
            post_dict["liked_by_user"] = False

        posts.append(post_dict)

    conn.close()

    return render_template(
        "feed.html",
        posts=posts,
        comments_map=comments_map,
        page=page,
        has_next=(page * per_page < total_posts),
        has_prev=(page > 1)
    )

@posts_bp.route("/create", methods=["POST"])
@limiter.limit("5 per minute")
def create_post():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    content = request.form["content"]

    conn = get_connection()
    conn.execute(
        "INSERT INTO posts (user_id, content) VALUES (?, ?)",
        (session["user_id"], content)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("posts.feed"))