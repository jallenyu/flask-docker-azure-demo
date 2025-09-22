from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# --- Database config ---
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")

SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# --- Model ---
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


# Create tables
with app.app_context():
    db.create_all()


# --- CRUD routes ---
@app.route("/")
def index():
    return {"message": "Hello, this is a small Flask app demo"}


@app.route("/health")
def health():
    return {"health": "Flask app is running!"}


# Create
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    item = Item(name=data["name"])
    db.session.add(item)
    db.session.commit()
    return jsonify({"id": item.id, "name": item.name}), 201


# Read all
@app.route("/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    return jsonify([{"id": i.id, "name": i.name} for i in items])


# Read one
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify({"id": item.id, "name": item.name})


# Update
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    item.name = data["name"]
    db.session.commit()
    return jsonify({"id": item.id, "name": item.name})


# Delete
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
