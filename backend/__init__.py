from flask import Flask
from flask_oauthlib.client import OAuth
def create_app():

    app=Flask(__name__)
    app.config['SECRET_KEY']="Manoj@1234"
    oauth = OAuth(app)
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    return app
