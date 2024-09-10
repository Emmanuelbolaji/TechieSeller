from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User
from email_validator import validate_email, EmailNotValidError

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        try:
            user = User.query.filter_by(username=username_to_check.data).first()
            if user:
                if not username_to_check.data.isalpha():
                    raise ValidationError('Username must contain only alphabets.')
                except Exception as e:
                    raise ValidationError(f"An error occurred during username validation: {str(e)}")
    def validate_email_address(self, email_address_to_check):
        try:
            valid = validate_email(email_address_to_check.data)
            email_address_to_check.data = valid.email
            
            email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
            if email_address:
                raise ValidationError('Email Address already exists! Please try a different email address.')
        except EmailNotValidError as e:
            raise ValidationError(f'Invalid email address: {str(e)}')
        except Exception as e:
            raise ValidationError(f"An error occurred during email validation: {str(e)}")

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

