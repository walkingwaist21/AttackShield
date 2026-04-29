DELIMITER $$

CREATE TRIGGER detect_sql_injection
BEFORE INSERT ON Requests_Log
FOR EACH ROW
BEGIN
    IF 
        NEW.payload LIKE '%OR 1=1%'
        OR NEW.payload LIKE '%--%'
        OR NEW.payload LIKE '%UNION SELECT%'
        OR NEW.payload LIKE '%DROP TABLE%'
        OR NEW.payload LIKE '%<script>%'
        OR NEW.payload LIKE '%../../%'
        OR NEW.payload LIKE '%; ls%'
    THEN
        SET NEW.attack_detected = TRUE;
        SET NEW.attack_id = 1;
    END IF;
END$$

DELIMITER ;
