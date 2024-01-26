"""Forms for our demo Flask app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length


class RegisterUserForm(FlaskForm):
    """Form for registering a user."""

    first_name = StringField("First Name",
                       validators=[InputRequired(message="Please provide a first name."),
                                   Length(max=30, message="First name can't be longer than 30 characters.")])
    
    last_name = StringField("Last Name",
                       validators=[InputRequired(message="Please provide a last name."),
                                   Length(max=30, message="Last name can't be longer than 30 characters.")])
    
    email = EmailField("Email",
                       validators=[InputRequired(message="Please provide a valid email address."),
                                   Length(max=50, message="Emails can't be longer than 50 characters.")])
    
    username = StringField("Username",
                       validators=[InputRequired(message="Please provide a username."),
                                   Length(max=20, message="Username can't be longer than 20 characters.")])
    
    password = PasswordField("Password",
                        validators=[InputRequired(message="Please provide a password."),
                                    Length(min=8, message="Password needs to be at least 8 characters long.")])
    

class LoginUserForm(FlaskForm):
    """Form for logging in a user."""
    
    username = StringField("Username",
                       validators=[InputRequired(message="Please provide a username."),
                                   Length(max=20, message="Username can't be longer than 20 characters.")])
    
    password = PasswordField("Password",
                        validators=[InputRequired(message="Please provide a password."),
                                    Length(min=8, message="Password needs to be at least 8 characters long.")])
    
