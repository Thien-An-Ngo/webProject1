import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
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
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    if session["user"] == None:
        return redirect("/login")
    else:
        return render_template("index.html")
    
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("")
    if request.method == "POST":
        user = request.form.get("name")
        session["user"] = user
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        error = ""
        username = request.form.get("username")
        password0 = request.form.get("password")
        password1 = request.form.get("passwordRepeat")
        if len(username) < 5 or len(password0) < 8:
            error = "Either username or password length do not suffice (username has to be greater than 5 and password has to contain a minimum of 8 words)"
            print(error)
            print("hurz")
            return render_template("register.html", error=error)
        if not password0 == password1:
            error = "Passwords do not match!"
            print(password0)
            print(password1)
            print(error)
            return render_template("register.html", error=error)
        if error == "":
            db.execute("insert into accounts (username, passwd) values (:username, :password)", {"username": username, "password": password0})
            db.commit()
            print(f"Hallo {error}")
        return redirect("/login")
    