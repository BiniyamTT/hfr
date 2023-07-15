import os
import sqlite3

def insert_default_images(folder_path, database_path):
    # Connect to the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Iterate over the images in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Adjust the file extensions as needed
            image_path = os.path.join(folder_path, filename)

            # Read the image data as binary
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

            # Insert the image into the database using the image name as the 'name' field
            cursor.execute('INSERT INTO default_images (name, image_data) VALUES (?, ?)', (filename, image_data))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def process_default_images():
    folder_path = '../hasslefreerentals/static/subcat images'  # Provide the path to the 'default_images' folder
    database_path = '../instance/hfr.sqlite'  # Provide the path to your SQLite database

    insert_default_images(folder_path, database_path)
    return 'Default images inserted into the database.'