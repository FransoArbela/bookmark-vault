import os
from cs50 import SQL

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bookmarks.db")

# Create empty SQLite file if it doesn't exist yet
if DATABASE_URL.startswith("sqlite:///"):
    database_path = DATABASE_URL.replace("sqlite:///", "")
    if database_path and not os.path.exists(database_path):
        open(database_path, "a").close()

db = SQL(DATABASE_URL)
