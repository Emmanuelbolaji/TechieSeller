from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import check_password_hash

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except (ValueError, TypeError) as e:
        return None

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")  # Prevent direct access to password

    @password.setter
    def password(self, plain_text_password):
        if not plain_text_password or len(plain_text_password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        if not attempted_password:
            raise ValueError("Attempted password cannot be empty.")
         return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("User with this username or email already exists.")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"An error occurred while saving the user: {str(e)}")

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Item with this name or barcode already exists.")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"An error occurred while saving the item: {str(e)}")


