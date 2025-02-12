from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError

class LoginForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[
            DataRequired(), 
            Length(min=3, max=30),
            Regexp(r'^[a-zA-Z0-9_]+$', message="Username must contain only letters, numbers, or underscores.")
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[
            DataRequired(),
            Length(min=3, max=30),
            Regexp(r'^[a-zA-Z0-9_]+$', message="Username must contain only letters, numbers, or underscores.")
        ]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8),
            Regexp(r'^(?=.*[A-Za-z])(?=.*\d).+$', message="Password must contain at least one letter and one number.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Register')

class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'New Password', 
        validators=[
            DataRequired(),
            Length(min=8),
            Regexp(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$', 
                   message="Password must contain at least one uppercase letter, one lowercase letter, and one digit.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Reset Password')

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])