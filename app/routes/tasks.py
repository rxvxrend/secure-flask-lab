from flask import Blueprint, request, redirect, render_template, url_for
from app.db import get_connection

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route('/')
def index():
    conn = get_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)


@tasks_bp.route('/add', methods=['POST'])
def add():
    title = request.form['title']

    conn = get_connection()

    # ❌ (SQL-инъекция)
    conn.execute(
        "INSERT INTO tasks (title) VALUES (?)",
        (title,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("tasks.index"))