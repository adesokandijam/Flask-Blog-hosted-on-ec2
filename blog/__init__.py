from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

import os

from flask_ckeditor import CKEditor

from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')


app = Flask(__name__, static_folder= join(dirname(realpath(__file__)), 'static/'))
ckeditor = CKEditor(app)




app.secret_key = "secret key"
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/User'
app.config['SECRET_KEY'] = "This should be more secure than this"
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager  = LoginManager(app)




from blog import routes