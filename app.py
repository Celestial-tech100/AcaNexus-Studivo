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

    conn.commit()
    conn.close()
    print("Database and notes table created!")
    
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

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

@app.route("/assignments")
def assignments():
    return render_template("assignments.html")

@app.route("/expenses")
def expenses():
    return render_template("expenses.html")

if __name__ == "__main__":
    create_database()
    app.run(debug=True)