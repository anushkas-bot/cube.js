from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

app = Flask(__name__)
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id='zmgaX4X9wf5KXK9UTpSjFa63lJkitruJ',
    client_secret='525-BM6bBkNu2-YyIHayQGu2_3bN_JlHSfrkUQScZEhyyFgcShSzkBaOMn6QKOgU',
    api_base_url='dev-zz43b2ca.us.auth0.com',
    access_token_url='https://dev-zz43b2ca.us.auth0.com/oauth/token',
    authorize_url='https://dev-zz43b2ca.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# Here we're using the /callback route.
@app.route('/callback')
def callback_handler():
# Handles response from auth0
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    user_info = resp.json()
    # Store the user information in the flask session.
    session['jwt_payload'] = user_info
    session['profile'] = {
    'user_id': userinfo['sub'],
    'name': userinfo['name'],
    }
    return redirect('/profile')

@app.route('/loginuser')
def user_login():
    return auth0.authorize_redirect(redirect_uri='CALLBACK_URL')

@app.route('/profile')
#@requires_auth
def profile():
    return render_template('profile.html',
    userinfo=session['profile'],
    userinfo_pretty=json.dumps(session['jwt_payload'], indent=3))

@app.route('/logout')
def user_logout():
    session.clear()
    #Redirecting user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'CLIENT_ID'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

if __name__ == "__main__":
    app.run()
