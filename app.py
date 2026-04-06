from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="attack_logger"
)

cursor = db.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        payload = request.form["payload"]
        ip = request.remote_addr

        cursor.execute("SELECT user_id FROM Users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user:
            user_id = user[0]

            cursor.execute("""
                INSERT INTO Requests_Log (user_id, ip_address, payload)
                VALUES (%s, %s, %s)
            """, (user_id, ip, payload))

            db.commit()
            message = "Request Logged!"

        else:
            message = "User not found!"

    cursor.execute("""
        SELECT log_id, ip_address, payload, attack_detected 
        FROM Requests_Log 
        ORDER BY log_id DESC
    """)
    logs = cursor.fetchall()

    return render_template("index.html", message=message, logs=logs)


@app.route("/block_ip")
def block_ip():
    cursor.execute("""
        INSERT IGNORE INTO Blocked_IPs (ip_address, reason)
        SELECT ip_address, 'Multiple attacks'
        FROM Requests_Log
        WHERE attack_detected = TRUE
        GROUP BY ip_address
        HAVING COUNT(*) >= 2
    """)
    db.commit()
    return "Blocked attackers!"


if __name__ == "__main__":
    app.run(debug=True)
