set foreign_key_checks=0;
INSERT INTO `bank_db`.`bank` (`bank_name`, `city`, `sum_remaining`) VALUES ('xx1支行', '合肥', '20000000');
INSERT INTO `bank_db`.`bank` (`bank_name`, `city`, `sum_remaining`) VALUES ('xx2支行', '上海', '20000000');
INSERT INTO `bank_db`.`bank` (`bank_name`, `city`, `sum_remaining`) VALUES ('鲜血王朝', '交界地', '20000000');

INSERT INTO `bank_db`.`department` (`department_id`, `bank_name`, `department_name`, `department_type`) VALUES ('1', 'xx1支行', '服务部门', '服务');
INSERT INTO `bank_db`.`department` (`department_id`, `bank_name`, `department_name`, `department_type`) VALUES ('2', 'xx1支行', '记账部门', '记账');
INSERT INTO `bank_db`.`department` (`department_id`, `bank_name`, `department_name`, `department_type`) VALUES ('3', 'xx2支行', '服务部门', '服务');
INSERT INTO `bank_db`.`department` (`department_id`, `bank_name`, `department_name`, `department_type`) VALUES ('4', 'xx2支行', '记账部门', '记账');
INSERT INTO `bank_db`.`department` (`department_id`, `bank_name`, `department_name`, `department_type`) VALUES ('5', '鲜血王朝', '服务部门', '捐钱');

INSERT INTO `bank_db`.`worker` (`worker_id`, `department_id`, `worker_name`, `worker_sex`, `worker_person_id`, `worker_number`, `worker_address`, `worker_level`) VALUES ('1', '1', '星', 'W', '100000000000000001', '10000000001', '星穹列车','7');
INSERT INTO `bank_db`.`worker` (`worker_id`, `department_id`, `worker_name`, `worker_sex`, `worker_person_id`, `worker_number`, `worker_address`, `worker_level`) VALUES ('2', '2', '褪色者', 'M', '100000000000000000', '20000000000', '交界地',  '8');
INSERT INTO `bank_db`.`worker` (`worker_id`, `department_id`, `worker_name`, `worker_sex`, `worker_person_id`, `worker_number`, `worker_address`, `worker_level`) VALUES ('3', '3', 'go', 'M', '200000000000000000', '12300000001', '下北泽',  '7');
INSERT INTO `bank_db`.`worker` (`worker_id`, `department_id`, `worker_name`, `worker_sex`, `worker_person_id`, `worker_number`, `worker_address`, `worker_level`) VALUES ('4', '4', '月村手毬', 'W', '200000000000000001', '12300000002', '初星学园', '7');
INSERT INTO `bank_db`.`worker` (`worker_id`, `department_id`, `worker_name`, `worker_sex`, `worker_person_id`, `worker_number`, `worker_address`, `worker_level`) VALUES ('5', '1', '藤丸立香', 'M', '100000000000000011', '10000000000', '迦勒底', '1');
INSERT INTO `bank_db`.`worker` (`worker_id`, `department_id`, `worker_name`, `worker_sex`, `worker_person_id`, `worker_number`, `worker_address`, `worker_level`) VALUES ('6', '4', 'u-official', 'W', '200000000000000022', '12300000000', '罗德塔', '2');
INSERT INTO `bank_db`.`worker` (`worker_id`, `department_id`, `worker_name`, `worker_sex`, `worker_person_id`, `worker_number`, `worker_address`, `worker_level`) VALUES ('7', '5', '蒙格', 'M', '200000000000000023', '12300000001', '交界地', '1');

INSERT INTO `bank_db`.`customer` (`client_person_id`, `client_name`, `client_number`, `client_address`, `client_sex`) VALUES ('123123200203150000', '藤田琴音', '11223344556', '初星学院', 'W');
INSERT INTO `bank_db`.`customer` (`client_person_id`, `client_name`, `client_number`, `client_address`, `client_sex`) VALUES ('234234000000000000', '艾蕾什基嘉尔', '12345123456', '迦勒底', 'W');
INSERT INTO `bank_db`.`customer` (`client_person_id`, `client_name`, `client_number`, `client_address`, `client_sex`) VALUES ('280800000000000000', '田所浩二', '12345678901', '下北沢', 'M');
INSERT INTO `bank_db`.`customer` (`client_person_id`, `client_name`, `client_number`, `client_address`, `client_sex`) VALUES ('302300000000000000', '流萤', '12345678909', '星核猎手', 'W');

INSERT INTO `bank_db`.`loan` (`loan_id`, `client_person_id`, `bank_name`, `loan_total`, `loan_remain`, `loan_date`, `loan_rate`) VALUES ('10', '302300000000000000', 'xx1支行', '10000', '10000', '2022-11-11', '0.05');

INSERT INTO `bank_db`.`pay_list` (`pay_id`, `loan_id`, `pay_money`, `pay_date`) VALUES ('11', '10', '1000', '2022-12-12');
INSERT INTO `bank_db`.`pay_list` (`pay_id`, `loan_id`, `pay_money`, `pay_date`) VALUES ('12', '10', '3000', '2023-3-1');

INSERT INTO `bank_db`.`account` (`account_id`, `client_person_id`, `bank_name`, `password`, `remaining`, `open_date`) VALUES ('1', '123123200203150000', 'xx1支行', '123123', '3000', '2023-3-1');
INSERT INTO `bank_db`.`account` (`account_id`, `client_person_id`, `bank_name`, `password`, `remaining`, `open_date`) VALUES ('2', '280800000000000000', 'xx1支行', '123456', '5000', '2023-2-1');
INSERT INTO `bank_db`.`credit_account` (`account_id`, `person_id`, `bank_name`, `password`, `remaining`, `open_date`, `credit`) VALUES ('1', '123123200203150000', 'xx1支行', '123123', '3000', '2023-3-1', '10000');

INSERT INTO `bank_db`.`save_account` (`account_id`, `person_id`, `bank_name`, `password`, `remaining`, `open_date`, `rate`) VALUES ('2', '280800000000000000', 'xx1支行', '123456', '5000', '2023-2-1', '0.03');

drop table if exists user;

CREATE table user
(  
   username            char(20)                       not null,
   password        char(20)                       not null,
   log_in  char(1) ,
   constraint pk_user primary key (username)
) ;
drop table if exists images;
CREATE TABLE images 
(
	username            char(20)                       not null,
	image_path VARCHAR(255)
);

INSERT INTO `bank_db`.`images` (`username`, `image_path`) VALUES ('admin', '../static/images/1707496853306.jpg');
INSERT INTO `bank_db`.`images` (`username`, `image_path`) VALUES ('user', '../static/images/1707496853306.jpg');

INSERT INTO `bank_db`.`user` (`username`, `password`,`log_in`) VALUES ('admin', '123456', '0');
INSERT INTO `bank_db`.`user` (`username`, `password`,`log_in`) VALUES ('user', '111111', '0');
set foreign_key_checks=1;