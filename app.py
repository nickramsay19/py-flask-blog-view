# Import dependencies
from flask import Flask, render_template, request
import mysql.connector
import configparser

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

# Welcome Route
@app.route('/')
def index():
    #return render_template('home.html')
    return 'Welcome to my Flask Blog API, created by Nicholas Ramsay'

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