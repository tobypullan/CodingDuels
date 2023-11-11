from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # this is the external connection url, not the internal one
    #engine = create_engine('postgresql://toby:GpYiCx5LQPoClKZI5TmIAXGIwIMyKDku@dpg-cl7mp02vokcc73anqkf0-a.frankfurt-postgres.render.com/codingduelsdb')
    
    app.config['SECRET_KEY'] = 'toby1234'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://toby:GpYiCx5LQPoClKZI5TmIAXGIwIMyKDku@dpg-cl7mp02vokcc73anqkf0-a.frankfurt-postgres.render.com/codingduelsdb'

    db.init_app(app)



    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from . import models
    with app.app_context():
        db.create_all()

    return app