import jwt
import time
import bcrypt
from config import jwt_secret_key
from error.invalid_account import InvalidAccountError, NoneAccountError, FrozenAccountError, ConditionNotMeetError, \
    NoSecuritiesError, MulOpenAccountError, WithFundAccountError
from error.wrong_money import NoMoneyError, MinusMoneyError, RemainMoneyError
from dao.account_admin_dao import AccountAdminDao
from model.account_admin import AccountAdmin
from model.account_admin import PersonalSecuritiesAccount
from model.account_admin import LegalPersonSecuritiesAccount
from model.account_admin import FundAccount
from model.account_admin import OwnStock


class AccountAdminService:
    @staticmethod
    def login(administrator_id, administrator_password):
        account_admin = AccountAdminDao.get(administrator_id)
        if account_admin is None:
            raise InvalidAccountError()
        encrypted_password = account_admin.administrator_password
        if not bcrypt.checkpw(administrator_password.encode("utf-8"), encrypted_password.encode("utf-8")):
            raise InvalidAccountError()
            # raise 以返回账号密码错误
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        # 设置超时时间：当前时间的30分钟以后超时
        exp = int(time.time() + 60 * 30)
        payload = {
            "administrator_id": administrator_id,
            "type": "account_admin",
            "exp": exp
        }
        token = jwt.encode(payload=payload, key=jwt_secret_key, algorithm='HS256', headers=headers)
        return token

    @staticmethod
    def show_deal():
        result = []
        temp_deal = AccountAdminDao.get_deals()
        print(type(temp_deal))
        for temp in temp_deal:
            temp_result = {}
            temp_result["deal_id"] = temp.deal_id
            temp_result["status"] = temp.status
            temp_result["person_id"] = temp.person_id
            result.append(temp_result)
        print("dxp:")
        print(result)
        return result

    # 添加个人证券账户
    @staticmethod
    def add_personal_securities_account(account_data):
        account_information = []
        print(account_data)
        password = account_data["password"].encode('utf-8')
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        no_p_account_number = "p_" + account_data["p_account_number"]
        temp_registration_date = int("".join(account_data["registration_date"].split('-')))
        print(temp_registration_date)
        # 验证是否重复开设
        temp_user_id_number = account_data["user_id_number"].encode('utf-8')
        judge = AccountAdminDao.get_personal_by_id(temp_user_id_number)
        if judge is not None:
            # 该身份证号已经有账户
            raise MulOpenAccountError()

        account_information.append(PersonalSecuritiesAccount( \
            p_account_number=no_p_account_number, \
            password=encrypted_password, \
            user_name=account_data["user_name"].encode('utf-8'), \
            user_gender=account_data["user_gender"].encode('utf-8'), \
            registration_date=temp_registration_date, \
            user_id_number=account_data["user_id_number"].encode('utf-8'), \
            user_address=account_data["user_address"].encode('utf-8'), \
            user_job=account_data["user_job"].encode('utf-8'), \
            user_education=account_data["user_education"].encode('utf-8'), \
            user_work_unit=account_data["user_work_unit"].encode('utf-8'), \
            telephone=account_data["telephone"].encode('utf-8'), \
            agent=account_data["agent"], \
            agent_id=account_data["agent_id"].encode('utf-8'), \
            authority=account_data["authority"].encode('utf-8'), \
            status="ok"
        ))
        print(account_information)
        AccountAdminDao.insert(account_information)

    # 添加法人证券账户
    @staticmethod
    def add_legal_person_securities_account(account_data):
        account_information = []
        print(account_data)
        password = account_data["password"].encode('utf-8')
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        no_l_account_number = "l_" + account_data["l_account_number"]
        # 验证是否重复开设
        temp_legal_person_registration_number = account_data["legal_person_registration_number"].encode('utf-8')
        judge = AccountAdminDao.get_legal_person_by_id(temp_legal_person_registration_number)
        if judge is not None:
            # 该法人注册登记号已经有账户
            raise MulOpenAccountError()

        account_information.append(LegalPersonSecuritiesAccount( \
            l_account_number=no_l_account_number, \
            password=encrypted_password, \
            legal_person_registration_number=account_data["legal_person_registration_number"].encode('utf-8'), \
            business_license_number=account_data["business_license_number"].encode('utf-8'), \
            legal_person_id_number=account_data["legal_person_id_number"].encode('utf-8'), \
            legal_person_name=account_data["legal_person_name"].encode('utf-8'), \
            legal_person_telephone=account_data["legal_person_telephone"].encode('utf-8'), \
            legal_person_address=account_data["legal_person_address"].encode('utf-8'), \
            excutor=account_data["excutor"].encode('utf-8'), \
            authorized_person_id_number=account_data["authorized_person_id_number"].encode('utf-8'), \
            authorized_person_telephone=account_data["authorized_person_telephone"].encode('utf-8'), \
            authorized_person_address=account_data["authorized_person_address"].encode('utf-8'), \
            authority=account_data["authority"].encode('utf-8'), \
            status="ok"
        ))
        AccountAdminDao.insert(account_information)

    # 实际并没有这个接口开放，可以事先开放插入管理员之后关闭它
    @staticmethod
    def register(admins_data):
        account_admins = []
        password = admins_data["administrator_password"].encode('utf-8')
        print(password)
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        print(encrypted_password)
        account_admins.append(
            AccountAdmin(administrator_id=admins_data["administrator_id"], administrator_password=encrypted_password))
        AccountAdminDao.insert(account_admins)

    # 添加一个资金账户，合法返回“ok"，否则返回"failed"
    @staticmethod
    def add_fund_account(fund_account_data):
        account_information = []
        temp_securities_account_number = fund_account_data["securities_account_number"]
        temp_label = fund_account_data["label"]

        if temp_label == "0":  # 法人
            temp_securities_account_number = "l_" + temp_securities_account_number
        else:   # 个人
            temp_securities_account_number = "p_" + temp_securities_account_number

        if AccountAdminDao.check_fund_account(temp_securities_account_number) == 0:
            raise NoSecuritiesError()
        trade_password = fund_account_data["trade_password"].encode('utf-8')
        encrypted_trade_password = bcrypt.hashpw(trade_password, bcrypt.gensalt())
        login_password = fund_account_data["login_password"].encode('utf-8')
        encrypted_login_password = bcrypt.hashpw(login_password, bcrypt.gensalt())
        account_information.append(FundAccount(fund_account_number=fund_account_data["fund_account_number"],
                                               balance=0, frozen=0,
                                               taken=0,
                                               trade_password=encrypted_trade_password,
                                               login_password=encrypted_login_password,
                                               account_status="ok",
                                               securities_account_number=temp_securities_account_number))
        AccountAdminDao.insert(account_information)
        print(account_information)

    # 资金账户存取款
    @staticmethod
    def modify_money(data):
        fund_account_number = data["fund_account_number"]
        input_trade_password = data["trade_password"].encode('utf-8')
        add_withdraw = data["add_withdraw"]
        operating_num = int(data["operating_num"])
        if operating_num <= 0:
            # 存取款金额小于等于0
            raise MinusMoneyError()
        fund_account = AccountAdminDao.get_fund(fund_account_number)
        if fund_account is None:
            # 找不到账户
            raise NoneAccountError()
        encrypted_password = fund_account.trade_password
        if not bcrypt.checkpw(input_trade_password, encrypted_password.encode("utf-8")):
            # 账户密码不匹配
            raise InvalidAccountError()
        if fund_account.account_status == "no":
            # 账户已被冻结
            raise FrozenAccountError()
        if add_withdraw == 0:
            # 存款
            AccountAdminDao.fund_save_money(operating_num, fund_account)
        else:
            # 取款
            if operating_num <= fund_account.balance:
                AccountAdminDao.fund_take_money(operating_num, fund_account)
            else:
                # 取款，钱不够
                raise NoMoneyError()

    # 资金账户修改密码
    @staticmethod
    def fund_change_password(data):
        fund_account_number = data["fund_account_number"]
        trade_withdraw = data["trade_withdraw"]
        old_input_password = data["old_password"].encode('utf-8')
        new_input_password = data["new_password"].encode('utf-8')
        fund_account = AccountAdminDao.get_fund(fund_account_number)
        if fund_account is None:
            # 没有该number的资金账户
            raise NoneAccountError()
        if trade_withdraw == 0:
            encrypted_password = fund_account.trade_password
        else:
            encrypted_password = fund_account.login_password
        if not bcrypt.checkpw(old_input_password, encrypted_password.encode("utf-8")):
            # 密码错误
            raise InvalidAccountError()
        password = bcrypt.hashpw(new_input_password, bcrypt.gensalt())
        AccountAdminDao.fund_password(password, fund_account, trade_withdraw)

    # 资金账户销户
    @staticmethod
    def fund_delete(data):
        id_num_legal_register_num = data["id_num/legal_register_num"]
        security_num = data["security_num"]
        label = data["label"]
        if label == 0:
            security_num = "l_" + security_num
        else:
            security_num = "p_" + security_num

        if security_num[0] == 'p':
            security_account = AccountAdminDao.get_personal(security_num)
            if security_account is None:
                # 没有该资金账户
                raise NoneAccountError()
            else:
                if id_num_legal_register_num != security_account.user_id_number:
                    # 个人证券账户与用户身份证不匹配
                    raise InvalidAccountError()
        elif security_num[0] == 'l':
            security_account = AccountAdminDao.get_legal(security_num)
            if security_account is None:
                # 没有该资金账户
                raise NoneAccountError()
            else:
                if id_num_legal_register_num != security_account.legal_person_id_number:
                    # 法人证券账户与用户身份证不匹配
                    raise InvalidAccountError()
        else:
            # account命名问题
            raise InvalidAccountError()
        fund_account = AccountAdminDao.get_fund_by_security(security_num)
        if fund_account is None:
            # 该证券账户没有绑定资金账户
            raise NoneAccountError()
        if fund_account.balance > 0:
            # 该资金账户尚有存款
            raise RemainMoneyError()
        AccountAdminDao.fund_delete_one(fund_account)
        AccountAdminDao.security_froze(security_account)

    # 个人证券账户冻结
    @staticmethod
    def personal_security_freeze(data):
        id_num = data["id_num"]
        security_account = AccountAdminDao.get_personal_by_id(id_num)
        if security_account is None:
            # 身份证号码无效
            raise NoneAccountError()
        else:
            AccountAdminDao.security_froze(security_account)

    # 个人证券账户解冻
    @staticmethod
    def personal_security_thaw(data):
        id_num = data["id_num"]
        security_account = AccountAdminDao.get_personal_by_id(id_num)
        if security_account is None:
            # 身份证号码无效
            raise NoneAccountError()
        else:
            AccountAdminDao.security_thaw(security_account)

    # 法人证券账户冻结
    @staticmethod
    def legal_person_security_freeze(data):
        legal_register_num = data["legal_register_num"]
        security_account = AccountAdminDao.get_legal_person_by_id(legal_register_num)
        if security_account is None:
            # 身份证号码无效
            raise InvalidAccountError()
        else:
            AccountAdminDao.security_froze(security_account)

    # 法人证券账户解冻
    @staticmethod
    def legal_person_security_thaw(data):
        legal_register_num = data["legal_register_num"]
        security_account = AccountAdminDao.get_legal_person_by_id(legal_register_num)
        if security_account is None:
            # 身份证号码无效
            raise InvalidAccountError()
        else:
            AccountAdminDao.security_thaw(security_account)

    # 资金账户冻结
    @staticmethod
    def fund_freeze(data):
        id_num_legal_register_num = data["id_num/legal_register_num"]
        security_num = data["security_num"]

        label = data["label"]
        if label == 0:
            security_num = "l_" + security_num
        else:
            security_num = "p_" + security_num

        if security_num[0] == 'p':
            security_account = AccountAdminDao.get_personal(security_num)
            if security_account is None:
                # 没有该证券账户
                raise NoneAccountError()
            else:
                if id_num_legal_register_num != security_account.user_id_number:
                    # 个人证券账户与用户身份证不匹配
                    raise InvalidAccountError()
        elif security_num[0] == 'l':
            security_account = AccountAdminDao.get_legal(security_num)
            if security_account is None:
                # 没有该资金账户
                raise NoneAccountError()
            else:
                if id_num_legal_register_num != security_account.legal_person_id_number:
                    # 法人证券账户与法人注册号不匹配
                    raise InvalidAccountError()
        else:
            # account命名问题
            raise InvalidAccountError()
        fund_account = AccountAdminDao.get_fund_by_security(security_num)
        if fund_account is None:
            # 该证券账户没有绑定资金账户
            raise NoneAccountError()
        AccountAdminDao.fund_froze(fund_account)

    # 资金账户解冻
    @staticmethod
    def fund_thaw(data):
        id_num_legal_register_num = data["id_num/legal_register_num"]
        security_num = data["security_num"]

        label = data["label"]
        if label == 0:
            security_num = "l_" + security_num
        else:
            security_num = "p_" + security_num

        if security_num[0] == 'p':
            security_account = AccountAdminDao.get_personal(security_num)
            if security_account is None:
                # 没有该证券账户
                raise NoneAccountError()
            else:
                if id_num_legal_register_num != security_account.user_id_number:
                    # 个人证券账户与用户身份证不匹配
                    raise InvalidAccountError()
        elif security_num[0] == 'l':
            security_account = AccountAdminDao.get_legal(security_num)
            if security_account is None:
                # 没有该资金账户
                raise NoneAccountError()
            else:
                if id_num_legal_register_num != security_account.legal_person_id_number:
                    # 法人证券账户与用户身份证不匹配
                    raise InvalidAccountError()
        else:
            # account命名问题
            raise InvalidAccountError()
        fund_account = AccountAdminDao.get_fund_by_security(security_num)
        if fund_account is None:
            # 该证券账户没有绑定资金账户
            raise NoneAccountError()
        AccountAdminDao.fund_thaw(fund_account)

    # 重新开户（个人证券账户）
    @staticmethod
    def re_add_personal_securities_account(data):
        id_num = data["user_id_number"]
        result = AccountAdminDao.get_personal_by_id(id_num)
        # 没有对应的账号
        if result is None:
            raise NoneAccountError()
        if result.status == "ok":
            raise ConditionNotMeetError()
        temp_new_number = "p_" + data["p_account_number"]
        password = data["password"].encode('utf-8')
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        AccountAdminDao.re_add_personal_securities_account(result, encrypted_password, temp_new_number)

    # 重新开户（法人证券账户）
    @staticmethod
    def re_add_legal_person_securities_account(data):
        id_num = data["legal_person_registration_number"]
        result = AccountAdminDao.get_legal_person_by_id(id_num)
        # 没有对应的账号
        if result is None:
            raise NoneAccountError()
        if result.status == "ok":
            raise ConditionNotMeetError()
        temp_new_number = "l_" + data["l_account_number"]
        password = data["password"].encode('utf-8')
        encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
        AccountAdminDao.re_add_legal_person_securities_account(result, encrypted_password, temp_new_number)

    # 重新开户（资金账户）
    @staticmethod
    def re_add_fund_account(data):
        id_num = data["id_num/legal_register_num"]
        label = data["label"]
        if label == 0:
            result = AccountAdminDao.get_legal_person_by_id(id_num)
        else:
            result = AccountAdminDao.get_personal_by_id(id_num)
        # 没有对应的账号
        if result is None:
            raise NoneAccountError()
        if label == 0:
            temp_new_number = "l_" + data["account_number"]
            security_num = result.l_account_number
        else:
            temp_new_number = "p_" + data["account_number"]
            security_num = result.p_account_number
        login_password = data["login_password"].encode('utf-8')
        encrypted_login_password = bcrypt.hashpw(login_password, bcrypt.gensalt())
        trade_password = data["trade_password"].encode('utf-8')
        encrypted_trade_password = bcrypt.hashpw(trade_password, bcrypt.gensalt())
        fund_account = AccountAdminDao.get_fund_by_security(security_num)
        if fund_account is None:
            # 该证券账户没有绑定资金账户
            raise NoneAccountError()
        if fund_account.account_status == "ok":
            raise ConditionNotMeetError()
        AccountAdminDao.re_add_fund_account(fund_account, encrypted_login_password, encrypted_trade_password, temp_new_number)

    # 证券账户销户
    @staticmethod
    def securities_account_delete(data):
        id_num = data["id_num/legal_register_num"]
        security_num = data["security_num"]
        label = data["label"]
        if label == "0":    # 法人
            security_num = "l_" + security_num
            temp_fund_account = AccountAdminDao.get_fund_by_securities_account(security_num)
            # 还有在资金账户与之绑定
            if temp_fund_account is not None:
                raise WithFundAccountError()
            temp_securities_account = AccountAdminDao.get_legal_person_by_id(id_num)
            AccountAdminDao.legal_personal_delete_one(temp_securities_account)
        else:   # 个人
            security_num = "p_" + security_num
            temp_fund_account = AccountAdminDao.get_fund_by_securities_account(security_num)
            # 还有在资金账户与之绑定
            if temp_fund_account is not None:
                raise WithFundAccountError()
            temp_securities_account = AccountAdminDao.get_personal_by_id(id_num)
            AccountAdminDao.personal_delete_one(temp_securities_account)








