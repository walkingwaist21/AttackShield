CREATE DATABASE attack_logger;
USE attack_logger;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(100)
);

INSERT INTO Users (username, password)
VALUES ('admin', 'admin123');

CREATE TABLE Attack_Types (
    attack_id INT PRIMARY KEY,
    attack_name VARCHAR(50),
    severity VARCHAR(20)
);

INSERT INTO Attack_Types VALUES
(1, 'SQL Injection', 'High'),
(2, 'XSS', 'Medium');

CREATE TABLE Requests_Log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    ip_address VARCHAR(50),
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload TEXT,
    attack_detected BOOLEAN DEFAULT FALSE,
    attack_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (attack_id) REFERENCES Attack_Types(attack_id)
);

CREATE TABLE Blocked_IPs (
    ip_address VARCHAR(50) PRIMARY KEY,
    reason TEXT,
    blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE TRIGGER detect_sql_injection
BEFORE INSERT ON Requests_Log
FOR EACH ROW
BEGIN
    IF NEW.payload LIKE '%OR 1=1%' OR NEW.payload LIKE '%--%' THEN
        SET NEW.attack_detected = TRUE;
        SET NEW.attack_id = 1;
    END IF;
END$$

DELIMITER ;
