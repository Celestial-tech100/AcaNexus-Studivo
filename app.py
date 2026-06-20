from flask import Flask, render_template, request, redirect, session, url_for

from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "acanexus_secret_key"


# ================= DATABASE =================
def create_database():
    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        content TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        subject TEXT,
        due_date TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        amount REAL,
        category TEXT,
        expense_date TEXT
    )
    """)
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    full_name TEXT,
    university TEXT,
    course TEXT,
    branch TEXT,
    year TEXT,
    semester TEXT,
    bio TEXT
)
""")

    conn.commit()
    conn.close()


# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")

# ================= PROFILE  =================
@app.route("/profile", methods=["GET", "POST"])
def profile():

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    user_id = session["user_id"]
    saved = False

    if request.method == "POST":
        full_name = request.form["full_name"]
        university = request.form["university"]
        course = request.form["course"]
        branch = request.form["branch"]
        year = request.form["year"]
        semester = request.form["semester"]
        session_value = request.form["session"]
        bio = request.form["bio"]

        cursor.execute("""
        UPDATE profiles
        SET full_name = ?,
            university = ?,
            course = ?,
            branch = ?,
            year = ?,
            semester = ?,
            session = ?,
            bio = ?
        WHERE user_id = ?
        """, (
            full_name,
            university,
            course,
            branch,
            year,
            semester,
            session_value,
            bio,
            user_id
        ))

        conn.commit()
        saved = True

    cursor.execute("""
        SELECT *
        FROM profiles
        WHERE user_id=?
    """, (user_id,))

    profile = cursor.fetchone()

    conn.close()

    return render_template("profile.html", profile=profile, saved=saved)

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    uid = session["user_id"]

    cursor.execute("SELECT COUNT(*) FROM notes WHERE user_id=?", (uid,))
    total_notes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM assignments WHERE user_id=? AND status='Pending'", (uid,))
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM assignments WHERE user_id=? AND status='Completed'", (uid,))
    completed = cursor.fetchone()[0]

    total_assignments = pending + completed

    today = date.today().isoformat()

    cursor.execute("""
        SELECT COUNT(*) FROM assignments
        WHERE user_id=? AND status='Pending' AND due_date < ?
    """, (uid, today))
    overdue = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id=?", (uid,))
    total_expenses = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id=?
        GROUP BY category
    """, (uid,))
    category_totals = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM expenses WHERE user_id=?", (uid,))
    expense_count = cursor.fetchone()[0]

    productivity_score = min(
        total_notes * 2 + completed * 5 + expense_count,
        100
    )

    completion_percentage = int((completed / total_assignments) * 100) if total_assignments else 0

    conn.close()

    return render_template(
        "dashboard.html",
        total_notes=total_notes,
        pending_assignments=pending,
        completed_assignments=completed,
        total_assignments=total_assignments,
        overdue_assignments=overdue,
        total_expenses=total_expenses,
        category_totals=category_totals,
        productivity_score=productivity_score,
        completion_percentage=completion_percentage
    )


# ================= NOTES =================
@app.route("/notes", methods=["GET", "POST"])
def notes():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()
    uid = session["user_id"]

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        cursor.execute("""
            INSERT INTO notes (user_id, title, content)
            VALUES (?, ?, ?)
        """, (uid, title, content))

        conn.commit()
        conn.close()
        return redirect("/notes")

    search = request.args.get("search")

    if search:
        cursor.execute("""
            SELECT * FROM notes
            WHERE user_id=? AND title LIKE ?
        """, (uid, f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM notes WHERE user_id=?", (uid,))

    notes_data = cursor.fetchall()
    conn.close()

    return render_template("notes.html", notes=notes_data)

# ================= EDIT NOTE =================

@app.route("/edit_note/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        cursor.execute("""
            UPDATE notes
            SET title=?, content=?
            WHERE id=? AND user_id=?
        """, (title, content, note_id, session["user_id"]))

        conn.commit()
        conn.close()

        return redirect(url_for("notes"))

    cursor.execute("""
        SELECT *
        FROM notes
        WHERE id=? AND user_id=?
    """, (note_id, session["user_id"]))

    note = cursor.fetchone()

    conn.close()

    return render_template("edit_note.html", note=note)


# ================= DELETE NOTE =================
@app.route("/delete_note/<int:note_id>")
def delete_note(note_id):

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM notes WHERE id=? AND user_id=?
    """, (note_id, session["user_id"]))

    conn.commit()
    conn.close()

    return redirect("/notes")


# ================= ASSIGNMENTS =================
@app.route("/assignments", methods=["GET", "POST"])
def assignments():
    print("ROUTE HIT:", request.method)

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()
    uid = session["user_id"]

    if request.method == "POST":
        title = request.form["title"]
        subject = request.form["subject"]
        due_date = request.form["due_date"]

        cursor.execute("""
            INSERT INTO assignments (user_id, title, subject, due_date, status)
            VALUES (?, ?, ?, ?, 'Pending')
        """, (uid, title, subject, due_date))

        conn.commit()
        conn.close()
        return redirect(url_for("assignments"))

    cursor.execute("""
    SELECT id, title, subject, due_date, status
    FROM assignments
    WHERE user_id=?
""", (session["user_id"],))

    assignments_data = cursor.fetchall()
    conn.close()

    today = date.today().isoformat()

    return render_template(
        "assignments.html",
        assignments=assignments_data,
        today=today
    )


# ================= COMPLETE =================
@app.route("/complete_assignment/<int:assignment_id>")
def complete_assignment(assignment_id):

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE assignments
        SET status='Completed'
        WHERE id=? AND user_id=?
    """, (assignment_id, session.get("user_id")))

    conn.commit()
    conn.close()

    return redirect(url_for("assignments"))

# ================= DELETE ASSIGNMENT =================
@app.route("/delete_assignment/<int:assignment_id>")
def delete_assignment(assignment_id):

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM assignments
        WHERE id=? AND user_id=?
    """, (assignment_id, session.get("user_id")))

    conn.commit()
    conn.close()

    return redirect(url_for("assignments"))


# ================= EXPENSES =================
@app.route("/expenses", methods=["GET", "POST"])
def expenses():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()
    uid = session["user_id"]

    if request.method == "POST":
        cursor.execute("""
            INSERT INTO expenses (user_id, title, amount, category, expense_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            uid,
            request.form["title"],
            request.form["amount"],
            request.form["category"],
            request.form["expense_date"]
        ))

        conn.commit()
        conn.close()
        return redirect("/expenses")

    cursor.execute("SELECT * FROM expenses WHERE user_id=?", (uid,))
    expenses_data = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id=?", (uid,))
    total = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id=?
        GROUP BY category
    """, (uid,))
    category_totals = cursor.fetchall()

    conn.close()

    return render_template(
        "expenses.html",
        expenses=expenses_data,
        total_expense=total,
        category_totals=category_totals
    )

# ================= DELETE EXPENSE =================

@app.route("/delete_expense/<int:expense_id>")
def delete_expense(expense_id):

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id=? AND user_id=?
    """, (expense_id, session.get("user_id")))

    conn.commit()
    conn.close()

    return redirect(url_for("expenses"))

# ================= AUTH =================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("database/acanexus.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        """, (username, email, password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database/acanexus.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/dashboard")

    return render_template("login.html")

# ================= LOGOUT  =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= CALENDAR =================
import calendar as cal
from datetime import datetime


@app.route("/calendar")
def calendar():

    if "user_id" not in session:
        return redirect("/login")

    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)

    today = datetime.now()

    today_day = today.day
    today_month = today.month
    today_year = today.year

    if not month:
        month = today.month

    if not year:
        year = today.year

    month_name = cal.month_name[month]

    calendar_days = cal.monthcalendar(year, month)

    prev_month = month - 1
    prev_year = year

    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    next_month = month + 1
    next_year = year

    if next_month == 13:
        next_month = 1
        next_year += 1

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id,
           title,
           event_type,
           event_date
    FROM calendar_events
    WHERE user_id = ?
    ORDER BY event_date
""", (session["user_id"],))

    rows = cursor.fetchall()

    events = {}

    for event_id, title, event_type, event_date in rows:

        if event_date not in events:
            events[event_date] = []

        events[event_date].append({
            "id": event_id,
            "title": title,
            "type": event_type
        })

    conn.close()

    return render_template(
        "calendar.html",
        calendar_days=calendar_days,
        month=month,
        year=year,
        month_name=month_name,
        prev_month=prev_month,
        prev_year=prev_year,
        next_month=next_month,
        next_year=next_year,
        today_day=today_day,
        today_month=today_month,
        today_year=today_year,
        events=events
    )

# ================= Add-Event  =================
@app.route("/add-event", methods=["POST"])
def add_event():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    title = request.form["title"]
    event_date = request.form["event_date"]
    event_type = request.form["event_type"]

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO calendar_events
        (user_id, title, event_type, event_date)
        VALUES (?, ?, ?, ?)
    """, (user_id, title, event_type, event_date))

    conn.commit()
    conn.close()

    return redirect("/calendar")

# ================= DELETE EVENT =================
@app.route("/delete-event/<int:event_id>", methods=["POST"])
def delete_event(event_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM calendar_events
        WHERE id = ?
        AND user_id = ?
    """, (event_id, session["user_id"]))

    conn.commit()
    conn.close()

    return redirect("/calendar")

# ================= EDIT EVENT =================
@app.route("/edit-event/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        event_date = request.form["event_date"]
        event_type = request.form["event_type"]

        cursor.execute("""
            UPDATE calendar_events
            SET title = ?,
                event_type = ?,
                event_date = ?
            WHERE id = ?
            AND user_id = ?
        """, (
            title,
            event_type,
            event_date,
            event_id,
            session["user_id"]
        ))

        conn.commit()
        conn.close()

        return redirect("/calendar")

    cursor.execute("""
        SELECT id,
               title,
               event_type,
               event_date
        FROM calendar_events
        WHERE id = ?
        AND user_id = ?
    """, (
        event_id,
        session["user_id"]
    ))

    event = cursor.fetchone()

    conn.close()

    if not event:
        return redirect("/calendar")

    return render_template(
        "edit_event.html",
        event=event
    )

# ================= ATTENDANCE =================
@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    conn = sqlite3.connect("database/acanexus.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    user_id = session["user_id"]

    if request.method == "POST":

        subject = request.form["subject"]
        total = request.form["total"]
        attended = request.form["attended"]

        cursor.execute("""
            INSERT INTO attendance
            (user_id, subject, attended, total)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            subject,
            attended,
            total
        ))

        conn.commit()

    cursor.execute("""
        SELECT *
        FROM attendance
        WHERE user_id = ?
        ORDER BY subject
    """, (user_id,))

    subjects = cursor.fetchall()

    conn.close()

    return render_template(
        "attendance.html",
        subjects=subjects
    )

# ================= SETTINGS =================
@app.route("/settings", methods=["GET", "POST"])
def settings():

    conn = sqlite3.connect("database/acanexus.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    user_id = session["user_id"]
    saved = False
    password_message = None

    if request.method == "POST":

        form_type = request.form.get("form_type")

        if form_type == "profile":
                full_name = request.form["full_name"]
                university = request.form["university"]
                course = request.form["course"]
                branch = request.form["branch"]
                year = request.form["year"]
                semester = request.form["semester"]
                session_value = request.form["session"]
                bio = request.form["bio"]

                cursor.execute("""
                    UPDATE profiles
                    SET
                        full_name = ?,
                        university = ?,
                        course = ?,
                        branch = ?,
                        year = ?,
                        semester = ?,
                        session = ?,
                        bio = ?
                    WHERE user_id = ?
                """, (
                    full_name,
                    university,
                    course,
                    branch,
                    year,
                    semester,
                    session_value,
                    bio,
                    user_id
                ))

                conn.commit()
                
                saved = True
                
        elif form_type == "password":

            current_password = request.form["current_password"]
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]

            cursor.execute("""
                SELECT password
                FROM users
                WHERE id = ?
            """, (user_id,))

            user = cursor.fetchone()

            if not check_password_hash(
                user["password"],
                current_password
            ):

                password_message = "❌ Current password is incorrect."

            elif new_password != confirm_password:

                password_message = "❌ New passwords do not match."

            else:

                new_hash = generate_password_hash(
                    new_password
                )

                cursor.execute("""
                    UPDATE users
                    SET password = ?
                    WHERE id = ?
                """, (
                    new_hash,
                    user_id
                ))

                conn.commit()

                password_message = "✅ Password changed successfully."
                
        elif form_type == "email":

            new_email = request.form["new_email"]

            cursor.execute("""
                UPDATE users
                SET email = ?
                WHERE id = ?
            """, (
                new_email,
                user_id
            ))

            conn.commit()

    cursor.execute("""
            SELECT *
            FROM profiles
            WHERE user_id = ?
        """, (user_id,))

    profile = cursor.fetchone()
    
    cursor.execute("""
        SELECT email
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return render_template(
        "settings.html",
        profile=profile,
        user=user,
        saved=saved,
        password_message=password_message
    )

# ================= DELETE ACCOUNT  =================
@app.route("/delete_account", methods=["POST"])
def delete_account():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("database/acanexus.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()

    session.clear()

    return redirect("/register")



# ================= RUN =================
if __name__ == "__main__":
    create_database()
    app.run(debug=True)