drop trigger if exists Decrease;
drop trigger if exists credit_bank;
drop trigger if exists save_bank;


DELIMITER //
CREATE trigger Decrease AFTER Insert ON pay_list FOR EACH ROW 
BEGIN
	UPDATE loan SET loan.loan_remain = (loan.loan_remain - NEW.Pay_money) Where loan.loan_id = NEW.loan_id;
	UPDATE `bank_db`.`bank`, `bank_db`.`loan` SET sum_remaining = sum_remaining + NEW.pay_money WHERE bank.bank_name = loan.bank_name AND loan.loan_id = NEW.loan_id;
END //
DELIMITER ;

DELIMITER //
CREATE trigger credit_bank AFTER UPDATE ON credit_account FOR EACH ROW 
BEGIN
	IF @enable_trigger = 1 THEN
		UPDATE `bank_db`.`bank` SET sum_remaining = sum_remaining - NEW.remaining + OLD.remaining WHERE bank.bank_name = NEW.bank_name;
	END IF;
END //
DELIMITER ;

DELIMITER //
CREATE trigger save_bank AFTER UPDATE ON save_account FOR EACH ROW 
BEGIN
	IF @enable_trigger = 1 THEN
		UPDATE `bank_db`.`bank` SET sum_remaining = sum_remaining + NEW.remaining - OLD.remaining WHERE bank.bank_name = NEW.bank_name;
    END IF;
END //
DELIMITER ;



