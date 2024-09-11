import unittest
from market import app, db
from market.models import User
from market.forms import RegisterForm, LoginForm
from flask import request
from email_validator import EmailNotValidError


class TestForms(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
            db.session.remove()
            db.drop_all()
            self.app_context.pop()

    def test_register_form_valid_data(self):
        form = RegisterForm(username='JohnDoe', email_address='johndoe@example.com', password1='password123', password2='password123')
        self.assertTrue(form.validate())

    def test_register_form_invalid_username_non_alpha(self):
        form = RegisterForm(username='JohnDoe123', email_address='johndoe@example.com', password1='password123', password2='password123')
        self.assertFalse(form.validate())
        self.assertIn('Username must contain only alphabets.', form.username.errors)

    def test_register_form_invalid_username_existing(self):
        db.session.add(user)
        db.session.commit()
                        
        form = RegisterForm(username='JohnDoe', email_address='newemail@example.com', password1='password123', password2='password123')
        self.assertFalse(form.validate())
        self.assertIn('Username already exists! Please try a different username.', form.username.errors)

    def test_register_form_invalid_email_existing(self):
        user = User(username='JohnDoe', email_address='johndoe@example.com', password_hash='hashedpassword')
        db.session.add(user)
        db.session.commit()
                                
        form = RegisterForm(username='NewUser', email_address='johndoe@example.com', password1='password123', password2='password123')
        self.assertFalse(form.validate())
        self.assertIn('Email Address already exists! Please try a different email address.', form.email_address.errors)

    def test_register_form_invalid_email_format(self):
        form = RegisterForm(username='JohnDoe', email_address='invalid-email', password1='password123', password2='password123')
        self.assertFalse(form.validate())
        self.assertIn('Invalid email address:', form.email_address.errors[0])

    def test_login_form_valid_data(self):
        form = LoginForm(username='JohnDoe', password='password123')
        self.assertTrue(form.validate())

    def test_login_form_missing_username(self):
        form = LoginForm(username='', password='password123')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.username.errors)

    def test_login_form_missing_password(self):
        form = LoginForm(username='JohnDoe', password='')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.password.errors)


if __name__ == '__main__':
    unittest.main()


