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
    year INTEGER NOT NULL,
    score_count INTEGER,
    average_score FLOAT
);

CREATE TABLE reviews(
    id SERIAL PRIMARY KEY,
    score FLOAT NOT NULL CHECK (score >= 1 AND score <= 5),
    text_review VARCHAR,
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books
);