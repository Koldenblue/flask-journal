import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from sqlalchemy import create_engine, text
from helpers import apology, login_required, lookup, usd
from datetime import datetime
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine("sqlite+pysqlite:///journal.db", echo=True, future=True)

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS registrants"))
    conn.execute(text("CREATE TABLE 'registrants' ('id' INTEGER PRIMARY KEY, 'name' VARCHAR(255),'email' VARCHAR(255))"))
    conn.execute(text("INSERT INTO registrants (name, email) VALUES ('alice', 'a@a.com')"))
    conn.execute(text("INSERT INTO registrants (name, email) VALUES ('b', 'b@b.com')"))
    conn.commit()

@app.route('/')
#decorator defined in helpers.py
@login_required
def index():
    return render_template('index.html', rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = conn.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session['username'] = rows[0]['username']

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


#allowing for both get and post methods
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        #if post method, get the data posted by the form action
        name = request.form.get('name')
        email = request.form.get('email')
        if not name:
            return render_template('apology.html', message="Must provide name")
        elif not email:
            return render_template('apology.html', message="Must provide email")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        elif request.form.get('password-confirm') != request.form.get('password'):
            return apology("must confirm password", 403)

        else:
            username = request.form.get('username')
            password = generate_password_hash(request.form.get('password'))
            rows = db.execute("SELECT * FROM users")
            #make sure username doesn't already exist
            for row in rows:
                if username == row['username']:
                    return apology("that username already exists", 403)
        # insert into registrants table
        with engine.connect() as conn:
            conn.execute(text("INSERT INTO registrants (name, email, hash) VALUES (:name, :email, hash)"), [{"name": name, "email": email, "hash":password}])
            conn.commit()
            return render_template('/login.html')


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
