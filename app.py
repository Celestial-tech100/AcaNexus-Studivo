from flask import ( Flask, render_template , request , redirect ,session, url_for )
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
import sqlite3
from datetime import date

app = Flask(__name__)

app.secret_key = "acanexus_secret_key"

def create_database():

    conn = sqlite3.connect("database/acanexus.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        subject TEXT NOT NULL,
        due_date TEXT NOT NULL,
        status TEXT DEFAULT 'Pending'
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        expense_date TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("Database and tables created!")
    
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM notes")
    total_notes = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM assignments WHERE status='Pending'"
    )
    pending_assignments = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM assignments WHERE status='Completed'"
    )
    completed_assignments = cursor.fetchone()[0]
    total_assignments = (
    pending_assignments
    + completed_assignments
)
    today = date.today().isoformat()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM assignments
        WHERE status='Pending'
        AND due_date < ?
        """,
        (today,)
    )
    overdue_assignments = cursor.fetchone()[0]
    cursor.execute(
    "SELECT SUM(amount) FROM expenses"
    )
    total_expenses = cursor.fetchone()[0]
    cursor.execute(
    """
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    """
    )
    category_totals = cursor.fetchall()
    cursor.execute(
        "SELECT COUNT(*) FROM expenses"
    )

    expense_count = cursor.fetchone()[0]
    
    if total_expenses is None:
        total_expenses = 0
    productivity_score = min(
    (
        total_notes * 2
        + completed_assignments * 5
        + expense_count
    ),
    100
    )
    if total_assignments > 0:
        completion_percentage = int(
            (completed_assignments / total_assignments) * 100
        )
    else:
        completion_percentage = 0

    conn.close()

    return render_template(
    "dashboard.html",
    total_notes=total_notes,
    pending_assignments=pending_assignments,
    completed_assignments=completed_assignments,
    total_assignments=total_assignments,
    overdue_assignments=overdue_assignments,
    total_expenses=total_expenses,
    category_totals=category_totals,
    productivity_score=productivity_score,
    completion_percentage=completion_percentage
)

@app.route("/notes", methods=["GET", "POST"])
def notes():

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        cursor.execute(
            "INSERT INTO notes (title, content) VALUES (?, ?)",
            (title, content)
        )

        conn.commit()

    search = request.args.get("search")

    if search:

        cursor.execute(
            "SELECT * FROM notes WHERE title LIKE ?",
            ('%' + search + '%',)
        )

    else:

        cursor.execute("SELECT * FROM notes")

    notes = cursor.fetchall()

    conn.close()

    return render_template(
        "notes.html",
        notes=notes
    )
    
@app.route("/delete_note/<int:note_id>")
def delete_note(note_id):

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/notes")

@app.route("/edit_note/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        cursor.execute(
            """
            UPDATE notes
            SET title = ?, content = ?
            WHERE id = ?
            """,
            (title, content, note_id)
        )

        conn.commit()
        conn.close()

        return redirect("/notes")

    cursor.execute(
        "SELECT * FROM notes WHERE id = ?",
        (note_id,)
    )

    note = cursor.fetchone()
    conn.close()

    return render_template(
        "edit_note.html",
        note=note
    )

@app.route("/assignments", methods=["GET", "POST"])
def assignments():

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        subject = request.form["subject"]
        due_date = request.form["due_date"]

        cursor.execute(
            """
            INSERT INTO assignments
            (title, subject, due_date)
            VALUES (?, ?, ?)
            """,
            (title, subject, due_date)
        )

        conn.commit()

    cursor.execute("SELECT * FROM assignments")

    assignments = cursor.fetchall()

    today = date.today().isoformat()

    conn.close()

    return render_template(
        "assignments.html",
        assignments=assignments,
        today=today
    )

@app.route("/delete_assignment/<int:assignment_id>")
def delete_assignment(assignment_id):

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM assignments WHERE id = ?",
        (assignment_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/assignments")

@app.route("/complete_assignment/<int:assignment_id>")
def complete_assignment(assignment_id):

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE assignments
        SET status = 'Completed'
        WHERE id = ?
        """,
        (assignment_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/assignments")


@app.route("/expenses", methods=["GET", "POST"])
def expenses():

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        expense_date = request.form["expense_date"]

        cursor.execute(
            """
            INSERT INTO expenses
            (title, amount, category, expense_date)
            VALUES (?, ?, ?, ?)
            """,
            (title, amount, category, expense_date)
        )

        conn.commit()

    cursor.execute(
        "SELECT * FROM expenses ORDER BY expense_date DESC"
    )

    expenses = cursor.fetchall()
    cursor.execute(
    "SELECT SUM(amount) FROM expenses"
    )

    total_expense = cursor.fetchone()[0]

    if total_expense is None:
        total_expense = 0
        
    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    """)
    category_totals = cursor.fetchall()

    conn.close()

    return render_template(
        "expenses.html",
        expenses=expenses,
        total_expense=total_expense,
        category_totals=category_totals
    )

@app.route("/delete_expense/<int:expense_id>")
def delete_expense(expense_id):

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/expenses")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("database/acanexus.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users(username, email, password)
        VALUES (?, ?, ?)
        """,
        (username, email, hashed_password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("database/acanexus.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users(username, email, password)
        VALUES (?, ?, ?)
        """,
        (username, email, hashed_password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/expenses")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database/acanexus.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):

            session["user_id"] = user[0]
            session["username"] = user[1]

            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    create_database()
    app.run(debug=True)