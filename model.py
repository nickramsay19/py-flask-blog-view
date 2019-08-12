import configparser
import mysql.connector

# Create Posts
Posts = []
class Post:
    def __init__(self, id, author, title, body):
        self.id = id 
        self.author = author
        self.title = title 
        self.body = body 

# Create Users
Users = []
class User:
    def __init__(self, id, name):
        self.id = id 
        self.name = name

class Blog:
    def __init__(self):
        self.Posts = []
        self.Users = []
        self.Account = User(0,'')

        # Get DB credentials from db.ini
        config = configparser.ConfigParser()
        config.read('db.ini')

        # setup DB
        db = mysql.connector.connect(
            host="remotemysql.com",
            user="pxHpXYXX51",
            passwd=config['DATABASE']['password'],
            database="pxHpXYXX51"
        )
        cursor = db.cursor()

        # Get all Users
        cursor.execute("SELECT id, name FROM Users;")
        Users = []
        for user in list(cursor.fetchall()):
            Users.append(User(str(user[0]), str(user[1])))

        # Get all Posts
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

