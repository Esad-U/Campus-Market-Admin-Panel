from flask import Flask
import views
from pymongo import MongoClient
from flask_login import LoginManager
from login_functions import get_user

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


client = MongoClient('localhost', 27017)

db = client.CampusMarket


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.index, methods=["GET", "POST"])
    app.add_url_rule("/home", view_func=views.home)

    app.config["dbconfig"] = db

    lm.init_app(app)
    lm.login_view = "index"

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5050)
    app.run(host="0.0.0.0", port=port)
