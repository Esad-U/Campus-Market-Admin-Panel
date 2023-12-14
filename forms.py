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
    role = SelectField("Role", validators=[DataRequired()], choices=["admin", "user"])
    address = StringField("Address", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    validation = PasswordField("Password Again", validators=[DataRequired()])


class AddCategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
