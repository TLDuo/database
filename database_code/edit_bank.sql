DELIMITER //
drop procedure if exists bank_rename;

CREATE procedure bank_rename (IN old_name CHAR(16), IN new_name CHAR(16), OUT status INT)
BEGIN
	SET status = 1;
	IF EXISTS (SELECT * FROM bank WHERE bank.bank_name = new_name) AND old_name != new_name THEN
		SET status = 2;
	END IF;
    IF status = 1 THEN
		START TRANSACTION;
		SET FOREIGN_KEY_CHECKS = 0;
        UPDATE department SET department.bank_name = new_name WHERE department.bank_name = old_name;
        UPDATE loan SET loan.bank_name = new_name WHERE loan.bank_name = old_name;
        UPDATE account SET account.bank_name = new_name WHERE account.bank_name = old_name;
        UPDATE credit_account SET credit_account.bank_name = new_name WHERE credit_account.bank_name = old_name;
        UPDATE save_account SET save_account.bank_name = new_name WHERE save_account.bank_name = old_name;
        UPDATE bank SET bank.bank_name = new_name WHERE bank.bank_name = old_name;
        SET FOREIGN_KEY_CHECKS = 1;
        COMMIT;
    END IF;
END //
DELIMITER ;

drop procedure if exists edit_bank;
DELIMITER //
CREATE procedure edit_bank (IN bank_name CHAR(16), IN bank_location CHAR(16), IN asset INT, OUT status INT)
BEGIN
	SET status = 1;
	IF status = 1 AND asset < 0 THEN
		SET status = 2;
	END IF;
	IF status = 1 THEN
		UPDATE bank b SET b.city = bank_location, b.sumremaining = asset WHERE b.bank_name = bank_name;
	END IF;
END //
DELIMITER ;