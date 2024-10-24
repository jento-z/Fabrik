import sqlite3

def insert_clothes_with_image(name, category_id, user_id, size, color, brand, image_path):
    conn = sqlite3.connect('virtual_closet.db')
    cursor = conn.cursor()
    
    with open(image_path, 'rb') as file:
        image_blob = file.read()

    cursor.execute("""
        INSERT INTO clothes (name, category_id, user_id, size, color, brand, image)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, category_id, user_id, size, color, brand, image_blob))

    conn.commit()
    conn.close()

# Example usage
insert_clothes_with_image('T-shirt', 1, 1, 'Large', 'White', 'Nike', 'C:\\Users\\Arturo Diaz\\Documents\\GitHub\\CS422\\Fabrik\\images\\shirt.png')