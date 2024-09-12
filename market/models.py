from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import check_password_hash

@login_manager.user_loader
def load_user(user_id):
    """
    Loads the user by user_id for session management.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User object if found, otherwise None.
    """
    try:
        return User.query.get(int(user_id))
    except (ValueError, TypeError) as e:
        return None

class User(db.Model, UserMixin):
    """
     Represents a user in the database. Inherits from SQLAlchemy's db.Model and Flask-Login's UserMixin.

     Attributes:
         id (int): The primary key for the user.
         username (str): The username of the user (unique).
         email_address (str): The email address of the user (unique).
         password_hash (str): The hashed password of the user.
         items (relationship): One-to-many relationship with the Item model (items owned by the user).
    """
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        """
        Prevents direct access to the user's password.

        Raises:
            AttributeError: If an attempt is made to read the password directly.
        """
        raise AttributeError("Password is not a readable attribute.")  # Prevent direct access to password

    @password.setter
    def password(self, plain_text_password):
        """
        Hashes and sets the user's password.

        Args:
            plain_text_password (str): The plain text password to hash.

        Raises:
            ValueError: If the password is empty or less than 6 characters long.
        """
        if not plain_text_password or len(plain_text_password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        """
        Checks if the provided password matches the stored password hash.

        Args:
            attempted_password (str): The password to check.

        Returns:
            bool: True if the password matches, False otherwise.

        Raises:
            ValueError: If the attempted password is empty.
        """
        if not attempted_password:
            raise ValueError("Attempted password cannot be empty.")
         return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def save(self):
        """
        Saves the user to the database.

        Raises:
            ValueError: If the username or email address is already taken.
            RuntimeError: If any other SQLAlchemy error occurs.
        """
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
    """
    Represents an item in the database.

    Attributes:
        id (int): The primary key for the item.
        name (str): The name of the item (unique).
        price (int): The price of the item.
        barcode (str): The barcode of the item (unique).
        description (str): The description of the item.
        owner (int): The ID of the user who owns the item (foreign key)
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        """
        Represents the item as a string.

        Returns:
            str: The string representation of the item.
        """
        return f'Item {self.name}'

    def save(self):
        """
        Saves the item to the database.

        Raises:
            ValueError: If the item name or barcode is already taken.
            RuntimeError: If any other SQLAlchemy error occur.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Item with this name or barcode already exists.")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"An error occurred while saving the item: {str(e)}")


