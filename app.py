import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from sqlalchemy import create_engine, text, select
# make sure that these variables don't conflict
from sqlalchemy.orm import Session as alcSession
from flask_session import Session
from helpers import apology, login_required, lookup
from datetime import datetime
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine("sqlite+pysqlite:///journal.db", echo=True, future=True)

@app.route('/update', methods=["GET", "POST"])
# @login_required
def update():
    if request.method == "GET" and not request.args:
        return redirect('/')
    # For submitting an update to an entry
    if request.method == 'POST':
        with alcSession(engine) as conn:
            try:
                newentry = request.form.get('journal-entry')
                newmood = request.form.get('mood-select')
                id = request.args['id']
                # statement = text("UPDATE entries SET entry, mood WHERE id = :id AND username = :username").bindparams(id = id, username = session['username'])
                statement = text("UPDATE entries SET entry = :newentry, mood = :newmood WHERE id = :id AND username = :username").bindparams(id = id, username = '1', newentry = newentry, newmood = newmood)
                conn.execute(statement)
                conn.commit()
                return redirect('/')
            except:
                flash("Error updating entry!")
                return redirect('/')
    elif request.method == "GET":
        print('hello')
        print(request.method)
        with alcSession(engine) as conn:
            # Get mood totals:
            statement = text("SELECT mood FROM entries WHERE username = '1'")  # for easy testing, using username '1'
            # statement = text("SELECT mood FROM entries WHERE username = :username").bindparams(username = session['username']) 
            rows = conn.execute(statement)
            rows = rows.all()
            total_moods = {}
            for row in rows:
                total_moods.setdefault(row[0], 0)
                total_moods[row[0]] += 1
            # next get the entry that needs to be updated
            statement = text("SELECT entry, mood FROM entries WHERE id = :id;").bindparams(id = request.args['id'])
            rows = conn.execute(statement)
            rows = rows.all()
            entry = rows
            return render_template('update.html', moods=total_moods, entry=entry, id=request.args['id'])




@app.route('/')
#decorator defined in helpers.py
# @login_required
def index():
    with alcSession(engine) as conn:
        statement = text("SELECT mood FROM entries WHERE username = '1'")  # for easy testing, using username '1'
        # statement = text("SELECT mood FROM entries WHERE username = :username").bindparams(username = session['username']) 
        rows = conn.execute(statement)
        rows = rows.all()
        total_moods = {}
        for row in rows:
            total_moods.setdefault(row[0], 0)
            total_moods[row[0]] += 1
    return render_template('index.html', moods=total_moods)


@app.route('/allentries', methods=["GET", "DELETE"])
def all_entries():
    if request.method == "GET":
        with alcSession(engine) as conn:
            # statement = text("SELECT id, entry, mood, fDate FROM entries WHERE username = :username ORDER BY date DESC").bindparams(username = session['username'])
            statement = text("SELECT id, entry, mood, fDate FROM entries WHERE username = '1' ORDER BY date DESC") # for easy testing, using username '1'
            rows = conn.execute(statement)
            rows = rows.all()
            print(rows)
            return render_template('allentries.html', entries = rows)
    # delete request:
    else:
        # get the id of the entry to be deleted - the id is on the del button
        id = request.args['id']
        with alcSession(engine) as conn:
            statement = text("DELETE FROM entries WHERE id = :id").bindparams(id = id)
            conn.execute(statement)
            conn.commit()


            return render_template('allentries.html')


@app.route('/journal', methods=["GET", "POST"])
def journal():
    if request.method == "GET":
        return redirect('/')
    else:
        # get data from form and post to database
        entry = request.form.get('journal-entry')
        mood = request.form.get('mood-select').lower()
        date = datetime.now()
        fDate = date.strftime("%a %B %d, %Y")
        # username = session['username']
        if entry.strip() == '':
            flash("The journal entry is empty!")
            return redirect('/')
        with alcSession(engine) as conn:
            # statement = text("INSERT INTO entries (username, entry, mood, date, fDate) VALUES (:username, :entry, :mood, :date, :fDate);").bindparams(username = username, entry = entry, mood = mood, date = date, fDate = fDate)
            # for dev testing, username '1':
            statement = text("INSERT INTO entries (username, entry, mood, date, fDate) VALUES (:username, :entry, :mood, :date, :fDate);").bindparams(username = 1, entry = entry, mood = mood, date = date, fDate = fDate)
            conn.execute(statement)
            conn.commit()
            return redirect('/')



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

        with alcSession(engine) as conn:
            # Query database for username
            statement = text("SELECT * FROM registrants WHERE username = :username").bindparams(username= request.form.get("username"))
            rows = conn.execute(statement)

            # the cursor is forgotten the first time .all() is used, so set the variable to the rows.all() array
            rows = rows.all()

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
        username = request.form.get('username')
        password = request.form.get('password')
        if not username:
            return apology("Must provide username", 403)
        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)
        # elif len(password) < 6:
        #     return apology("Password must be at least 6 characters", 403)
        elif request.form.get('password-confirm') != request.form.get('password'):
            return apology("must confirm password", 403)
        else:
            username = request.form.get('username')
            password = generate_password_hash(password)
            # insert into registrants table
            with engine.connect() as conn:
                rows = conn.execute(text("SELECT username FROM registrants"))
                #make sure username doesn't already exist
                for row in rows.all():
                    if username == row['username']:
                        return apology("that username already exists", 403)
                conn.execute(text("INSERT INTO registrants (username, hash) VALUES (:username, :hash)"),
                                [{"username": username, "hash":password}])
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
