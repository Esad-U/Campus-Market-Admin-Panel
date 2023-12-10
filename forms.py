import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class AddUserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    role = SelectField("Role", validators=[DataRequired()], choices=["Admin", "User"])
    address = StringField("Address", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
