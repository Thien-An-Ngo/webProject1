import os
import requests

from flask import Flask, session, render_template, request, redirect, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

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

error = None
key = "qK70VNE35zrRo69bTbV5Q"

@app.route("/")
def index():
    if "username" in session and session["username"] != None:
        bookList = db.execute("SELECT * FROM books ORDER BY id ASC").fetchall()
        return render_template("index.html", books=bookList)
    return redirect("/login")

@app.route("/search", methods=["POST"])
def search():
    searchResults = []
    search = request.form.get("search")
    search = f"%{search}%"
    results = db.execute("SELECT * FROM books WHERE isbn LIKE :search OR title LIKE :search OR author LIKE :search",
                    {"search": search}).fetchall()
    return render_template("index.html", books=results)

@app.route("/book/<int:id>")
def bookPage(id=None):
    book = db.execute("SELECT * FROM books WHERE id=:id", {"id": id}).fetchone()
    isbn = db.execute("SELECT * FROM books WHERE id=:id", {"id": id}).fetchall()
    comments = db.execute("SELECT * FROM reviews WHERE book_id=:id", {"id": id}).fetchall()
    print(book)
    for i in isbn:
        isbn = i.isbn
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                params={"isbns": isbn, "key": key})
    if res.status_code != 200:
        average_score = db.execute("SELECT AVG(rating) FROM reviews WHERE book_id=:id", {"id": id}).fetchone()
        rating_count = db.execute("SELECT COUNT(*) FROM reviews WHERE book_id=:id", {"id": id}).fetchone()
    else:
        data = res.json()
        books = data["books"]
        average_score = data["books"][0]["average_rating"]
        print(f"res: {average_score}")
        rating_count = data["books"][0]["ratings_count"]
    print(f"AS: {average_score}, RC: {rating_count}")
    hasReviewed = db.execute("SELECT * FROM reviews WHERE user_id=:user_id AND book_id=:id", 
                        {"user_id": session["user_id"], "id": id}).rowcount == 1
    return render_template("book.html", book=book, comments=comments, id=id, error=error, hasReviewed=hasReviewed,
    average_score=average_score, rating_count=rating_count)

@app.route("/review", methods=["POST"])
def review():
    rating = request.form.get("rating")
    title = request.form.get("title")
    text_review = request.form.get("text")
    book_id = request.form.get("id")
    book_id = int(book_id)
    user_id = session["user_id"]
    if rating == None:
        error = "Please rate the book in order to post your review."
        return redirect(f"/book/{book_id}")
    try:
        db.execute(
        "INSERT INTO reviews (score, title, text_review, user_id, book_id) VALUES (:rating, :title, :text_review, :user_id, :book_id)",
                {"rating": rating, "title": title, "text_review": text_review, "user_id": user_id, "book_id": book_id,})
        db.commit()
    except SQLAlchemyError as e:
        error = "You have already posted a review for this book."
        return redirect(f"/book/{book_id}")
    return redirect(f"/book/{book_id}")

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
        user_id = db.execute("SELECT * FROM users WHERE username=:username", {"username": session["username"]}).fetchall()
        for i in user_id:
            session["user_id"] = i.id
        session["username"] = username
        return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/api/<isbn>")
def api(isbn=None):
    books = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).fetchall()
    for book in books:
        title = book.title
        author = book.author
        year = book.year
        isbn = book.isbn
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                params={"isbns": isbn, "key": key})
    # if books is None:
    if res.status_code != 200:
        # raise Exception("ERROR: API request unsuccessful")
        return jsonify({"error": "ISBN not found"})
    data = res.json()
    print(f"data: {data}")
    average_score = data["books"][0]["average_rating"]
    rating_count = data["books"][0]["ratings_count"]
    return jsonify({
        "title": title,
        "author": author,
        "publishing_year": year,
        "isbn": isbn,
        "rating_count": rating_count,
        "average_score": average_score
    })
