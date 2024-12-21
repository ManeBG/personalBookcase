# models.py
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
