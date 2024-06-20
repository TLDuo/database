drop procedure if exists calculate_loan_formal;

DELIMITER //
CREATE procedure calculate_loan_formal ()
BEGIN
	DECLARE state INT DEFAULT 0;
    DECLARE curr_loan INT DEFAULT 0;
    DECLARE curr_remain INT DEFAULT 0;
    DECLARE curr_rate FLOAT DEFAULT 0;
    DECLARE curr_id INT DEFAULT 0;
    DECLARE borr_date DATE;
	DECLARE cs_loan CURSOR FOR (SELECT loan_id, loan_remain, loan_rate FROM loan);
	DECLARE cs_saving CURSOR FOR (SELECT account_id, remaining, rate FROM save_account);
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET state = 1;
    OPEN cs_loan;
    REPEAT
		FETCH cs_loan INTO curr_id, curr_loan, curr_rate;
        IF state = 0 AND curr_loan > 0 THEN
			SELECT loan_date FROM loan WHERE loan.loan_id = curr_id INTO borr_date;
			IF datediff((Curdate()), borr_date) % 30 = 0 THEN
				UPDATE  `bank_db`.`loan` SET loan.loan_remain = (curr_loan + CAST(curr_loan*curr_rate as signed)) WHERE loan.loan_id = curr_id;
			END IF;
		END IF;
        UNTIL state = 1
	END REPEAT;
    CLOSE cs_loan;
    SET state = 0;
    OPEN cs_saving;
    REPEAT
		FETCH cs_saving INTO curr_id, curr_remain, curr_rate;
        IF state = 0 THEN
			SELECT open_date FROM save_account WHERE save_account.account_id = curr_id INTO borr_date;
			IF datediff((Curdate()), borr_date) % 30 = 0 THEN
				START TRANSACTION;
				SET @enable_trigger = 0;
				UPDATE  `bank_db`.`save_account` SET save_account.remaining = (curr_remain + CAST(curr_remain*curr_rate as signed)) WHERE save_account.account_id = curr_id;
				SET @enable_trigger = 1;
                COMMIT;
			END IF;
		END IF;
        UNTIL state = 1
	END REPEAT;
    CLOSE cs_saving;
END //
DELIMITER ;