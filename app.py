from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

# =========================
# DATABASE CONNECTION
# =========================
db = mysql.connector.connect(
    host="localhost",          # change to cloud DB host later
    user="root",               # change if needed
    password="",               # your mysql password
    database="attack_logger"
)

cursor = db.cursor()


# =========================
# HOME PAGE
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        payload = request.form["payload"]
        ip = request.form["ip_address"]

        user_id = 1
        attack_type = "Normal"

        payload_lower = payload.lower()

        # SQL Injection Detection
        if (
            "or 1=1" in payload_lower
            or "union" in payload_lower
            or "drop" in payload_lower
            or "select" in payload_lower
            or "--" in payload_lower
        ):
            attack_type = "SQL Injection"

        # XSS Detection
        elif "<script>" in payload_lower:
            attack_type = "XSS"

        # Path Traversal Detection
        elif "../../" in payload_lower:
            attack_type = "Path Traversal"

        # Command Injection Detection
        elif "; ls" in payload_lower:
            attack_type = "Command Injection"

        cursor.execute("""
            INSERT INTO Requests_Log (
                user_id,
                ip_address,
                payload,
                attack_type
            )
            VALUES (%s, %s, %s, %s)
        """, (user_id, ip, payload, attack_type))

        db.commit()
        message = "Request Logged Successfully!"

    cursor.execute("""
        SELECT log_id, ip_address, payload, attack_detected, attack_type
        FROM Requests_Log
        ORDER BY log_id DESC
    """)
    logs = cursor.fetchall()

    return render_template(
        "index.html",
        message=message,
        logs=logs
    )


# =========================
# BLOCK ATTACKERS
# =========================
@app.route("/block_ip")
def block_ip():
    cursor.execute("""
        INSERT IGNORE INTO Blocked_IPs (ip_address, reason)
        SELECT ip_address, 'Multiple attacks'
        FROM Requests_Log
        WHERE attack_detected = TRUE
        GROUP BY ip_address
        HAVING COUNT(*) >= 1
    """)

    db.commit()
    return "Blocked attackers successfully!"


# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():
    cursor.execute("SELECT COUNT(*) FROM Requests_Log")
    total_requests = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) 
        FROM Requests_Log 
        WHERE attack_detected = TRUE
    """)
    total_attacks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Blocked_IPs")
    blocked_ips = cursor.fetchone()[0]

    cursor.execute("""
        SELECT attack_type, COUNT(*)
        FROM Requests_Log
        GROUP BY attack_type
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    top_attack = cursor.fetchone()

    return render_template(
        "dashboard.html",
        total_requests=total_requests,
        total_attacks=total_attacks,
        blocked_ips=blocked_ips,
        top_attack=top_attack
    )


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )