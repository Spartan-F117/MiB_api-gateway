from flask import Blueprint, redirect, render_template,flash
from flask_login import login_user, logout_user, current_user, login_required
from mib.forms import LoginForm
import requests
from mib import app
from mib.auth.user import User

auth = Blueprint('auth', __name__)

LOGIN_OK = 200
LOGIN_FAIL = 201
DOUBLE_LOGIN = 202

LOTTERY_ENDPOINT = app.config['LOTTERY_MS_URL']
REQUESTS_TIMEOUT_SECONDS = 60
USERS_ENDPOINT = app.config['USERS_MS_URL']


def send_logout_request():
    pass


# This is the route to do the login, in the login.html page there is a form and the information
# that are put in the form are cheked in the db and the is_active flag in the db is put equal to True
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        email, password = form.data['email'], form.data['password']
        payload = dict(email=email, password=password)
        try:
            print('trying response....')
            response = requests.post(USERS_ENDPOINT+'/authenticate',
                                     json=payload,
                                     timeout=REQUESTS_TIMEOUT_SECONDS
                                     )
            print('received response....')
            json_response = response.json()
            status = response.status_code

            if status == 200:
                user = User.build_from_json(json_response['user'])
                print("user logged")
                print(user)
                login_user(user)
                return render_template("mailbox.html")
            elif status == 201 or "not a 'email'" in json_response["detail"]:
                print("Invalid credential")
                flash("Invalid credential")
                return render_template('login.html', form=form)
            else:
                return "You are already logged"
        except Exception as e:
            print(e)
            return "HTTP timeout"
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    send_logout_request()
    logout_user()
    return redirect('/')
