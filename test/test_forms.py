import unittest
from market import app, db
from market.models import User
from market.forms import RegisterForm, LoginForm
from flask import request
from email_validator import EmailNotValidError


class TestForms(unittest.TestCase):
    """
    This class contains unit tests for the RegisterForm and LoginForm used in the Market application.
    """
    def setUp(self):
        """
        Sets up the testing environment by creating a new application instance, disabling CSRF protection,
        configuring a temporary SQLite database, and pushing the application context.
        """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Tears down the testing environment by removing the session, dropping all database tables,
        and popping the application context.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_form_valid_data(self):
        """
        Tests if the RegisterForm validates successfully with valid data.
        """
        form = RegisterForm(username='JohnDoe', email_address='johndoe@example.com', password1='password123', password2='password123')
        self.assertTrue(form.validate())

    def test_register_form_invalid_username_non_alpha(self):
        """
        Tests if the RegisterForm fails to validate when the username contains non-alphanumeric characters.
        """
        form = RegisterForm(username='JohnDoe123', email_address='johndoe@example.com', password1='password123', password2='password123')
        self.assertFalse(form.validate())
        self.assertIn('Username must contain only alphabets.', form.username.errors)

    def test_register_form_invalid_username_existing(self):
        """
        Tests if the RegisterForm fails to validate when the username already exists in the database.
        """
        db.session.add(user)
        db.session.commit()
                        
        form = RegisterForm(username='JohnDoe', email_address='newemail@example.com', password1='password123', password2='password123')
        self.assertFalse(form.validate())
        self.assertIn('Username already exists! Please try a different username.', form.username.errors)

    def test_register_form_invalid_email_existing(self):
        """
        Tests if the RegisterForm fails to validate when the email address already exists in the database.
        """
        user = User(username='JohnDoe', email_address='johndoe@example.com', password_hash='hashedpassword')
        db.session.add(user)
        db.session.commit()
                                
        form = RegisterForm(username='NewUser', email_address='johndoe@example.com', password1='password123', password2='password123')
        self.assertFalse(form.validate())
        self.assertIn('Email Address already exists! Please try a different email address.', form.email_address.errors)

    def test_register_form_invalid_email_format(self):
        """
        Tests if the RegisterForm fails to validate when the email address has an invalid format.
        """
        form = RegisterForm(username='JohnDoe', email_address='invalid-email', password1='password123', password2='password123')
        self.assertFalse(form.validate())
        self.assertIn('Invalid email address:', form.email_address.errors[0])

    def test_login_form_valid_data(self):
        """
        Tests if the LoginForm validates successfully with valid data.
        """
        form = LoginForm(username='JohnDoe', password='password123')
        self.assertTrue(form.validate())

    def test_login_form_missing_username(self):
        """
        Test that the form fails validation when the username is missing.
        This ensures that the username field is required and returns the correct error message
        """
        form = LoginForm(username='', password='password123')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.username.errors)

    def test_login_form_missing_password(self):
        """
        Test that the form fails validation when the password is missing.
        This ensures that the password field is required and returns the correct error message.
        """
        form = LoginForm(username='JohnDoe', password='')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.password.errors)


if __name__ == '__main__':
    unittest.main()


