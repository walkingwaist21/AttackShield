🔐 AttackShield

Real-Time SQL Injection Detection and Attack Logging System

📌 Overview

AttackShield is a cybersecurity-focused DBMS project that detects and logs SQL injection attacks in real-time using MySQL triggers and a Flask-based web interface.

It simulates how modern systems monitor malicious payloads and block repeated attackers.

⸻

🚀 Features
	•	Detects SQL Injection patterns (' OR 1=1 --)
	•	Logs all incoming requests
	•	Automatically marks malicious payloads
	•	Blocks IP addresses after repeated attacks
	•	Displays logs via a web interface

⸻

🛠️ Tech Stack
	•	Python (Flask)
	•	MySQL
	•	HTML/CSS

    📁 Project Setup

1️⃣ Clone the repository

git clone https://github.com/walkingwaist21/AttackShield
cd AttackShield

2️⃣ Install dependencies

pip3 install -r requirements.txt

3️⃣ Setup MySQL Database

mysql -u root

Run the SQL file:

SOURCE /full/path/to/db.sql;

4️⃣ Run the application

python3 app.py

5️⃣ Open in browser

http://127.0.0.1:5000

🧪 Demo

Normal Input
	•	Username: admin
	•	Payload: hello

➡️ Output: Attack = NO

⸻

Attack Input
	•	Username: admin
	•	Payload:
    ' OR 1=1 --
➡️ Output: Attack = YES

⸻

🚫 Blocking Attackers

Click “Block Attackers” to block IPs with repeated malicious activity.

Check blocked IPs:SELECT * FROM Blocked_IPs;

🧠 How It Works
	•	A MySQL trigger scans payloads before insertion
	•	If suspicious patterns are found → marks as attack
	•	Aggregation query blocks IPs after multiple attacks

⸻

📌 Future Enhancements
	•	XSS detection
	•	Dashboard with graphs
	•	Integration with Burp Suite
	•	Machine learning-based anomaly detection

⸻

👨‍💻 Author

Dushanth Purushotham