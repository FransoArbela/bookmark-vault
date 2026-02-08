#!/usr/bin/env python3
"""
Manual seed script to populate the database with sample bookmarks.
Run this script from the backend directory: python seed.py

Note: New users automatically get sample bookmarks on registration.
This script is useful for manually seeding bookmarks for existing users.
"""

from db import db
from bookmarks_seed import SAMPLE_BOOKMARKS

def seed_bookmarks():
    """Seed the database with sample bookmarks for the first user"""
    try:
        # Get the first user in the database
        users = db.execute("SELECT id FROM users LIMIT 1")
        
        if not users:
            print("No users found. Please create an account first by logging in.")
            return
        
        user_id = users[0]["id"]
        
        # Check if user already has bookmarks
        existing = db.execute("SELECT COUNT(*) as count FROM bookmarks WHERE user_id = ?", user_id)
        bookmark_count = existing[0]["count"]
        
        if bookmark_count > 0:
            print(f"User {user_id} already has {bookmark_count} bookmarks. Skipping.")
            return
        
        # Insert sample bookmarks
        for bookmark in SAMPLE_BOOKMARKS:
            db.execute(
                """
                INSERT INTO bookmarks (user_id, title, url, tags, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                user_id,
                bookmark["title"],
                bookmark["url"],
                bookmark["tags"],
                bookmark["note"]
            )
        
        print(f"✓ Added {len(SAMPLE_BOOKMARKS)} sample bookmarks for user {user_id}")
    
    except Exception as error:
        print(f"✗ Error seeding bookmarks: {error}")

if __name__ == "__main__":
    seed_bookmarks()
