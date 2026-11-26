import os                       # open uploaded files
import shutil                   # copies uploaded files into the resources folder
import sqlite3                  # stores resource information in a local database
from pathlib import Path        # safely handle paths

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
            uploaded_at TEXT NOT NULL
        )
    """)

    connection.commit()        # Saves the table creation
    connection.close()         # Closes the database connection


create_database()