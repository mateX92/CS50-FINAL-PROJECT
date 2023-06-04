from flask import Flask # Call flask class
from flask import session, render_template, redirect, url_for, request
import key # another .py file
from helpers import lookup, login_required
import sqlite3

app = Flask(__name__)
app.secret_key = key.SECRET_KEY

# Connect to SQL db - to be moved out of index
db_con = sqlite3.connect('users.db', check_same_thread=False)
db = db_con.cursor()

# Tell flask what URL should trigger functions
@app.route("/")
def index():
# @login_required
    dbTest = db.execute("SELECT * from users")
    print(db.fetchall())

    if session:
        print("Success")
        logout = "Log Out"
        return render_template('index.html', logout=logout)
    else:
        print(session)
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
# @login_required
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register'):
def register():
    # TO DO: create html, add users to users.db, make sure to check if the user exists (copy from finance?), hash password (finance?)
    return render_template('register.html')


if __name__ == "__main__":
    app.run()


# Here you need to get the DB table, not sure how yet, to query from it for your search.
@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        title = request.form.get('movieTitle')
        movieArray = lookup(title)
        return render_template('search.html', movies=movieArray)
    elif request.method == "GET":        
        return render_template('search.html')


# FOR SESSION
# We have HTML layout where there is navbar with regular links - perhaps it is better for layout to only refer to logged in user?

# For logged out user, we should only have LOG IN, REGISTER and HOME navbar buttons

# FOR LOGGING IN - check session object once you provide user data from HTML
# Later, in sqlite, create a db that stores user's data to keep it further on
# Check with CHAT GPT about primary key and foreign key - will be useful later to connect users to interests