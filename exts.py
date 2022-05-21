# 独立db的建立，避免出现循环import依赖

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()