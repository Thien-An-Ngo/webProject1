import os

from flask import Flask, session, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "123456789abcdefghi"

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    if "username" in session and session["username"] != None:
        bookList = db.execute("SELECT isbn, title, author, year FROM books ORDER BY average_score DESC").fetchall()
        books = []
        for book in bookList:
            bookItem = [f"{book.title}", f"{book.author}", f"{book.year}", f"{book.isbn}"]
            books.append(bookItem)
        return render_template("index.html", books=books)
    return redirect("/login")

@app.route("/search", methods=["POST"])
def search():
    searchResults = []
    search = request.form.get("search")
    search = f"%{search}%"
    results = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn LIKE :search OR title LIKE :search OR author LIKE :search",
                    {"search": search}).fetchall()
    for result in results:
        resultItem = [f"{result.title}", f"{result.author}", f"{result.year}", f"{result.isbn}"]
        searchResults.append(resultItem)
    return render_template("index.html", books=searchResults)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    username = ""
    password = ""
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(f"{username} / {password}")
        if db.execute("SELECT * FROM users WHERE username=:username AND passwd=:password",
                    {"username": username, "password": password}).rowcount == 0:
            error = "Username or Password is incorrect."
            return render_template("login.html", error=error)
        session["username"] = username
        return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        error = ""
        username = request.form.get("username")
        password0 = request.form.get("password")
        password1 = request.form.get("passwordRepeat")
        if db.execute("SELECT username FROM users WHERE username=:username", {"username": username}).rowcount == 1:
            error = "Username already taken. Please select a new one."
        elif len(username) < 3 or len(password0) < 8:
            error = "Either username or password length do not suffice (username has to be greater than 2 and password has to contain a minimum of 8 letters)"
            print(error)
            print("hurz")
        elif not password0 == password1:
            error = "Passwords do not match!"
            print(password0)
            print(password1)
            print(error)
        elif error == "":
            db.execute("insert into users (username, passwd) values (:username, :password)",
                                        {"username": username, "password": password0})
            db.commit()
            print(f"Hallo {error}")
            return redirect("/login")
        return render_template("register.html", error=error)
