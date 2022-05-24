jwt_secret_key = "gumi"

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'stock2022'
PASSWORD = 'stock2022aaa'
HOST = '110.42.175.148'
PORT = '3306'
DATABASE = 'stock'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)