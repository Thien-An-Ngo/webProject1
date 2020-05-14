DROP TABLE reviews;

DROP TABLE users;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    passwd VARCHAR NOT NULL
);

CREATE TABLE reviews(
    id SERIAL PRIMARY KEY,
    score FLOAT NOT NULL CHECK (score >= 1 AND score <= 5),
    text_review VARCHAR,
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books
);