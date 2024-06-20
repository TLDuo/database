/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2024/6/2 17:52:07                            */
/*==============================================================*/

-- create library
drop
    database if exists bank_db;
create
    database bank_db;
use
    bank_db;

drop table if exists account;

drop table if exists bank;

drop table if exists credit_account;

drop table if exists customer;

drop table if exists department;

drop table if exists loan;

drop table if exists pay_list;

drop table if exists save_account;

drop table if exists serve_list;

drop table if exists worker;

/*==============================================================*/
/* Table: bank                                                  */
/*==============================================================*/
create table bank
(
   bank_name            varchar(16) not null,
   city                 varchar(16) not null,
   sum_remaining        int,
   primary key (bank_name)
);

/*==============================================================*/
/* Table: customer                                              */
/*==============================================================*/
create table customer
(
   client_name                 varchar(16) not null,
   client_number        varchar(16) not null,
   client_address       varchar(64) not null,
   client_person_id     varchar(20) not null,
   client_sex           char(1) not null,
   primary key (client_person_id)
);

/*==============================================================*/
/* Table: account                                               */
/*==============================================================*/
create table account
(
   account_id           int not null,
   client_person_id     varchar(20) not null,
   bank_name            varchar(16) not null,
   password             varchar(20) not null,
   remaining            int not null,
   open_date            date,
   primary key (account_id),
   constraint FK_create foreign key (bank_name)
      references bank (bank_name) on delete restrict on update restrict,
   constraint FK_own foreign key (client_person_id)
      references customer (client_person_id) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: credit_account                                        */
/*==============================================================*/
create table credit_account
(
   account_id           int not null,
   person_id            varchar(20),
   bank_name            varchar(16),
   password             varchar(20) not null,
   remaining            int not null,
   open_date            date,
   credit               int not null,
   primary key (account_id),
   constraint FK_信用 foreign key (account_id)
      references account (account_id) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: department                                            */
/*==============================================================*/
create table department
(
   department_id         varchar(16) not null,
   bank_name            varchar(16) not null,
   department_name      varchar(16) not null,
   department_type      varchar(16) not null,
   primary key (department_id),
   constraint FK_include foreign key (bank_name)
      references bank (bank_name) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: loan                                                  */
/*==============================================================*/
create table loan
(
   loan_id              varchar(16) not null,
   bank_name            varchar(16) not null,
   client_person_id     varchar(20) not null,
   loan_total           int not null,
   loan_remain          int not null,
   loan_date            date not null,
   loan_rate            float not null,
   primary key (loan_id),
   constraint FK_lend_credit foreign key (client_person_id)
      references customer (client_person_id) on delete restrict on update restrict,
   constraint FK_lend_bank foreign key (bank_name)
      references bank (bank_name) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: pay_list                                              */
/*==============================================================*/
create table pay_list
(
   pay_id               varchar(30) not null,
   loan_id              varchar(16) not null,
   pay_money            int not null,
   pay_date             date not null,
   primary key (pay_id),
   constraint FK_pay foreign key (loan_id)
      references loan (loan_id) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: save_account                                          */
/*==============================================================*/
create table save_account
(
   account_id           int not null,
   person_id            varchar(20),
   bank_name            varchar(16),
   password             varchar(20) not null,
   remaining            int not null,
   open_date            date,
   rate                 float not null,
   primary key (account_id),
   constraint FK_save foreign key (account_id)
      references account (account_id) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: worker                                                */
/*==============================================================*/
create table worker
(
   worker_id            varchar(16) not null,
   department_id        varchar(16) not null,
   worker_name          varchar(16) not null,
   worker_sex           char(1) not null,
   worker_person_id     varchar(20) not null,
   worker_level         varchar(16) not null,
   worker_number        varchar(16) not null,
   worker_address       varchar(64) not null,
   primary key (worker_id),
   constraint FK_belong foreign key (department_id)
      references department (department_id) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: serve_list                                            */
/*==============================================================*/
create table serve_list
(
   worker_id            varchar(16) not null,
   client_person_id     varchar(20) not null,
   serve_date           date not null,
   serve_type           varchar(16) not null,
   constraint FK_serve_list foreign key (worker_id)
      references worker (worker_id) on delete restrict on update restrict,
   constraint FK_serve_list2 foreign key (client_person_id)
      references customer (client_person_id) on delete restrict on update restrict
);

