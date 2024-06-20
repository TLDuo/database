drop procedure if exists DecreaseAfterInsert;

DELIMITER //
CREATE PROCEDURE DecreaseAfterInsert(
    IN payLoanId INT,
    IN payMoney DECIMAL(10, 2),
    OUT status INT
)
BEGIN
    -- 更新bank表中的sum_remaining字段
    UPDATE `bank_db`.`bank`, `bank_db`.`loan` 
    SET bank.sum_remaining = bank.sum_remaining + payMoney 
    WHERE bank.bank_name = loan.bank_name AND loan.loan_id = payLoanId;
    
    -- 更新loan表中的loan_remain字段
    UPDATE loan 
    SET loan.loan_remain = (loan.loan_remain - payMoney) 
    WHERE loan.loan_id = payLoanId;
    set status = 1;
END //
DELIMITER ;
