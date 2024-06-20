DELIMITER //
CREATE FUNCTION get_service_count(worker_id_param CHAR(16))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE service_count INT;
    SELECT COUNT(*) INTO service_count
    FROM serve_list
    WHERE worker_id = worker_id_param;
    RETURN service_count;
END //
DELIMITER ;