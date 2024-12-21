# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base.db'

db = SQLAlchemy(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
