import sqlite3
import os


#----------------------------------- GLOBALS -----------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, 'virtual_closet.db')

#---------------------------------- Constants ----------------------------------


#------------------------------- Insert Functions -------------------------------
def insert_user(username, email, password_hash):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
    """, (username, email, password_hash))

    conn.commit()
    conn.close()

def insert_category(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO categories (name)
        VALUES (?)
    """, (name,))

    conn.commit()
    conn.close()

def insert_clothes(name, category_id, user_id, size=None, color=None, brand=None, image_path=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clothes (name, category_id, user_id, size, color, brand, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, category_id, user_id, size, color, brand, image_path))

    conn.commit()
    conn.close()

def insert_favorite(user_id, clothes_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO favorites (user_id, clothes_id)
        VALUES (?, ?)
    """, (user_id, clothes_id))

    conn.commit()
    conn.close()

def insert_outfit(user_id, outfit_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO outfits (user_id, outfit_name)
        VALUES (?, ?)
    """, (user_id, outfit_name))

    conn.commit()
    conn.close()

def insert_outfit_clothes(outfit_id, clothes_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO outfit_clothes (outfit_id, clothes_id)
        VALUES (?, ?)
    """, (outfit_id, clothes_id))

    conn.commit()
    conn.close()

# Example usage
# insert_user('Arturo', 'arturo@example.com', 'password')
# insert_category('Jackets') # Needs to be unique
# insert_clothes('T-shirt', 1, 1, 'M', 'Red', 'Nike', '/images/clothes/tshirt.jpg')
# insert_favorite(1, 1)
# insert_outfit(1, 'Casual Friday')
# insert_outfit_clothes(1, 1)

#------------------------------- Delete Functions -------------------------------
def delete_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM categories WHERE category_id = ?
    """, (category_id,))

    conn.commit()
    conn.close()

def delete_clothes(clothes_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM clothes WHERE clothes_id = ?
    """, (clothes_id,))

    conn.commit()
    conn.close()

def delete_favorite(favorite_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM favorites WHERE favorite_id = ?
    """, (favorite_id,))

    conn.commit()
    conn.close()

def delete_outfit(outfit_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM outfits WHERE outfit_id = ?
    """, (outfit_id,))

    conn.commit()
    conn.close()

def delete_outfit_clothes(outfit_id, clothes_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM outfit_clothes WHERE outfit_id = ? AND clothes_id = ?
    """, (outfit_id, clothes_id))

    conn.commit()
    conn.close()

# delete_user(2) # Delete a user with user_id = 1
# delete_category(5) # Delete a category with category_id = 2
# delete_clothes(1) # Delete a clothing item with clothes_id = 3
# delete_favorite(1) # Delete a favorite entry with favorite_id = 4
# delete_outfit(1) # Delete an outfit with outfit_id = 5
# delete_outfit_clothes(1, 3) # Remove a specific clothing item from an outfit (outfit_id = 1, clothes_id = 2)

#------------------------------- Print Function -------------------------------
def print_table(table_name):
    conn = sqlite3.connect('virtual_closet.db')
    cursor = conn.cursor()

    # Fetch the table contents
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Fetch column headers
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]

    # Print table name
    print(f"\n=== {table_name.upper()} ===")

    # Print column headers
    print(" | ".join(columns))
    print("-" * (len(columns) * 15))  # Divider line based on column count

    # Print each row of the table
    for row in rows:
        print(" | ".join(map(str, row)))

    conn.close()

# Print the contents of each table
# print_table('users')
# print_table('categories')
# print_table('clothes')
# print_table('favorites')
# print_table('outfits')
# print_table('outfit_clothes')