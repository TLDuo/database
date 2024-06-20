drop procedure if exists return_loan;

DELIMITER //
CREATE procedure return_loan (IN loan_id CHAR(30), IN pay_money INT,  OUT status INT)
BEGIN
    DECLARE max_no INT DEFAULT 0;
    DECLARE next_no INT DEFAULT 0;
    DECLARE loan_remain INT DEFAULT 0;
    SET status = -1;
	IF (SELECT COUNT(*) FROM pay_list) != 0 THEN
		SELECT MAX(pay_id) FROM pay_list INTO max_no;
	END IF;
    IF NOT EXISTS(SELECT * FROM loan WHERE loan.loan_id = loan_id) THEN
		SET status = -2;
    END IF;
    IF pay_money < 0 THEN
		SET status = -3;
	END IF;
    SELECT loan.loan_remain FROM loan WHERE loan.loan_id = loan_id INTO loan_remain;
	SET next_no = max_no+1;
    IF pay_money > loan_remain THEN
		SET status = loan_remain;
	END IF;
    IF status = -1 THEN
		INSERT INTO `bank_db`.`pay_list` (`pay_id`, `loan_id`, `pay_money`, `pay_date`) VALUES (next_no, loan_id, pay_money, (Curdate()));
        -- CALL DecreaseAfterInsert(loan_id, pay_money, status);
	END IF;
END //
DELIMITER ;