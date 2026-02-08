from dotenv import load_dotenv
from flask import Flask
from flask_session import Session
from flask_cors import CORS

from routes import register_routes
from db import db

load_dotenv()

app = Flask(__name__)

# Allow frontend on Vite dev server to make authenticated requests
CORS(app, resources={r"/api/*": {
    "origins": ["http://localhost:5173"],
    "supports_credentials": True
}})

# Session configuration for authentication
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
Session(app)

def init_db():
    with open("schema.sql", "r", encoding="utf-8") as schema_file:
        sql_content = schema_file.read()
    statements = [statement.strip() for statement in sql_content.split(";") if statement.strip()]
    for statement in statements:
        db.execute(statement)

init_db()
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)