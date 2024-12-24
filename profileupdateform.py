from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError
from models import User 

class ProfileUpdateForm(FlaskForm):
    email = StringField(
        'New Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            Length(min=8),
            Regexp(
                r'^(?=.*[A-Za-z])(?=.*\d).+$',
                message="Password must contain at least one letter and one number."
            )
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        # Ensure the email is unique
        existing_user = User.query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError('This email is already in use. Please choose a different one.')
