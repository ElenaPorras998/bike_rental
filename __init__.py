from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import Users
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    # Create Flask app.
    app = Flask(__name__)

    # Database URI values.
    POSTGRES = {
    }
    # set the database URI values using placeholders and the values defined previously.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s/%(db)s' % POSTGRES
    # Secret key is necessary for user authentication.
    app.config['SECRET_KEY'] = ''

    # Initialize the app
    db.init_app(app)
    # Set the login view to the Login Manager and initialize it.
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # function to load the user using it's ID
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # Register the two blueprints used in this project (auth and main)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app