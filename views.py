from flask import render_template, current_app, flash, request, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import pbkdf2_sha256 as hasher
from forms import *
from login_functions import get_user
from models.user import User


def index():
    if current_user.is_authenticated:
        # Redirect them away from the intended URL (e.g., a form submission URL)
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.data["email"]
        user = get_user(email)
        if user is not None and user.role == 'admin':
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in")
                next_page = request.args.get("next", url_for("home"))
                return redirect(next_page)
        flash("Invalid credentials")
    return render_template("index.html", form=form)


@login_required
def home():
    return render_template("home.html")


@login_required
def logout():
    logout_user()
    flash("You have logged out")

    return redirect(url_for("index"))


@login_required
def users_page():
    db = current_app.config["dbconfig"]

    if request.method == 'GET':
        users = db.get_users()
        return render_template("users.html", users=users)
    else:
        form_user_keys = request.form.getlist("user_keys")
        if len(form_user_keys) == 0:
            flash("Choose users to delete.")
        else:
            for key in form_user_keys:
                if key != str(current_user.id):
                    db.delete_user(key)
                else:
                    flash("You cannot delete your own user.")
        return redirect(url_for("users_page"))


@login_required
def add_user_page():
    form = AddUserForm()
    db = current_app.config["dbconfig"]

    if form.validate_on_submit():
        name = form.data['name']
        surname = form.data['surname']
        role = form.data['role']
        address = form.data['address']
        email = form.data['email']
        password = hasher.hash(form.data['password'])

        if db.get_user_by_email(email) is None:
            new_user = User(id="", name=name, surname=surname, role=role, address=address, email=email,
                            password=password)
            db.insert_user(new_user)

            return redirect(url_for('users_page'))
        else:
            flash('A user with this email already exists')

    return render_template('add_user_page.html', form=form)


@login_required
def profile_page():
    return render_template('user_profile.html', user=current_user)


@login_required
def change_password_page():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if form.data['password'] != form.data['validation']:
            flash('Two passwords do not match. Enter again!')
        else:
            new_pw = hasher.hash(form.data['password'])
            current_app.config['dbconfig'].update_password(current_user, new_pw)

            return redirect(url_for('profile_page'))

    return render_template('change_password.html', form=form)


@login_required
def comments_page():
    db = current_app.config["dbconfig"]

    if request.method == 'GET':
        comments = db.get_comments()
        return render_template("comments.html", comments=comments)
    else:
        form_comment_keys = request.form.getlist("comment_keys")
        if len(form_comment_keys) == 0:
            flash("Choose comments to delete.")
        else:
            for key in form_comment_keys:
                db.delete_comment(key)
        return redirect(url_for("comments_page"))
