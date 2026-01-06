import sqlite3
import os

def get_connection(db_path="output/asana_simulation.sqlite"):
    """
    Connect to SQLite database.
    Creates the output folder if it does not exist.
    """
    # Ensure folder exists
    folder = os.path.dirname(db_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
