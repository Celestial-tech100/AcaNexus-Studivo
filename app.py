from flask import Flask, render_template , request , redirect 
import sqlite3

app = Flask(__name__)
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

    conn.commit()
    conn.close()
    print("Database and notes table created!")
    
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():

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

    conn.close()

    return render_template(
        "dashboard.html",
        total_notes=total_notes,
        pending_assignments=pending_assignments,
        completed_assignments=completed_assignments
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

    conn.close()

    return render_template(
        "assignments.html",
        assignments=assignments
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



@app.route("/expenses")
def expenses():
    return render_template("expenses.html")

if __name__ == "__main__":
    create_database()
    app.run(debug=True)