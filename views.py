from flask import render_template, current_app, flash, request, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import pbkdf2_sha256 as hasher
from forms import *
from login_functions import get_user


def index():
    form = LoginForm()
    if form.validate_on_submit():
        # print("entered validation")
        email = form.data["email"]
        user = get_user(email)
        if user is not None and user.role == 'admin':
            # print("found customer")
            password = form.data["password"]
            if hasher.verify(password, user.password):
                # print("verified customer")
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
                db.delete_user(key)
        return redirect(url_for("users_page"))
