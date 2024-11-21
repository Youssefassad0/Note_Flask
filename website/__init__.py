from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os



db=SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']=os.urandom(24)  
    app.config['SQLALCHEMY_DATABASE_URI']='mssql+pyodbc://ECM:.\Ec@Extr@net@192.168.2.230/NOTEBOOK?driver=SQL Server Native Client 10.0'
    db.init_app(app) 
    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    

    return app
