import os                       # open uploaded files
import shutil                   # copies uploaded files into the resources folder
import sqlite3                  # stores resource information in a local database
from pathlib import Path        # safely handle paths
from datetime import datetime   # records the date and time when a resource is deleted

PROJECT_DIR = Path(__file__).resolve().parent    # Gets the folder where this Python file is located
RESOURCES_DIR = PROJECT_DIR / "resources"        # Sets the folder used to store uploaded resources
RESOURCES_DIR.mkdir(exist_ok=True)               # Creates the resources folder if it doesn't exist

DATABASE_PATH = PROJECT_DIR / "edutrack.db"      # Sets the location of the local database file


def create_database():
    """Creates the table used to store uploaded resource information."""

    connection = sqlite3.connect(DATABASE_PATH)    # Connects to the database
    cursor = connection.cursor()                   # Creates a cursor to run SQL commands

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            title TEXT NOT NULL,
            file_path TEXT NOT NULL,
            uploaded_at TEXT NOT NULL,
            is_deleted INTEGER NOT NULL DEFAULT 0,
            deleted_at TEXT
        )
    """)

    connection.commit()        # Saves the table creation
    connection.close()         # Closes the database connection


create_database()

def move_to_trash(resource_id):
    """Moves a resource as deleted without removing it permanently."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE resources
        SET is_deleted = 1, deleted_at = ?
        WHERE id = ?
    """, (datetime.now().strftime("%Y-%m-%d %H:%M"), resource_id))

    connection.commit()
    connection.close()

