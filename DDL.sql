create table admin (
    admin_id varchar(20) not null,
    password varchar(200) not null,
    primary key (admin_id)
);
create table administrator_account (
    administrator_id varchar(20) not null,
    administrator_password varchar(200) not null,
    primary key (administrator_id)
);
create table personal_securities_account (
    p_account_number varchar(20) not null,
    password varchar(200) not null,
    user_name varchar(50) not null,
    user_gender varchar(1) not null,
    registration_date int not null,
    user_id_number varchar(18) not null,
    user_address varchar(100) not null,
    user_job varchar(100) not null,
    user_education varchar(20) not null,
    user_work_unit varchar(100) not null,
    telephone varchar(11) not null,
    agent boolean not null,
    agent_id varchar(18),
    authority varchar(3),
    primary key (p_account_number)
);
create table legal_person_securities_account (
    l_account_number varchar(20) not null,
    password varchar(200) not null,
    legal_person_registration_number varchar(18) not null,
    business_license_number varchar(15) not null,
    legal_person_id_number varchar(18) not null,
    legal_person_name varchar(50) not null,
    legal_person_telephone varchar(11) not null,
    legal_person_address varchar(100) not null,
    excutor varchar(50) not null,
    authorized_person_id_number varchar(18) not null,
    authorized_person_telephone varchar(11) not null,
    authorized_person_address varchar(100) not null,
    authority varchar(3) not null,
    primary key (l_account_number)
);
create table fund_account (
    fund_account_number varchar(20) not null,
    balance double not null,
    frozen double not null,
    taken double not null,
    trade_password varchar(200) not null,
    login_password varchar(200) not null,
    login_status boolean not null,
    account_status varchar(4) not null,
    securities_account_number varchar(20) not null,
    primary key (fund_account_number)
);
create table own_stock (
    stock_id varchar(20) not null,
    securities_account_number varchar(20) not null,
    own_number int not null,
    frozen int not null,
    own_amount double not null,
    primary key (stock_id)
);
create table deal(
    deal_id int not null,
    securities_account_number varchar(20) not null,
    person_id varchar(18) not null,
    status varchar(10) not null,
    event varchar(10),
    primary key (deal_id)
)