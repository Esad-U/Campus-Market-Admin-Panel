from flask import render_template, current_app, flash, request, url_for, redirect, abort, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_paginate import Pagination, get_page_parameter
from forms import *
from models.user import User


def index():
    """ Linked to API """
    session['token'] = ""
    if current_user.is_authenticated:
        # Redirect them away from the intended URL (e.g., a form submission URL)
        return redirect(url_for('home'))

    form = LoginForm()
    db = current_app.config["dbconfig"]
    if form.validate_on_submit():
        email = form.data["email"]
        password = form.data["password"]

        status_code, body = db.admin_login(email, password)

        if status_code == 200:
            session['token'] = body['token']
            user = User(body['token'], email)
            login_user(user)
            flash("You have logged in")
            next_page = request.args.get("next", url_for("home"))
            return redirect(next_page)
        flash(body)
    return render_template("index.html", form=form)


@login_required
def home():
    return render_template("home.html")


@login_required
def logout():
    logout_user()
    session['token'] = ""
    session['data'] = []
    session['comments_list'] = []
    flash("You have logged out")

    return redirect(url_for("index"))


@login_required
def users_page():
    """ Linked To API """
    db = current_app.config["dbconfig"]

    if request.method == 'GET':
        users = db.get_all_data_from_table('User', current_user.token)
        session['data'] = users

        paginated_users, pagination = pagination_function(users, 'users')

        return render_template("users.html", users=paginated_users, pagination=pagination)
    else:
        form_user_keys = request.form.getlist("user_keys")
        if len(form_user_keys) == 0:
            flash("Choose users to delete.")
        else:
            for key in form_user_keys:
                status_code = db.delete_data_from_table(key, 'User', current_user.token)
                if status_code != 200:
                    abort(status_code)
        return redirect(url_for("users_page"))


@login_required
def block_user(user_id):
    """ Linked to API """
    db = current_app.config["dbconfig"]

    status_code = db.block_user_api(user_id, current_user.token)

    if status_code != 200:
        abort(status_code)

    return redirect(url_for("users_page"))


@login_required
def unblock_user(user_id):
    """ Linked to API """
    db = current_app.config["dbconfig"]

    status_code = db.unblock_user_api(user_id, current_user.token)

    if status_code != 200:
        abort(status_code)

    return redirect(url_for("users_page"))


@login_required
def comments_page():
    """ Linked to API """
    db = current_app.config["dbconfig"]

    if request.method == 'GET':
        comments = db.get_all_data_from_table('Comment', current_user.token)
        session['comments_list'] = comments

        paginated_comments, pagination = pagination_function(comments, 'comments')

        return render_template("comments.html", comments=paginated_comments, pagination=pagination)
    else:
        form_comment_keys = request.form.getlist("comment_keys")
        if len(form_comment_keys) == 0:
            flash("Choose comments to delete.")
        else:
            for key in form_comment_keys:
                status_code = db.delete_data_from_table(key, 'Comment', current_user.token)
                if status_code != 200:
                    abort(status_code)
        return redirect(url_for("comments_page"))


@login_required
def comment_page(comment_id):
    """ Linked to API """
    comment = None
    for c in session['comments_list']:
        if str(c['_id'])[10:-2] == comment_id[10:-2]:
            comment = c
            break
    if request.method == "GET":
        return render_template("comment.html", comment=comment)
    else:
        db = current_app.config["dbconfig"]
        status_code = db.delete_data_from_table(comment_id, 'Comment', current_user.token)
        if status_code != 200:
            abort(status_code)
        return redirect(url_for("comments_page"))


@login_required
def accept_comment(comment_id):
    """ Linked to API """
    db = current_app.config["dbconfig"]

    status_code, resp_body = db.verify_comment_api(comment_id, current_user.token)

    if status_code == 200:
        flash("Comment is accepted!")
        return redirect(url_for("comments_page"))
    else:
        flash(resp_body)
        return redirect(url_for("comments_page"))


"""@login_required
def chats_page():
    # ToDO: Waiting for the database
    db = current_app.config["dbconfig"]

    if request.method == "GET":
        chats = db.get_chats()
        return render_template("chats.html", chats=chats)
    else:
        form_chat_keys = request.form.getlist("chat_keys")
        if len(form_chat_keys) == 0:
            flash("Choose chats to delete.")
        else:
            for key in form_chat_keys:
                db.delete_chat(key)
        return redirect(url_for("chats_page"))"""


@login_required
def products_page():
    """ Linked to API """
    db = current_app.config["dbconfig"]

    if request.method == "GET":
        products = db.get_all_data_from_table('Product', current_user.token)
        session['data'] = products

        paginated_products, pagination = pagination_function(products, 'products')

        return render_template("products.html", products=paginated_products, pagination=pagination)
    else:
        form_prod_keys = request.form.getlist("prod_keys")
        if len(form_prod_keys) == 0:
            flash("Choose products to delete.")
        else:
            for key in form_prod_keys:
                status_code = db.delete_data_from_table(key, 'Product', current_user.token)
                if status_code != 200:
                    abort(status_code)
        return redirect(url_for("products_page"))


@login_required
def categories_page():
    """ Linked to API """
    db = current_app.config["dbconfig"]

    if request.method == "GET":
        categories = db.get_all_data_from_table('Category', current_user.token)
        session['data'] = categories

        paginated_categories, pagination = pagination_function(categories, 'categories')

        return render_template("categories.html", categories=paginated_categories, pagination=pagination)
    else:
        form_category_keys = request.form.getlist("category_keys")
        if len(form_category_keys) == 0:
            flash("Choose categories to delete.")
        else:
            for key in form_category_keys:
                status_code = db.delete_data_from_table(key, 'Category', current_user.token)
                if status_code != 200:
                    abort(status_code)
        return redirect(url_for("categories_page"))


@login_required
def add_category_page():
    """ Linked to API """
    form = AddCategoryForm()
    db = current_app.config["dbconfig"]

    if form.validate_on_submit():
        name = form.data['name']

        status_code = db.insert_category_api(name, current_user.token)

        if status_code == 400:
            flash("This category already exists!")
        elif status_code != 200:
            abort(status_code)
        else:
            return redirect(url_for("categories_page"))

    return render_template('add_category.html', form=form)


@login_required
def search_users():
    if request.method == 'GET':
        return redirect(url_for('home'))
    else:
        keyword = request.form.get('keyword')

        users = [item for item in session['data'] if keyword.lower() in str(item['_id']).lower()]

        if not len(users):
            flash("Could not find any data related to given keyword: '" + keyword + "'")
            paginated_users, pagination = pagination_function(session['data'], 'users')
            return render_template("users.html", users=paginated_users, pagination=pagination)

    paginated_users, pagination = pagination_function(users, 'users', len(users))

    return render_template("users.html", users=paginated_users, pagination=pagination)


@login_required
def search_comments():
    if request.method == 'GET':
        return redirect(url_for('home'))
    else:
        keyword = request.form.get('keyword')

        comments = [item for item in session['comments_list'] if keyword.lower() in str(item['author']).lower()]

        if not len(comments):
            flash("Could not find any data related to given keyword: '" + keyword + "'")
            paginated_comments, pagination = pagination_function(session['comments_list'], 'comments')
            return render_template("comments.html", comments=paginated_comments, pagination=pagination)

    paginated_comments, pagination = pagination_function(comments, 'comments', len(comments))

    return render_template("comments.html", comments=paginated_comments, pagination=pagination)


@login_required
def search_products():
    if request.method == 'GET':
        return redirect(url_for('home'))
    else:
        keyword = request.form.get('keyword')

        products = [item for item in session['data'] if keyword.lower() in str(item['categoryId']).lower()]

        if not len(products):
            flash("Could not find any data related to given keyword: '" + keyword + "'")
            paginated_products, pagination = pagination_function(session['data'], 'products')
            return render_template("products.html", products=paginated_products, pagination=pagination)

    paginated_products, pagination = pagination_function(products, 'products', len(products))

    return render_template("products.html", products=paginated_products, pagination=pagination)


@login_required
def search_categories():
    if request.method == 'GET':
        return redirect(url_for('home'))
    else:
        keyword = request.form.get('keyword')

        categories = [item for item in session['data'] if keyword.lower() in str(item['categoryName']).lower()]

        if not len(categories):
            flash("Could not find any data related to given keyword: '" + keyword + "'")
            paginated_categories, pagination = pagination_function(session['data'], 'categories')
            return render_template("categories.html", categories=paginated_categories, pagination=pagination)

    paginated_categories, pagination = pagination_function(categories, 'products', len(categories))

    return render_template("categories.html", categories=paginated_categories, pagination=pagination)


def pagination_function(data, name, per_page=10):
    # Pagination parameters
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = per_page  # Number of items per page
    offset = (page - 1) * per_page
    total = len(data)

    # Paginate the data
    paginated_data = data[offset: offset + per_page]

    pagination = Pagination(page=page, per_page=per_page, total=total, record_name=name,
                            css_framework='bootstrap4')

    return paginated_data, pagination
