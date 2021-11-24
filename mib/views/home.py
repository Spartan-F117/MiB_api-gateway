
from flask import Blueprint, render_template, redirect, url_for

from flask import Blueprint, render_template, flash
import requests
from flask_login import LoginManager, current_user
from mib import app

users = Blueprint('users', __name__)

LOTTERY_ENDPOINT = app.config['LOTTERY_MS_URL']
REQUESTS_TIMEOUT_SECONDS = 60
USERS_ENDPOINT = app.config['USERS_MS_URL']
MESSAGE_ENDPOINT = ""




home = Blueprint('home', __name__)



@home.route('/', methods=['GET', 'POST'])
def index():
    return redirect("/mailbox")
