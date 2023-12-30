from flask import Flask
import views
from pymongo import MongoClient
from flask_login import LoginManager
from login_functions import get_user
from database import Database

lm = LoginManager()

uri = "mongodb+srv://admin:admin12345@campusmarket.dedlc0d.mongodb.net/?retryWrites=true&w=majority"
url = "https://tnglgfyhba.execute-api.eu-central-1.amazonaws.com"


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.index, methods=["GET", "POST"])
    app.add_url_rule("/home", view_func=views.home)
    app.add_url_rule("/logout", view_func=views.logout)
    app.add_url_rule("/profile", view_func=views.profile_page)
    app.add_url_rule("/change-password", view_func=views.change_password_page, methods=["GET", "POST"])

    app.add_url_rule("/users", view_func=views.users_page, methods=["GET", "POST"])
    app.add_url_rule("/add-user", view_func=views.add_user_page, methods=["GET", "POST"])
    app.add_url_rule("/search_users", view_func=views.search_users, methods=["GET", "POST"])

    app.add_url_rule("/comments", view_func=views.comments_page, methods=["GET", "POST"])
    app.add_url_rule("/comment/<comment_id>", view_func=views.comment_page, methods=["GET", "POST"])
    app.add_url_rule("/search_comments", view_func=views.search_comments, methods=["GET", "POST"])
    app.add_url_rule("/accept-comment/<comment_id>", view_func=views.accept_comment, methods=["GET"])

    app.add_url_rule("/chats", view_func=views.chats_page, methods=["GET", "POST"])
    app.add_url_rule("/search_chats", view_func=views.search_chats, methods=["GET", "POST"])

    app.add_url_rule("/products", view_func=views.products_page, methods=["GET", "POST"])
    app.add_url_rule("/search_products", view_func=views.search_products, methods=["GET", "POST"])

    app.add_url_rule("/categories", view_func=views.categories_page, methods=["GET", "POST"])
    app.add_url_rule("/add-category", view_func=views.add_category_page, methods=["GET", "POST"])
    app.add_url_rule("/search_categories", view_func=views.search_categories, methods=["GET", "POST"])

    app.config["dbconfig"] = Database(uri=uri, url=url, dbname='CampusMarket')

    lm.init_app(app)
    lm.login_view = "index"

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5050)
    app.run(host="0.0.0.0", port=port)
