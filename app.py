from flask import Flask
from demo_api import demo_api
from admin_api import admin_api
from admin_errorhandler import admin_error
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


@app.route('/', methods=["GET", "POST"])
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
