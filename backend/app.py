from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# ---------------- APP SETUP ----------------
app = Flask(__name__)
CORS(app)

# ---------------- DATABASE CONFIG ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:321194142@localhost/loginappdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- MODEL ----------------
class Account(db.Model):
    __tablename__ = "accounts"

    acc_no = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pin = db.Column(db.String(10), nullable=False)
    balance = db.Column(db.Integer, default=0)

# ---------------- CREATE TABLES ----------------
with app.app_context():
    db.create_all()

# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return "Banking Backend is running successfully"

# ---------------- CREATE ACCOUNT ----------------
@app.route("/account/create", methods=["POST"])
def create_account():
    data = request.json

    acc_no = data.get("acc_no")
    name = data.get("name")
    pin = data.get("pin")

    if not acc_no or not name or not pin:
        return jsonify({"error": "All fields are required"}), 400

    if Account.query.filter_by(acc_no=acc_no).first():
        return jsonify({"error": "Account already exists"}), 409

    new_account = Account(
        acc_no=acc_no,
        name=name,
        pin=pin,
        balance=0
    )

    db.session.add(new_account)
    db.session.commit()

    return jsonify({"message": "Account created successfully"}), 201

# ---------------- LOGIN ----------------
@app.route("/account/login", methods=["POST"])
def login():
    data = request.json

    acc_no = data.get("acc_no")
    pin = data.get("pin")

    if not acc_no or not pin:
        return jsonify({"error": "Account number and PIN required"}), 400

    account = Account.query.filter_by(acc_no=acc_no, pin=pin).first()

    if not account:
        return jsonify({"error": "Invalid account number or PIN"}), 401

    return jsonify({"message": "Login successful"}), 200

# ---------------- CHECK BALANCE ----------------
@app.route("/account/balance", methods=["POST"])
def balance():
    data = request.json

    acc_no = data.get("acc_no")
    pin = data.get("pin")

    if not acc_no or not pin:
        return jsonify({"error": "Missing account number or PIN"}), 400

    account = Account.query.filter_by(acc_no=acc_no, pin=pin).first()

    if not account:
        return jsonify({"error": "Invalid account number or PIN"}), 404

    return jsonify({"balance": account.balance}), 200

# ---------------- DEPOSIT ----------------
@app.route("/account/deposit", methods=["POST"])
def deposit():
    data = request.json

    acc_no = data.get("acc_no")
    pin = data.get("pin")
    amount = data.get("amount")

    if not acc_no or not pin or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    account = Account.query.filter_by(acc_no=acc_no, pin=pin).first()

    if not account:
        return jsonify({"error": "Invalid account number or PIN"}), 404

    account.balance += amount
    db.session.commit()

    return jsonify({
        "message": "Deposit successful",
        "balance": account.balance
    }), 200

# ---------------- WITHDRAW ----------------
@app.route("/account/withdraw", methods=["POST"])
def withdraw():
    data = request.json

    acc_no = data.get("acc_no")
    pin = data.get("pin")
    amount = data.get("amount")

    if not acc_no or not pin or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    account = Account.query.filter_by(acc_no=acc_no, pin=pin).first()

    if not account:
        return jsonify({"error": "Invalid account number or PIN"}), 404

    if account.balance < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    account.balance -= amount
    db.session.commit()

    return jsonify({
        "message": "Withdrawal successful",
        "balance": account.balance
    }), 200

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
