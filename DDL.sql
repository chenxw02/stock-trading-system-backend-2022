create table admin (
    admin_id varchar(20) not null,
    password varchar(200) not null,
    primary key (admin_id)
);
create table admin_permission (
    admin_id varchar(20) not null,
    stock_id varchar(20) not null,
    primary key (admin_id, stock_id),
    foreign key (admin_id) REFERENCES admin(admin_id),
    foreign key (stock_id) REFERENCES stock(stock_id)
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
    status varchar(2) not null,
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
    status varchar(2) not null,
    primary key (l_account_number)
);
create table fund_account (
    fund_account_number varchar(20) not null,
    balance double not null,
    frozen double not null,
    taken double not null,
    trade_password varchar(200) not null,
    login_password varchar(200) not null,
    account_status varchar(4) not null,
    securities_account_number varchar(20) not null,
    check account_status in ("ok","no"),
    primary key (fund_account_number)
);
create table own_stock (
    stock_id varchar(20) not null,
    securities_account_number varchar(20) not null,
    own_number int not null,
    frozen int not null,
    own_amount double not null,
    primary key (stock_id,securities_account_number)
);
create table deal(
    deal_id int not null,
    securities_account_number varchar(20) not null,
    person_id varchar(18) not null,
    status varchar(10) not null,
    event varchar(10),
    primary key (deal_id)
);
create table stock
(
    stock_id       varchar(20) not null,
    stock_name     varchar(20) not null,
    remain_number  int         not null,
    price          double      not null,
    stock_type     char(1)     not null,
    stock_status   char(1)     not null,
    rise_threshold double      not null,
    fall_threshold double      not null,
    primary key (stock_id),
    check (stock_type in ('S', 'N')),
    check (stock_status in ('T', 'F'))
);
create table instruction
(
    instruction_id      int         not null,
    stock_id            varchar(20) not null,
    fund_account_number varchar(20) not null,
    buy_sell_flag       char(1)     not null,
    target_number       int         not null,
    actual_number       int         not null,
    target_price        double      not null,
    total_amount        double      not null,
    time                int         not null,
    instruction_state   char(1)     not null,
    primary key (instruction_id),
    foreign key (stock_id) references stock (stock_id),
    foreign key (fund_account_number) references fund_account (fund_account_number),
    check (buy_sell_flag in ('B', 'S')),
    check (instruction_state in ('N', 'P', 'T', 'E'))
    /* N是未成交，P是部分成交，T是完全成交，E是过期失效 */
);
create table k
(
    k_id          varchar(20) not null,
    stock_id      varchar(20) not null,
    start_price   double,
    end_price     double,
    highest_price double,
    lowest_price  double,
    trade_number  int         not null,
    trade_amount  double      not null,
    date          int         not null,
    primary key (k_id),
    foreign key (stock_id) references stock(stock_id)
);
create table transaction
(
    transaction_id      varchar(20) not null,
    stock_id            varchar(20) not null,
    instruction_id      varchar(20) not null,
    fund_account_number varchar(20) not null,
    buy_sell_flag       char(1)     not null,
    transaction_price   double      not null,
    transaction_amount  double      not null,
    transaction_number  int         not null,
    transaction_date    int         not null,
    transaction_time    int         not null,
    primary key (transaction_id),
    foreign key (stock_id) references stock(stock_id),
    foreign key (instruction_id) references instruction(instruction_id),
    foreign key (fund_account_number) references fund_account(fund_account_number),
    check (buy_sell_flag in ('B', 'S'))
);
create table queryuser
(
  ID varchar(20) not null,
  password varchar(200) not null,
  authority char(1) not null,
  primary key(ID)
);
create table  payaccount (
  pay_account_id varchar(20) not null,
  pay_account_psw varchar(200) not null,
  balance int not null,
  primary key (pay_account_id)
);