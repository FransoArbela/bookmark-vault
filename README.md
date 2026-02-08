# Bookmark Vault

A full-stack web application for saving and organizing bookmarks with search, tagging, and favorites functionality.

#### Video Demo: [URL HERE]

## Description

Bookmark Vault is a personal bookmark manager that allows users to save, organize, search, and categorize their favorite websites. Users can register an account, add bookmarks with titles and descriptions, tag them for organization, mark favorites, and search through their collection. The application features a clean, modern interface with a purple/magenta color theme and provides a seamless experience for managing web bookmarks.

## Tech Stack

### Backend
- **Python 3** with Flask web framework
- **SQLite** database with CS50 SQL library
- **Flask-Session** for session management
- **Flask-CORS** for cross-origin requests
- **Werkzeug** for password hashing

### Frontend
- **React 19** with Vite build tool
- **Tailwind CSS v4** for styling
- Modern component-based architecture

## Features

- ✅ User authentication (register/login/logout)
- ✅ Auto-seeded sample bookmarks for new users (10 default bookmarks)
- ✅ Create bookmarks with title, URL, tags, and notes
- ✅ Search bookmarks by title, URL, tags, or notes
- ✅ Mark bookmarks as favorites (sorted to top)
- ✅ Delete bookmarks with confirmation dialog
- ✅ Session-based authentication with secure cookies
- ✅ Responsive design with adjustable border radius
- ✅ Custom purple/magenta oklch color theme
- ✅ Modular component-based CSS architecture
- ✅ Separated API service layer for better code organization

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- npm

### Quick Start (For Graders)

**Everything is pre-configured. Just run these commands:**

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
flask --app app run
```
Backend runs at: `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: `http://localhost:5173`

Then open `http://localhost:5173` in your browser and start using the app!

---

### Detailed Setup Instructions

#### Backend Setup

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

The backend will run on `http://localhost:5000`

**Note:** The database schema and `.env` configuration are already included. No setup needed.

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

The frontend will run on `http://localhost:5173` (or another port if 5173 is busy)

## Sample Data

New users automatically receive 10 sample bookmarks on registration:
- GitHub
- Stack Overflow
- MDN Web Docs
- CSS-Tricks
- Dev.to
- Tailwind CSS
- React Documentation
- Python.org
- Flask Documentation
- YouTube

To manually seed bookmarks for existing users without bookmarks:
```bash
cd backend
python seed.py
```

## Usage

1. Open your browser to `http://localhost:5173`
2. **Create a new account** - You'll automatically receive 10 sample bookmarks
3. **Test features:**
   - Search bookmarks by title, URL, tags, or notes
   - Click the star icon (☆/★) to mark favorites - they appear at the top
   - Delete bookmarks - a confirmation dialog will appear
   - Click bookmark titles to open URLs in a new tab
   - Log out and log back in - session persists
4. **Create more bookmarks** to test the full CRUD functionality

## Testing Instructions for Graders

**Nothing needs to be configured. Just follow the Quick Start above.**

1. Start both backend and frontend servers
2. Open `http://localhost:5173` in your browser
3. Create a test account (any username/password)
4. You'll automatically see 10 sample bookmarks
5. Test the features:
   - ✅ **Search**: Use the search bar (works on title, URL, tags, notes)
   - ✅ **Create**: Add a new bookmark via the form
   - ✅ **Update**: Edit functionality (if implemented)
   - ✅ **Delete**: Click Delete button, confirm the dialog
   - ✅ **Favorites**: Click star icon - moves to top
   - ✅ **Authentication**: Log out, create another account, log back in
   - ✅ **Responsive Design**: Resize browser window

**Database:** SQLite file at `backend/bookmarks.db` - automatically created on first run

**Sample Data:** Automatically seeded for new users on registration

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
- `POST /api/register` - Create a new user account
- `POST /api/login` - Authenticate and create session
- `POST /api/logout` - Clear session
- `GET /api/me` - Get current user info

### Bookmarks
- `GET /api/bookmarks` - List all user's bookmarks (with optional `?query=` search)
- `POST /api/bookmarks` - Create a new bookmark
- `PUT /api/bookmarks/:id` - Update a bookmark
- `DELETE /api/bookmarks/:id` - Delete a bookmark
- `PATCH /api/bookmarks/:id/favorite` - Toggle favorite status

## Code Architecture

### Backend Organization
- **Modular routing:** Separate modules for auth and bookmarks endpoints
- **Shared utilities:** `utils.py` contains reusable functions (e.g., `require_login()`)
- **Clean variable names:** Descriptive names throughout codebase (no single-letter variables)
- **Automatic seeding:** New users receive sample bookmarks automatically on registration

### Frontend Organization
- **Service layer:** API calls separated into `services/authApi.js` and `services/bookmarkApi.js`
- **Component-focused:** Components handle UI logic, services handle API communication
- **Modular styling:** CSS organized into tailwind.css, theme.css, base.css, components.css
- **Reusable components:** All recurring UI elements use component classes from components.css

## Design Decisions

- **Session-based auth** instead of JWT for simplicity and better security for a single-domain app
- **SQLite** for portability and ease of grading
- **React** for modern, reactive UI without page reloads
- **Tailwind CSS v4** with @theme directive
- **Service layer pattern** to separate API calls from UI components for cleaner, testable code
- **Component-based CSS** for maintainability and DRY principle
- **Auto-seeding on registration** to provide users an immediate, populated experience
- **Favorites sorting** - favorites appear first in the list for quick access
- **Descriptive variable names** and consolidated duplicate functions for code clarity

## Challenges & Solutions

- **CORS issues**: Solved by configuring Flask-CORS with credentials support
- **Cookie blocking**: Fixed by ensuring backend and frontend use the same domain (localhost)
- **Session persistence**: Flask sessions stored in `.flask_session/` folder (not committed to git)
- **Duplicate code**: Consolidated `require_login()` in `utils.py` module


## AI Assistance Disclosure

In accordance with CS50's academic honesty policy, I disclose the following:

**AI tools used:** GitHub Copilot and ChatGPT were used during development

**How AI was used:**
- Assistance with Flask routing patterns and error handling structure
- Help debugging CORS and session configuration issues
- Code refactoring suggestions for component organization

**What I implemented myself:**
- All business logic and feature requirements
- Database schema design
- Component architecture decisions
- API endpoint design
- UI/UX layout and color scheme choices
- Problem-solving approach for session management
- Search functionality implementation

**Understanding:** I understand all code in this project and can explain any part of it. The AI assisted with syntax and best practices, but all architectural decisions and feature implementations were my own.

## Future Enhancements

- Edit bookmark functionality (inline or modal)
- Bookmark folders/categories
- URL validation and auto-prefixing
- Import/export bookmarks
- Browser extension integration
- Sharing bookmarks with other users

## License

This project was created as a final project for Harvard's CS50 course.

## Author

Created by Samal Ibrahim for CS50x Final Project 2026
