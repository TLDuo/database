DROP PROCEDURE IF EXISTS delete_worker;
DELIMITER //
CREATE PROCEDURE delete_worker(IN worker_id CHAR(16), IN department_id CHAR(16), IN worker_name CHAR(16), OUT status INT)
BEGIN
    DECLARE worker_exists INT;

    SELECT COUNT(*) INTO worker_exists FROM worker w WHERE w.worker_id = worker_id AND w.department_id = department_id AND w.worker_name = worker_name;

    IF worker_exists > 0 THEN
        SET status = 2; -- 假设状态2表示找到了员工
        START TRANSACTION;
            SET FOREIGN_KEY_CHECKS = 0;
            DELETE FROM serve_list s WHERE s.worker_id = worker_id;
            DELETE FROM worker w WHERE w.worker_id = worker_id AND w.department_id = department_id AND w.worker_name = worker_name;
            SET FOREIGN_KEY_CHECKS = 1;
        COMMIT;
    ELSE
        SET status = 1; -- 假设状态1表示员工不存在
    END IF;
END //
DELIMITER ;