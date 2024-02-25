from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine
from flask_socketio import SocketIO

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy() # create a new SQLAlchemy object
socketio = SocketIO() # create a new SocketIO object
def create_app(*args, **kwargs):
    print(args)
    print(kwargs) # takes arguments and keyword arguments provided by production server
    app = Flask(__name__)
    
    print("socketio init")
    # this is the external connection url, not the internal one
    engine = create_engine('postgresql://toby:GpYiCx5LQPoClKZI5TmIAXGIwIMyKDku@dpg-cl7mp02vokcc73anqkf0-a.frankfurt-postgres.render.com/codingduelsdb')

    app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://toby:GpYiCx5LQPoClKZI5TmIAXGIwIMyKDku@dpg-cl7mp02vokcc73anqkf0-a.frankfurt-postgres.render.com/codingduelsdb'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Users

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of  user table, use it in the query for the user
        return Users.query.get(int(user_id))

    # blueprint for auth routes in  app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    socketio.init_app(app, cors_allowed_origins="*") # allow all origins to connect to the socket, necessary for production
    return app
