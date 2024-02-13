from flask import Blueprint, session, redirect, url_for, request
from flask_oauthlib.client import OAuth

views = Blueprint('views', __name__)

oauth = OAuth()

google = oauth.remote_app('google',
                        consumer_key='466995828317-j1ij0nr84nabl0hkdauum7q4or2k410h.apps.googleusercontent.com',
                        consumer_secret='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',
                        request_token_params={'scope': 'email'},
                        base_url='https://www.googleapis.com/oauth2/v1/',
                        authorize_url='https://accounts.google.com/o/oauth2/auth',
                        request_token_url=None,
                        access_token_method='POST',
                        access_token_url='https://accounts.google.com/o/oauth2/token')

@views.route('/')
def home():
    return "<a href='/login'><button>Login</button></a>"

@views.route('/login')
def login():
    return google.authorize(callback=url_for('views.authorized', _external=True))

@views.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('views.home'))

@views.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    return 'Logged in as: ' + user_info.data['email']

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
