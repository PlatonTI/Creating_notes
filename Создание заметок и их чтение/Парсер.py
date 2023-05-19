from flask import Flask, render_template, request, redirect, url_for
import sqlite3

conn = sqlite3.connect("notes.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)")
conn.commit()
conn.close()

def get_notes():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()
    return notes

def add_note(title, content):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

def delete_note(id):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()

app = Flask(__name__)

@app.route("/")
def index():
    notes = get_notes()
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    content = request.form["content"]
    add_note(title, content)
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    delete_note(id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
