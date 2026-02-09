# Bookmark Vault

Bookmark Vault is a full-stack web application for saving and organizing bookmarks with search, tagging, and favorites functionality. It is designed as a personal knowledge hub where a user can quickly capture links, add context (tags and notes), and later retrieve them with fast search and clear organization. The interface is intentionally clean and focused, so the core flow of saving a link, finding it again, and marking favorites feels lightweight and reliable.

#### Video Demo: [https://youtu.be/4kcOqGuxAZQ]

## Description

This project lets users register accounts, log in, and manage a private collection of bookmarks. Each bookmark stores a title, URL, optional tags, and a short note. Users can search across multiple fields, mark favorites to keep important links at the top, and delete entries with a confirmation prompt. For a smooth first-run experience, new accounts receive a small set of seeded bookmarks so the UI is not empty and all features are immediately visible.

The goal of the project is to demonstrate a complete, production-style workflow in a compact codebase: a Flask API that validates requests and enforces authentication, a SQLite database to persist data, and a React front end that provides a responsive, modern UI. I also focused on maintainable separation of concerns by keeping API calls in a service layer and using modular CSS to keep styles consistent.

## Tech Stack

### Backend
- Python 3 with Flask
- SQLite database with CS50 SQL library
- Flask-Session for server-side sessions
- Flask-CORS for cross-origin requests
- Werkzeug for password hashing

### Frontend
- React 19 with Vite
- Tailwind CSS v4
- Component-based structure

## Features

- User authentication (register, login, logout)
- Auto-seeded sample bookmarks for new users
- Create bookmarks with title, URL, tags, and notes
- Search bookmarks by title, URL, tags, or notes
- Mark bookmarks as favorites (sorted to top)
- Delete bookmarks with confirmation dialog
- Session-based authentication with secure cookies
- Responsive layout with adjustable border radius
- Custom purple and magenta theme
- Separated API service layer

## File Guide

This section explains the files I wrote and what each does.

### Backend
- [backend/app.py](backend/app.py) is the Flask application entry point. It creates the app, loads configuration, initializes the database connection, and registers the route blueprints.
- [backend/db.py](backend/db.py) contains the database setup and connection helpers for the CS50 SQL library.
- [backend/schema.sql](backend/schema.sql) defines the SQLite tables for users and bookmarks.
- [backend/utils.py](backend/utils.py) contains shared helpers like `require_login()` to enforce authentication on protected routes.
- [backend/routes/__init__.py](backend/routes/__init__.py) sets up the blueprint exports so they can be registered cleanly in the app.
- [backend/routes/auth.py](backend/routes/auth.py) implements register, login, logout, and session user endpoints.
- [backend/routes/bookmarks.py](backend/routes/bookmarks.py) implements CRUD endpoints for bookmarks plus the favorite toggle.
- [backend/seed.py](backend/seed.py) inserts sample data for users who already exist but have no bookmarks.
- [backend/bookmarks_seed.py](backend/bookmarks_seed.py) provides the list of default bookmarks used by the seeding logic.
- [backend/requirements.txt](backend/requirements.txt) lists Python dependencies.

### Frontend
- [frontend/index.html](frontend/index.html) is the Vite entry HTML.
- [frontend/src/main.jsx](frontend/src/main.jsx) bootstraps React and mounts the app.
- [frontend/src/App.jsx](frontend/src/App.jsx) is the main layout and routing logic for authenticated vs. unauthenticated views.
- [frontend/src/Login.jsx](frontend/src/Login.jsx) handles registration and login forms.
- [frontend/src/Bookmarks.jsx](frontend/src/Bookmarks.jsx) renders the bookmark list, search, and create/delete interactions.
- [frontend/src/api.js](frontend/src/api.js) contains shared request helpers and base configuration.
- [frontend/src/services/authApi.js](frontend/src/services/authApi.js) wraps authentication calls and keeps auth requests in one place.
- [frontend/src/services/bookmarkApi.js](frontend/src/services/bookmarkApi.js) wraps bookmark CRUD requests and the favorite toggle.
- [frontend/src/index.css](frontend/src/index.css) pulls together Tailwind and project styles.
- [frontend/src/styles/base.css](frontend/src/styles/base.css) provides global typography and base element styles.
- [frontend/src/styles/theme.css](frontend/src/styles/theme.css) defines the color tokens used across the app.
- [frontend/src/styles/components.css](frontend/src/styles/components.css) contains reusable component class styles.
- [frontend/src/styles/tailwind.css](frontend/src/styles/tailwind.css) defines Tailwind directives for build-time generation.

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- npm

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# macOS/Linux
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the Flask server:
```bash
flask --app app run
```

The backend runs on `http://localhost:5000`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend runs on `http://localhost:5173` (or another port if 5173 is busy).

## Sample Data

New users automatically receive 10 sample bookmarks on registration. To manually seed bookmarks for existing users without bookmarks:
```bash
cd backend
python seed.py
```

## Usage

1. Open your browser to `http://localhost:5173`.
2. Create a new account; you will automatically receive 10 sample bookmarks.
3. Try the features:
   - Search bookmarks by title, URL, tags, or notes.
   - Click the star icon to mark favorites; favorites appear at the top.
   - Delete bookmarks; a confirmation dialog appears.
   - Click bookmark titles to open URLs in a new tab.
4. Create more bookmarks to test the full CRUD flow.

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  hash TEXT NOT NULL
);
```

### Bookmarks Table
```sql
CREATE TABLE bookmarks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  tags TEXT DEFAULT '',
  note TEXT DEFAULT '',
  is_favorite INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## API Endpoints

### Authentication
- `POST /api/register` creates a new user account
- `POST /api/login` authenticates and creates a session
- `POST /api/logout` clears the session
- `GET /api/me` returns the current user

### Bookmarks
- `GET /api/bookmarks` lists all user bookmarks (optional `?query=` search)
- `POST /api/bookmarks` creates a new bookmark
- `PUT /api/bookmarks/:id` updates a bookmark
- `DELETE /api/bookmarks/:id` deletes a bookmark
- `PATCH /api/bookmarks/:id/favorite` toggles favorite status

## Design Decisions

I debated using JWT for authentication but chose session-based auth for simplicity and better security in a single-domain app. Server-side sessions keep token handling off the client and avoid local storage pitfalls. I also weighed using PostgreSQL, but SQLite fits the scope and grading environment and keeps setup minimal.

On the frontend, I considered using a state management library, but the app is small enough that local component state and a clear service layer are sufficient and easier to explain. For styling, I used Tailwind CSS v4 with custom theme tokens and a small set of component classes to keep visuals consistent while still allowing quick iteration. I also decided to seed bookmarks for new users so the UI does not feel empty and users can immediately see search, favorites, and list interactions without first creating data.

## Challenges and Solutions

- CORS issues were resolved by configuring Flask-CORS with credentials support.
- Cookie blocking was avoided by keeping both services on localhost.
- Session persistence is handled via Flask-Session stored in the `.flask_session/` folder (not committed to git).
- Duplicate route helpers were consolidated into `require_login()` in `utils.py`.

## AI Assistance Disclosure

In accordance with CS50's academic honesty policy, I disclose the following:

**AI tools used:** GitHub Copilot and ChatGPT were used during development.

**How AI was used:**
- Assistance with Flask routing patterns and error handling structure.
- Help debugging CORS and session configuration issues.
- Refactoring suggestions for component organization.

**What I implemented myself:**
- All business logic and feature requirements.
- Database schema design.
- Component architecture decisions.
- API endpoint design.
- UI and layout choices.
- Search functionality implementation.

**Understanding:** I understand all code in this project and can explain any part of it. The AI assisted with syntax and best practices, but all architectural decisions and feature implementations were my own.

## Future Enhancements

- Edit bookmark functionality (inline or modal)
- Bookmark folders or categories
- URL validation and auto-prefixing
- Import and export bookmarks
- Browser extension integration
- Sharing bookmarks with other users

## License

This project was created as a final project for Harvard's CS50 course.

## Author

Created by Samal Ibrahim for CS50x Final Project 2026
