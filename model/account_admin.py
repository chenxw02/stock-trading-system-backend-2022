from exts import db


class AccountAdmin(db.Model):
    __tablename__ = "administrator_account"
    administrator_id = db.Column(db.String(20), nullable=False, primary_key=True)
    administrator_password = db.Column(db.String(200), nullable=False)

#
# class Deal(db.Model):
#     __tablename__ = "deal"
#     deal_id = db.Column(int, nullable=False, primary_key=True)
#     securities_account_number = db.Column(db.String(20), nullable=False)
#     person_id = db.Column(db.String(18), nullable=False)
#     status = db.Column(db.String(10), nullable=False)
#     event = db.Column(db.String(10), nullable=False)
#
#
# class LegalPersonSecuritiesAccount(db.Model):
#     __tablename__ = "legal_person_securities_account"
#     l_account_number = db.Column(db.String(20), nullable=False, primary_key=True)
#     password = db.Column(db.String(200), nullable=False)
#     legal_person_registration_number = db.Column(db.String(18), nullable=False)
#     business_license_number = db.Column(db.String(15), nullable=False)
#     legal_person_id_number = db.Column(db.String(18), nullable=False)
#     legal_person_name = db.Column(db.String(50), nullable=False)
#     legal_person_telephone = db.Column(db.String(11), nullable=False)
#     legal_person_address = db.Column(db.String(100), nullable=False)
#     excutor = db.Column(db.String(50), nullable=False)
#     authorized_person_id_number = db.Column(db.String(18), nullable=False)
#     authorized_person_telephone = db.Column(db.String(11), nullable=False)
#     authorized_person_address = db.Column(db.String(100), nullable=False)
#     authority = db.Column(db.String(3), nullable=False)
#
#
# class PersonalSecuritiesAccount(db.Model):
#     __tablename__ = "personal_securities_account"
#     p_account_number = db.Column(db.String(20), nullable=False, primary_key=True)

