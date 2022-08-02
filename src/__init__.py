from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load environmet variables
load_dotenv('./env')

# Create app
# Load environmet variables
app = Flask(__name__)
app.config['SECRET_KEY'] = "a12b9af2eb5a26ch8rl1e1c6771e52bmnfsfa2z6"
app.jinja_env.add_extension('jinja2.ext.do')


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://gestion8_cjjouanne:inverges1205@localhost:5432/gestion8_siiapi"
db = SQLAlchemy(app)

if db:
    print('Conection to database established successfully...')

# ______________________________________________________________________________

# _______________________________________________________________________________
# Others
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from .routes import *  # nopep8