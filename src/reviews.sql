DROP TABLE reviews;

CREATE TABLE reviews(
    id SERIAL PRIMARY KEY,
    score INTEGER NOT NULL CHECK (score >= 1 AND score <= 5),
    title VARCHAR,
    text_review VARCHAR,
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books,
    UNIQUE (user_id, book_id)
);