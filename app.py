# Import dependencies
from flask import Flask, render_template, request, session, redirect, url_for, escape
import mysql.connector
import configparser
from model import Blog, User, Post

# Get DB credentials from db.ini
config = configparser.ConfigParser()
config.read('db.ini')

# Setup DB Connection
db = mysql.connector.connect(
  host="remotemysql.com",
  user="pxHpXYXX51",
  passwd=config['DATABASE']['password'],
  database="pxHpXYXX51"
)
cursor = db.cursor()

# Setup Flask API & Routes
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # set secret key for sessions

# Welcome Route
@app.route('/')
def index():
    
    # get all users to be rendered
    cursor.execute("SELECT id, name FROM Users;")
    Users = []
    for user in list(cursor.fetchall()):
        Users.append(User(str(user[0]), str(user[1])))
    
    # first get all posts to be rendered
    cursor.execute("SELECT id, userId, title, body FROM Posts;")
    Posts = []
    for post in list(cursor.fetchall()):
        # find the author in Users
        author = 'Anonymous'
        for user in Users:
            if user.id == str(post[1]):
                author = user.name
        Posts.append(Post(str(post[0]), author, str(post[2]), str(post[3])))

    # check if logged in to render correct page
    if 'username' in session:
        return render_template('home.html', posts = Posts, user=session['username'])
    return render_template('home.html', posts = Posts, user=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['pass']

        cursor.execute("SELECT id, name FROM Users WHERE name=\'" + name + "\' AND pass=\'" + password + "\';")
        
        #try:
        session['username'] = list(cursor.fetchall())[0][1]
        session['id'] = list(cursor.fetchall())[0][0]
        return redirect(url_for('index'))
        #except:
            #return render_template('login.html', error = 'Invalid username or password.')
    return render_template('login.html', error = None)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for('index'))

@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        #try:
        title = request.form['title']
        body = request.form['body']
        userId = session['id']

        cursor.execute("INSERT INTO Posts (userId, title, body) VALUES (" + userId + ",\"" + title + "\",\"" + body + "\");")
        return redirect(url_for('index'))
        #except:
            #return redirect(url_for('index'))

# Users
@app.route('/users/')
@app.route('/users/<id>')
def getUsers(id = None):
    if id == None:
        cursor.execute("SELECT id, name FROM Users;")
        res = ''
        for user in list(cursor.fetchall()):
            res += '{id:' + str(user[0]) + ',name:\"' + str(user[1]) + '\"},'
        return res[:-1]
    else:
        try:
            cursor.execute("SELECT id, name FROM Users WHERE id=\"" + str(id) + '\";')
            res = ''
            for user in list(cursor.fetchall()):
                res += '{id:' + str(user[0]) + ',name:\"' + str(user[1]) + '\"}'
            return res
        except:
            return 'No user found.'

# Posts
@app.route('/posts/')
@app.route('/posts/<id>')
def getPosts(id = None):
    if id == None:
        cursor.execute("SELECT id, userId, title, body FROM Posts;")
        res = ''
        for post in list(cursor.fetchall()):
            res += '{id:' + str(post[0]) + ',userId:' + str(post[1]) + ',title:\"' + str(post[2]) + '\",body:\"' + str(post[3]) + '\"},'
        return res[:-1]
    else:
        try:
            cursor.execute("SELECT id, userId, title, body FROM Posts WHERE id=\"" + str(id) + '\";')
            res = ''
            for post in list(cursor.fetchall()):
                res += '{id:' + str(post[0]) + ',userId:' + str(post[1]) + ',title:\"' + str(post[2]) + '\",body:\"' + str(post[3]) + '\"}'
            return res
        except:
            return 'No post found.'

# Start the server
if __name__ == '__main__':
    app.run()