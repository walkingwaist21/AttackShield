from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="attack_logger"
)

cursor = db.cursor()

# Home page
@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        payload = request.form["payload"]
        ip = request.form["ip_address"]

        user_id = 1

        cursor.execute("""
            INSERT INTO Requests_Log (user_id, ip_address, payload)
            VALUES (%s, %s, %s)
        """, (user_id, ip, payload))

        db.commit()
        message = "Request Logged!"

    cursor.execute("""
        SELECT log_id, ip_address, payload, attack_detected
        FROM Requests_Log
        ORDER BY log_id DESC
    """)
    logs = cursor.fetchall()

    return render_template("index.html", message=message, logs=logs)


# Block IP route
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
    return "Blocked attackers!"


# Dashboard route
@app.route("/dashboard")
def dashboard():
    cursor.execute("SELECT COUNT(*) FROM Requests_Log")
    total_requests = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Requests_Log WHERE attack_detected=TRUE")
    total_attacks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Blocked_IPs")
    blocked_ips = cursor.fetchone()[0]

    cursor.execute("""
        SELECT payload, COUNT(*)
        FROM Requests_Log
        WHERE attack_detected=TRUE
        GROUP BY payload
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


if __name__ == "__main__":
    app.run(debug=True)