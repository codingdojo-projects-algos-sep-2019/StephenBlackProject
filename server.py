from flask import Flask, render_template, request, redirect, session, flash
from datetime import datetime
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
app.secret_key = 'Super Secret'
database = 'creations_db'
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

@app.route('/')
def signin():
    return render_template('index.html')

@app.route('/register', methods=["POST"])
def register_user():
    is_valid = True
    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("First Name must be at least 2 characters.")
    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Last Name must be at least 2 characters.")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!")
    if len(request.form['password']) < 8:
        is_valid = False
        flash("Password must be at least 8 characters.")
    if (request.form['password']) != request.form['c_password']:
        is_valid = False
        flash("Passwords do not match.")
    if is_valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password']) 
        mysql = connectToMySQL(database)
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(fn)s,%(ln)s,%(em)s,%(pw)s,NOW(),NOW());"
        data = {
            "fn": request.form['first_name'],
            "ln": request.form['last_name'],
            "em": request.form['email'],
            "pw": pw_hash
        }
        user_id = mysql.query_db(query,data)
        session['userid'] = user_id
        return redirect('/creations')
    else:
        return redirect('/')

@app.route('/login', methods=["POST"])
def login():
    is_valid = True
    if len(request.form['email']) < 2:
        is_valid = False
        flash("Please enter an email address")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!")
    if len(request.form['password']) < 2:
        is_valid = False
        flash("Please enter a password")
    if not is_valid:
        return redirect('/')
    else:
        mysql = connectToMySQL(database)
        query = "SELECT * FROM users WHERE email = %(em)s;"
        data  = {
            "em" : request.form["email"]
        }
        result = mysql.query_db(query, data)
        if result:
            if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
                session['userid'] = result[0]['user_id']
                return redirect('/creations')
        flash("Email or Password was incorrect")
        return redirect("/")

@app.route('/creations')
def creations():
    if 'userid' not in session:
        return redirect('/')
    
    mysql = connectToMySQL(database)
    query = "SELECT * FROM users WHERE user_id=%(id)s"
    data = {
        'id': session['userid']
    }
    users = mysql.query_db(query, data)

    mysql = connectToMySQL(database)
    query = "SELECT *, COUNT(users_likes_creations.creation_id) AS likes FROM creations JOIN users ON creations.user_id = users.user_id LEFT JOIN users_likes_creations ON creations.creation_id = users_likes_creations.creation_id GROUP BY creations.creation_id ORDER BY COUNT(likes) DESC;"
    
    creations = mysql.query_db(query, data)

    mysql = connectToMySQL(database)
    query = "SELECT * FROM creations WHERE user_id = %(uid)s;"
    data = {
        'uid' : session['userid']
    }
    has_creation = mysql.query_db(query,data)
    had_creations = []
    for owned in has_creation:
        had_creations.append(owned['creation_id'])
        
    return render_template('creations.html', users=users, creations=creations, had_creations = had_creations)

@app.route('/post_creation', methods=["POST"])
def commit_creation():
    if 'userid' not in session:
        return redirect('/')
    is_valid = True

    if len(request.form["creation_content"]) > 256:
        is_valid  =False
        flash ("Creationt cannot be longer than 255 characters")
    if len(request.form["creation_content"]) < 5:
        is_valid = False
        flash ("Creation cannot be shorter than 5 characters")
    if is_valid:
        mysql = connectToMySQL(database)
        query = "INSERT INTO creations (user_id, message, created_at, updated_at) VALUES (%(ui)s, %(me)s, NOW(), NOW());"
        data = {
            'ui': session['userid'],
            'me': request.form["creation_content"]
        }
        mysql.query_db(query, data)

    return redirect('/creations')

@app.route("/delete/<c_id>")
def delete_creation(c_id):
    if 'userid' not in session:
        return redirect('/')

    mysql = connectToMySQL(database)
    query = "DELETE FROM users_likes_creations WHERE creation_id = %(cid)s and user_id = %(uid)s;"
    data = {
        'cid' : c_id,
        'uid' : session['userid']
    }
    mysql.query_db(query, data)

    mysql = connectToMySQL(database)
    query = "DELETE FROM creations WHERE creation_id = %(cid)s and user_id = %(uid)s;"
    data = {
        'cid' : c_id,
        'uid' : session['userid']
    }
    mysql.query_db(query, data)

    return redirect ('/creations')

@app.route("/creations/<c_id>/details", methods=['POST'])
def details(c_id):
    if 'userid' not in session:
        return redirect('/')
    mysql = connectToMySQL(database)
    query = "SELECT * FROM creations LEFT JOIN users ON creations.user_id = users.user_id WHERE creation_id = %(cid)s;"
    data = {
        'cid' : c_id
    }
    ind_creations = mysql.query_db(query,data)

    mysql = connectToMySQL(database)
    query = "SELECT * FROM users_likes_creations LEFT JOIN users ON users_likes_creations.user_id = users.user_id WHERE creation_id = %(cid)s;"
    data = {
        'cid' : c_id
    }
    liked_users = mysql.query_db(query,data)

    mysql = connectToMySQL(database)
    query = "SELECT * FROM users_likes_creations WHERE user_id = %(uid)s;"
    data = {
        'uid' : session['userid']
    }
    is_liked = mysql.query_db(query,data)
    liked_creations = []
    for liked in is_liked:
        liked_creations.append(liked['creation_id'])
    
    return render_template('details.html', ind_creations = ind_creations, liked_users = liked_users, liked_creations = liked_creations)

@app.route("/like/<c_id>")
def like_creation(c_id):
    if 'userid' not in session:
        return redirect('/')
    mysql = connectToMySQL(database)
    query = "INSERT INTO users_likes_creations (user_id, creation_id, created_at, updated_at) VALUES (%(uid)s, %(cid)s, NOW(), NOW());"
    data = {
        'uid' : session['userid'],
        'cid' : c_id
    }
    mysql.query_db(query,data)

    return redirect('/creations')

@app.route("/unlike/<c_id>")
def unlike_creation(c_id):
    if 'userid' not in session:
        return redirect('/')
    mysql = connectToMySQL(database)
    query = "DELETE FROM users_likes_creations WHERE user_id = %(uid)s and creation_id = %(cid)s;"
    data = {
        'uid' : session['userid'],
        'cid' : c_id
    }
    mysql.query_db(query,data)

    return redirect('/creations')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)