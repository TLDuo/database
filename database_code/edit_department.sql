DELIMITER //
drop procedure if exists renum_department;

CREATE procedure renum_department (IN old_id CHAR(16), IN new_id CHAR(16), OUT status INT)
BEGIN
	SET status = 1;
	IF EXISTS (SELECT * FROM department WHERE department.department_id = new_id) AND old_id != new_id THEN
		SET status = 2;
	END IF;
    IF status = 1 THEN
		START TRANSACTION;
		SET FOREIGN_KEY_CHECKS = 0;
        UPDATE worker SET worker.department_id = new_id WHERE worker.department_id = old_id;
        UPDATE department SET department.department_id = new_id WHERE department.department_id = old_id;
        SET FOREIGN_KEY_CHECKS = 1;
        COMMIT;
    END IF;
END //
DELIMITER ;
