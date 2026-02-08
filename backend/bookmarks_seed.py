"""
Sample bookmarks data for seeding new user accounts.
"""

SAMPLE_BOOKMARKS = [
    {
        "title": "GitHub",
        "url": "https://github.com",
        "tags": "code,development,version-control",
        "note": "Version control and collaboration platform"
    },
    {
        "title": "Stack Overflow",
        "url": "https://stackoverflow.com",
        "tags": "help,learning,code,debugging",
        "note": "Q&A community for programmers"
    },
    {
        "title": "MDN Web Docs",
        "url": "https://developer.mozilla.org",
        "tags": "learning,web,documentation,javascript",
        "note": "Mozilla's comprehensive web development docs"
    },
    {
        "title": "CSS-Tricks",
        "url": "https://css-tricks.com",
        "tags": "css,web-design,learning",
        "note": "Articles and learning resources about CSS"
    },
    {
        "title": "Dev.to",
        "url": "https://dev.to",
        "tags": "blogs,development,community",
        "note": "Community of developers sharing articles"
    },
    {
        "title": "Tailwind CSS",
        "url": "https://tailwindcss.com",
        "tags": "css,framework,utility",
        "note": "Utility-first CSS framework for rapid UI"
    },
    {
        "title": "React Documentation",
        "url": "https://react.dev",
        "tags": "javascript,frontend,framework",
        "note": "Official React docs and tutorials"
    },
    {
        "title": "Python.org",
        "url": "https://python.org",
        "tags": "python,programming,documentation",
        "note": "Official Python programming language site"
    },
    {
        "title": "Flask Documentation",
        "url": "https://flask.palletsprojects.com",
        "tags": "python,backend,framework",
        "note": "Flask web framework for Python"
    },
    {
        "title": "YouTube",
        "url": "https://youtube.com",
        "tags": "video,learning,entertainment",
        "note": "Video sharing platform"
    },
]


def seed_user_bookmarks(user_id, database):
    """
    Add sample bookmarks to a new user's account.
    
    Args:
        user_id: The ID of the newly registered user
        database: The database connection object (db)
    """
    try:
        for bookmark in SAMPLE_BOOKMARKS:
            database.execute(
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
    except Exception as error:
        # Silently fail - don't break registration if seeding fails
        print(f"Warning: Could not seed bookmarks for user {user_id}: {error}")
