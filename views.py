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
        if user is not None:
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
