from flask import redirect
from flask import Blueprint
from mib import app

users = Blueprint('users', __name__)

LOTTERY_ENDPOINT = app.config['LOTTERY_MS_URL']
REQUESTS_TIMEOUT_SECONDS = 60
USERS_ENDPOINT = app.config['USERS_MS_URL']
MESSAGE_ENDPOINT = ""


home = Blueprint('home', __name__)


@home.route('/', methods=['GET'])
def index():
    return redirect("/mailbox")
