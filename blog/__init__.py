from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '9bd0a97f80d5bcaaa049260d9a218b4b08928a01c0eb9bfb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21110149:Simon01234@csmysql.cs.cf.ac.uk:3306/c21110149_21110149_cmt120_cw2'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from blog import routes