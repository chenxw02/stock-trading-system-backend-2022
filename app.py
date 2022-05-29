from flask import Flask
from controller.demo_api import demo_api
from controller.admin_api import admin_api
from controller.account_admin_api import account_admin_api
from controller.admin_errorhandler import admin_error
from controller.account_admin_errorhandler import account_admin_error
from controller.release_search_api import release_search_api
from controller.query_user_api import query_user_api
from controller.query_user_errorhandler import query_user_error
from exts import db
from flask_cors import CORS

import config

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(config)
db.init_app(app)

app.register_blueprint(demo_api)
app.register_blueprint(admin_api)
app.register_blueprint(admin_error)
app.register_blueprint(account_admin_api)
app.register_blueprint(account_admin_error)
app.register_blueprint(release_search_api)
app.register_blueprint(query_user_api)
app.register_blueprint(query_user_error)


@app.route('/', methods=["GET", "POST"])
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
