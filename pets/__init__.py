import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from pets.utils.consts import Consts

# init the app
app = Flask(__name__)
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.dirname(__file__)
    app.url_map.strict_slashes = False

    db.init_app(app)
    db.create_all(app=app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from pets.models.manager import Manager

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Manager.query.get(user_id)

    # Don't Save Cache - for developer mode / debuging
    # @app.after_request
    # def set_response_headers(response):
    #     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    #     response.headers['Pragma'] = 'no-cache'
    #     response.headers['Expires'] = '0'
    #     return response

    # blueprint for auth routes in our app
    from pets.controllers.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from pets.controllers.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from pets.controllers.animals import animals as animal_blueprint
    app.register_blueprint(animal_blueprint)

    from pets.controllers.employees import employees as employees_blueprint
    app.register_blueprint(employees_blueprint)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html', title='404'), 404

    return app
