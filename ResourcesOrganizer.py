import os                             # open uploaded files
import shutil                         # copies uploaded files into the resources folder
import sqlite3                        # stores resource information in a local database
from pathlib import Path              # safely handle paths
from datetime import datetime         # records the date and time when a resource is deleted
import tkinter as tk                  # creates the application window and basic widgets
from tkinter import ttk, filedialog   # provides styled widgets and a file dialog

PROJECT_DIR = Path(__file__).resolve().parent    # Gets the folder where this Python file is located
RESOURCES_DIR = PROJECT_DIR / "resources"        # Sets the folder used to store uploaded resources
RESOURCES_DIR.mkdir(exist_ok=True)               # Creates the resources folder if it doesn't exist

DATABASE_PATH = PROJECT_DIR / "edutrack.db"      # Sets the location of the local database file


def choose_file():
    """Opens a dialog for the user to select a study resource file."""

    file_path = filedialog.askopenfilename(
        title="Choose a study resource",
        filetypes=[
            ("Supported files", "*.pdf *.doc *.docx *.ppt *.pptx *.png *.jpg *.jpeg"),
            ("All files", "*.*")
        ]
    )

    if file_path:
        selected_file_var.set(file_path)      # Shows the selected file path in the form


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


def restore_resource(resource_id):
    """Restores a resource from the trash."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE resources
        SET is_deleted = 0, deleted_at = NULL
        WHERE id = ?
    """, (resource_id,))

    connection.commit()
    connection.close()


def clear_resource(resource_id):
    """Permanently deletes a resource and its uploaded file."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT file_path FROM resources WHERE id = ?", 
        (resource_id,)
        )
    result = cursor.fetchone()  # gets the saved file path

    if result:
        file_path = Path(result[0])   # converts the file path into a Path object

        if file_path.exists():
            file_path.unlink()  # permanently deletes the uploaded file

    cursor.execute(
        "DELETE FROM resources WHERE id = ?", 
        (resource_id,)
        )

    connection.commit()
    connection.close()

create_database()  # Creates the database table when this file runs

root = tk.Tk()                                          # Creates the main application window
root.title("EduTrack - Study Resources Organizer")      # Sets the window title
root.geometry("800x550")                                # Sets the starting window size

subject_var = tk.StringVar()                            # Stores the subject entered by the user
resource_type_var = tk.StringVar(value="Notes")         # Stores the selected resource type
title_var = tk.StringVar()                              # Stores the resource title
selected_file_var = tk.StringVar()                      # Stores the path of the selected file

main_frame = ttk.Frame(root, padding=20)                # Creates the main content area
main_frame.pack(fill="both", expand=True)

ttk.Label(
    main_frame,
    text="Study Resources Organizer",
    font=("Arial", 18, "bold")
).pack(anchor="w", pady=(0, 15))

form_frame = ttk.LabelFrame(
    main_frame,
    text="Upload Study Resource",
    padding=15
)
form_frame.pack(fill="x")

ttk.Label(form_frame, text="Subject:").grid(row=0, column=0, sticky="w", pady=6)
ttk.Entry(form_frame, textvariable=subject_var, width=45).grid(
    row=0, column=1, sticky="ew", padx=(10, 0), pady=6
)

ttk.Label(form_frame, text="Resource Type:").grid(row=1, column=0, sticky="w", pady=6)
ttk.Combobox(
    form_frame,
    textvariable=resource_type_var,
    values=["Notes", "Slides", "Past Year Questions"],
    state="readonly",
    width=42
).grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=6)

ttk.Label(form_frame, text="Title:").grid(row=2, column=0, sticky="w", pady=6)
ttk.Entry(form_frame, textvariable=title_var, width=45).grid(
    row=2, column=1, sticky="ew", padx=(10, 0), pady=6
)

ttk.Label(form_frame, text="File:").grid(row=3, column=0, sticky="w", pady=6)
ttk.Entry(
    form_frame,
    textvariable=selected_file_var,
    state="readonly",
    width=35
).grid(row=3, column=1, sticky="ew", padx=(10, 8), pady=6)

ttk.Button(
    form_frame,
    text="Choose File",
    command=choose_file
).grid(row=3, column=2, pady=6)

form_frame.columnconfigure(1, weight=1)  # Lets input fields expand with the window

root.mainloop()  # Keeps the window open and listens for user actions