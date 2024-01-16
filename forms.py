from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, validators
from wtforms.validators import DataRequired, Email


class SignupForm(FlaskForm):  # this is WT Form Class for sign-up
    user_name = StringField("Name", validators=[DataRequired()])
    user_email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        validators.InputRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField("Signup")


class SigninForm(FlaskForm):  # this is WT Form class for sign-in
    user_email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Signup")
