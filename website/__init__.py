from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
# from users import users

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Set the app's secret key and database URI
    app.config['SECRET_KEY'] = os.urandom(24)  # You can also use a fixed key, but urandom is fine for development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:ecmaroc@192.168.2.210/RENTWAY?driver=SQL Server Native Client 10.0'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

    # Initialize the app with SQLAlchemy
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Import Blueprints
    from .views import views
    from .auth import auth
    from .users import users

    # Register Blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(users, url_prefix='/users')

    # Import models for user management
    from .models import User, Note

    # Set up user_loader function for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) 

    return app
