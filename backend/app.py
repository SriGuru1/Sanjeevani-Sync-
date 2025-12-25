from flask import Flask, render_template, request, session, jsonify
import mysql.connector
import random
import os
import datetime
from flask_mail import Mail, Message

app = Flask(__name__)

# ===============================
# Configuration (Environment Vars)
# ===============================
app.secret_key = os.getenv("SECRET_KEY")

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

# ===============================
# Database Connection
# ===============================
def create_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# ===============================
# Routes
# ===============================
@app.route("/")
def home():
    return render_template("index.html")

# ---------- Registration ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/registration", methods=["POST"])
def registration():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    session["name"] = name
    session["email"] = email
    session["password"] = password

    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user:
        return render_template("register.html", error="User already exists")

    otp = random.randint(100000, 999999)
    session["otp"] = otp

    msg = Message(
        "Sanjeevani Sync - OTP Verification",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email]
    )
    msg.body = f"Your OTP is: {otp}"
    mail.send(msg)

    return render_template("verify.html")

@app.route("/verify", methods=["POST"])
def verify():
    entered_otp = request.form.get("otp")

    if entered_otp == str(session.get("otp")):
        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (session["name"], session["email"], session["password"])
        )
        conn.commit()
        session["status"] = "ok"
        return render_template("index.html")

    return "Invalid OTP"

# ---------- Login ----------
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logging_in", methods=["POST"])
def logging_in():
    email = request.form.get("email")
    password = request.form.get("password")

    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result and result["password"] == password:
        session["email"] = email
        session["status"] = "ok"
        return render_template("index.html")

    return "Invalid credentials"

# ---------- Medicine Scheduling ----------
@app.route("/home", methods=["POST"])
def home_page():
    medicine = request.form.get("medicine")
    time = request.form.get("time")

    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medicine_schedule (email, medicine_name, time) VALUES (%s, %s, %s)",
        (session["email"], medicine, time)
    )
    conn.commit()

    return render_template("index.html")

# ---------- ESP32 API ----------
@app.route("/get-timings", methods=["GET"])
def get_timings():
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT time FROM medicine_schedule WHERE email = %s",
        (session.get("email"),)
    )

    timings = cursor.fetchall()
    formatted_times = []

    for t in timings:
        time_data = t["time"]
        if isinstance(time_data, datetime.timedelta):
            total_seconds = time_data.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            formatted_times.append(f"{hours:02d}:{minutes:02d}")

    return jsonify(formatted_times)

# ---------- Logout ----------
@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
