from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'exhibitors.db'

def get_db():
    """
    Returns a database connection using Flask's application context.
    Row factory is set so rows can be accessed as dictionaries.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # allows column access by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    """
    Closes the database connection when the application context ends.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    """
    The main route: fetch all exhibitors and render them in the template.
    """
    db = get_db()
    cur = db.execute("SELECT * FROM exhibitors")
    exhibitors = cur.fetchall()
    return render_template("index.html", exhibitors=exhibitors)

if __name__ == '__main__':
    app.run(debug=True)
