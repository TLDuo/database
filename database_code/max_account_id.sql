drop procedure if exists max_account_id;
DELIMITER //

CREATE procedure max_account_id (OUT status INT)
BEGIN
	DECLARE max_no INT DEFAULT 0;
	set status = -1;
	IF (SELECT COUNT(*) FROM account) != 0 THEN
		START TRANSACTION;
		SELECT MAX(account_id) FROM account INTO max_no;
		SET status = max_no+1;
		COMMIT;
	END IF;
END //
DELIMITER ;
