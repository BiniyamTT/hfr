import os
import sqlite3

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def insert_default_images(folder_path):
    # Connect to the database
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cursor = conn.cursor()

    # Iterate over the images in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Adjust the file extensions as needed
            image_path = os.path.join(folder_path, filename)

            # Read the image data as binary
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            name = os.path.splitext(filename)[0]
            # Insert the image into the database using the image name as the 'name' field
            cursor.execute('INSERT INTO default_images (name, image_data) VALUES (?, ?)', (name, image_data))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def process_default_images():
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    folder_path = os.path.join(current_directory, 'subcat_images')  # Provide the path to the 'subcat_images' folder

    insert_default_images(folder_path)
    return 'Default images inserted into the database.'

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

@click.command('process-default-images')
def process_default_images_command():
    process_default_images()
    click.echo('Processed and inserted the default images into the database.')    
    
    
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(process_default_images_command)