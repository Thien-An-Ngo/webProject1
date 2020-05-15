import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    books = db.execute("SELECT isbn, title, author, year FROM books").fetchall()
    for book in books:
        print(f"{book.title}, written by {book.author}, published in {book.year} has the ISBN {book.isbn}")

if __name__ == "__main__":
    main()
