DROP TABLE reviews;

DROP TABLE books;

DROP TABLE users;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    passwd VARCHAR NOT NULL
);

CREATE TABLE books(
    id SERIAL PRIMARY KEY,
    isbn VARCHAR UNIQUE NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE reviews(
    id SERIAL PRIMARY KEY,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR,
    text_review VARCHAR,
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books,
    UNIQUE (user_id, book_id)
);