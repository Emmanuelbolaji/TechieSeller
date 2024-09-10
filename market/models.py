from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import check_password_hash

@login_manager.user_loader
def load_user(user_id):
