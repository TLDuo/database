drop procedure if exists borrow_loan;

DELIMITER //
CREATE procedure borrow_loan (IN client_id CHAR(18), IN bank_name CHAR(30), IN loan_total INT, IN loan_rate FLOAT,  OUT status INT)
BEGIN
    DECLARE max_no INT DEFAULT 0;
    DECLARE next_no INT DEFAULT 0;
    DECLARE test_id INT DEFAULT 0;
    DECLARE test INT DEFAULT 0;
	SET status = 1;
    SET test_id = Length(client_id);
    IF NOT EXISTS(SELECT * FROM customer WHERE customer.client_person_id = client_id) THEN
		SET status = 2;
	END IF;
    IF loan_total < 0 OR loan_rate < 0.0 THEN
		SET status = 6;
	END IF;
    IF status = 1 AND EXISTS(SELECT * FROM loan Where client_id = loan.client_person_id AND bank_name = loan.bank_name AND loan_remain > 0 )  THEN
		SET status = 3;
	END IF;
	IF (SELECT COUNT(*) FROM loan) != 0 THEN
		SELECT MAX(loan_id) FROM loan INTO max_no;
	END IF;
	SET next_no = max_no+1;
    IF status = 1 AND loan_total > (SELECT bank.sum_remaining FROM bank Where bank.bank_name = bank_name) THEN
		SET status = 4;
	END IF;
	IF status = 1 AND NOT EXISTS(SELECT * FROM bank WHERE bank.bank_name = bank_name) THEN
		SET status = 5;
	END IF;
    IF status = 1 THEN
		if EXISTS(SELECT loan_id FROM loan Where client_id = loan.client_person_id AND bank_name = loan.bank_name AND loan_remain = 0)  THEN
			SELECT loan_id FROM loan Where client_id = loan.client_person_id AND bank_name = loan.bank_name AND loan_remain = 0 into test;
            DELETE FROM pay_list WHERE loan_id = test;
			UPDATE loan SET loan.loan_id = next_no Where loan.loan_id = loan_id AND bank_name = loan.bank_name;
			UPDATE loan SET loan.loan_remain = loan_total Where loan.loan_id = loan_id AND bank_name = loan.bank_name;
            UPDATE loan SET loan.loan_total = loan_total Where loan.loan_id = loan_id AND bank_name = loan.bank_name;
            UPDATE loan SET loan.loan_date = (Curdate()) Where loan.loan_id = loan_id AND bank_name = loan.bank_name;
            UPDATE loan SET loan.loan_rate = loan_rate Where loan.loan_id = loan_id AND bank_name = loan.bank_name;
        else
			INSERT INTO `bank_db`.`loan` (`loan_id`, `client_person_id`, `bank_name`, `loan_total`, `loan_remain`, `loan_date`, `loan_rate`) VALUES (next_no, client_id, bank_name, loan_total, loan_total, (Curdate()), loan_rate);
        end if;
		UPDATE `bank_db`.`bank` SET sum_remaining = sum_remaining - loan_total WHERE bank.bank_name = bank_name;
	END IF;
END //
DELIMITER ;