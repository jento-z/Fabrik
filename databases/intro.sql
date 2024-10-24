-- CREATE TABLE users (
--     user_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username TEXT NOT NULL,
--     email TEXT NOT NULL UNIQUE,
--     password_hash TEXT NOT NULL,
--     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
-- );

-- INSERT INTO users (username, email, password_hash)
-- VALUES ('Arturo', '6arturodiaz@gmail.com', 'password');

-- CREATE TABLE clothes (
--     clothes_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL,
--     category_id INTEGER NOT NULL,
--     user_id INTEGER NOT NULL,
--     size TEXT,
--     color TEXT,
--     brand TEXT,
--     FOREIGN KEY (category_id) REFERENCES categories(category_id),
--     FOREIGN KEY (user_id) REFERENCES users(user_id)
-- );

-- INSERT INTO clothes (name, category_id, user_id, size, color, brand, image_path)
-- VALUES ('T-shirt', 1, 1, 'M', 'Red', 'Nike', '/images/clothes/tshirt.jpg');

-- CREATE TABLE categories (
--     category_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL UNIQUE
-- );

-- INSERT INTO categories (name) 
-- VALUES ('Tops'), ('Bottoms'), ('Shoes'), ('Accessories');


-- CREATE TABLE favorites (
--     favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     clothes_id INTEGER NOT NULL,
--     FOREIGN KEY (user_id) REFERENCES users(user_id),
--     FOREIGN KEY (clothes_id) REFERENCES clothes(clothes_id)
-- );


-- CREATE TABLE outfits (
--     outfit_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     outfit_name TEXT NOT NULL,
--     FOREIGN KEY (user_id) REFERENCES users(user_id)
-- );

-- INSERT INTO outfits (user_id, outfit_name) 
-- VALUES (1, 'Casual Friday');



-- CREATE TABLE outfit_clothes (
--     outfit_id INTEGER NOT NULL,
--     clothes_id INTEGER NOT NULL,
--     FOREIGN KEY (outfit_id) REFERENCES outfits(outfit_id),
--     FOREIGN KEY (clothes_id) REFERENCES clothes(clothes_id)
-- );

-- INSERT INTO outfit_clothes (outfit_id, clothes_id) 
-- VALUES (1, 2), (1, 3);















-- ALTER TABLE users ADD COLUMN status TEXT;

-- DROP TABLE users;

-- INSERT INTO users (name, username) 
-- VALUES ('Caleb Curry', 'calcur123');

-- INSERT INTO users (name, username) 
-- VALUES ('John Smith', 'js'), ('Sal Smith', 'ss'), ('Cole Conner', 'colec');

-- SELECT * FROM users
-- LIMIT 2;

-- UPDATE users SET email = 'newemail@gmail.com' WHERE id = 1;

-- DELETE FROM users WHERE id = 2;

-- SELECT * FROM users

-- CREATE TABLE posts (
--     id INTEGER PRIMARY KEY,
--     user_id INTEGER REFERENCES users(id), --foreign key
--     title TEXT NOT NULL,
--     body TEXT NOT NULL
-- );

-- INSERT INTO posts (user_id, title, body)
-- VALUES (1, 'my better first post', 'purple is my favorite color');

-- CREATE VIEW posts_info AS
--     SELECT p.body, u.username FROM posts p
--     JOIN users u ON p.user_id = u.id;

-- SELECT * FROM posts_info;