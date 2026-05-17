from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import bcrypt
import sqlite3
from app.db import get_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

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
            conn.close()

            flash ("Account created successfully", "success")
            return redirect(url_for("auth.login"))
        
        except sqlite3.IntegrityError:
            flash("Username already exists", "error")
            return redirect(url_for("auth.register"))
        
        finally:
            conn.close()
    
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

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