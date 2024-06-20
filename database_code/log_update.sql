drop procedure if exists log_update;
DELIMITER //

CREATE procedure log_update (OUT status INT)
BEGIN
	SET status = 1;
    IF status = 1 THEN
		START TRANSACTION;
		SET SQL_SAFE_UPDATES = 0;
        UPDATE user SET log_in = 0 WHERE log_in = 1;
        SET SQL_SAFE_UPDATES = 1;
        COMMIT;
    END IF;
END //
DELIMITER ;

