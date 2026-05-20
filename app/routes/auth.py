from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import bcrypt
import sqlite3
from app.db import get_connection
from app import limiter

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def register():
    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        if len(username) < 3 or len(username) > 30:
            flash("Username must be 3-30 characters", "error")
            return redirect(url_for("auth.register"))
        
        if len(password) < 6 or len(password) > 100:
            flash("Password must be 6-100 characters", "error")
            return redirect(url_for("auth.register"))

        password_hash = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )

        conn = get_connection()

        try:

            conn.execute(
                """
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
                """,
                (username, password_hash)
            )
            conn.commit()

            flash ("Account created successfully", "success")
            return redirect(url_for("auth.login"))
        
        except sqlite3.IntegrityError:
            flash("Username already exists", "error")
            return redirect(url_for("auth.register"))
        
        finally:
            conn.close()
    
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            flash("Empty fields not allowed", "error")
            return redirect(url_for("auth.login"))

        conn = get_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode(), user["password_hash"]):

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            flash("Logged in successfuly", "success")
            return redirect(url_for("posts.feed"))
        
        flash("Invalid username or password", "error")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()

    flash("Logged out successfully", "success")
    return redirect(url_for("auth.login"))