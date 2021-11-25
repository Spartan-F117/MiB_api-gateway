from flask import Blueprint, render_template, flash, redirect, request
import requests
from flask_login import login_required, current_user
from mib import app
from mib.forms import UserForm

users = Blueprint('users', __name__)

LOTTERY_ENDPOINT = app.config['LOTTERY_MS_URL']
USERS_ENDPOINT = app.config['USERS_MS_URL']
REQUESTS_TIMEOUT_SECONDS = 60
MESSAGE_ENDPOINT = ""

def add_to_blacklist(owner_blocklist, user_in_blacklist):
    payload = dict(id_owner=owner_blocklist,id_to_insert=user_in_blacklist)
    try:
        response = requests.post(USERS_ENDPOINT + "/blacklist",
                                 json=payload,
                                 timeout=REQUESTS_TIMEOUT_SECONDS
                                 )
        if response.status_code == 202:
            print("user added to blacklist")
            flash("user added to blacklist")
        elif response.status_code == 303:
            print("Generic error")
            flash("Generic error")
    except Exception as e:
        print(e)


def remove_to_blacklist(owner_blocklist, user_in_blacklist):
    payload = dict(id_owner=owner_blocklist, id_to_insert=user_in_blacklist)
    try:
        response = requests.delete(USERS_ENDPOINT + "/blacklist", json=payload, timeout=REQUESTS_TIMEOUT_SECONDS)
        if response.status_code == 202:
            print("user removed to blacklist")
            flash("user removed to blacklist")
        elif response.status_code == 303:
            print("Generic error")
            flash("Generic error")
    except Exception as e:
        print(e)


def add_to_reportlist(owner_reportlist, user_in_reportlist):
    payload = dict(id_owner=owner_reportlist, id_to_insert=user_in_reportlist)
    try:
        response = requests.post(USERS_ENDPOINT + "/reportlist", json=payload, timeout=REQUESTS_TIMEOUT_SECONDS)
        if response.status_code == 202:
            print("user added to report list")
            flash("user added to report list")
        elif response.status_code == 303:
            print("Generic error")
            flash("Generic error")
    except Exception as e:
        print(e)


def retrive_users(id):
    payload = dict(id=id)
    try:
        response = requests.post(USERS_ENDPOINT + "/show_users",
                                 json=payload,
                                 timeout=REQUESTS_TIMEOUT_SECONDS
                                 )
        if response.status_code == 201:
            print("list retrived")
            json_response = response.json()
            result = json_response["list_users"]
        elif response.status_code == 303:
            print("Generic error")
            result = "error"
        return result
    except Exception as e:
        print(e)


@users.route('/create_user/', methods=['POST', 'GET'])
def create_user():
    '''
        Create a user
    '''

    form = UserForm()
    if not (current_user is not None and hasattr(current_user, 'id')):  # check if the user is logged
        if form.is_submitted():  # take information from the Form
            email = form.data['email']
            firstname = form.data['firstname']
            lastname = form.data['lastname']
            password = form.data['password']
            date_of_birth = str(form.data['date_of_birth'])
            nickname = form.data['nickname']
            location = form.data['location']

            payload = dict(email=email, password=password, firstname=firstname,
                           lastname=lastname, date_of_birth=date_of_birth,
                           nickname=nickname, location=location)

            try:
                print('trying creating user....')
                response = requests.post(USERS_ENDPOINT + '/create_user',
                                         json=payload,
                                         timeout=REQUESTS_TIMEOUT_SECONDS
                                         )
                print('received response for create user....')
                json_response = response.json()

                status = response.status_code

                # it's ok.. user created
                if status == 201:
                    print("user created")
                    return redirect("/login")
                # invalid creation
                elif status == 203:
                    print("Invalid credential")
                    flash("invalid credential")
                    return render_template('create_user.html', form=form)
            except Exception as e:
                print(e)
                return "HTTP timeout"
        return render_template('create_user.html', form=form)
    else:
        return "You are currently logged in, you have to <a href=/logout>logout</a> first"


# #This route is to see the mailbox
@users.route('/mailbox/', methods=['GET'])
def inbox():
    # '''
    #  Shows the mailbox of the user divded into three parts
    #  1) The Inbox part shows the received messages
    #  2) The Sent part shows the messages that user sent
    #  3) The Draft part shows the messages in the draft
    #
    #  It also provides the functionality for the user to delete future
    #  messages if the user is lottery winner
    # '''
    if current_user is not None and hasattr(current_user, 'id'): #check if the user is logged:

        # look for filter
        payload_filter = dict(id=current_user)
        try:
            response = requests.post(USERS_ENDPOINT + "/filter_list",
                                     json=payload_filter,
                                     timeout=REQUESTS_TIMEOUT_SECONDS
                                     )
            if response.status_code == 201:
                #filter recived
                filter = response.json()
            elif response.status_code == 202:
                #no filter setting
                filter = ""
            elif response.status_code == 303:
                #generic error
                filter = ""
        except Exception as e:
            print(e)

        payload = dict(id=current_user, filter=filter)
        try:
            response = requests.post(MESSAGE_ENDPOINT+"/mailbox",
                                     json=payload,
                                     timeout=REQUESTS_TIMEOUT_SECONDS
                                     )
            # response from mailbox microservice:
            # {
            #     sent: <msg1>,<msg2>
            #     recived: <msg2>
            #     draft: <msg1>
            # }
            if response.status_code == 200:
                flash("you can't see this information")
                return render_template("login.html")
            elif response.status_code == 302:
                print("infromation recived")
                json_response = response.json()
                #TODO: parsing json to retrive this three information:
                sent_message = ""
                draft_message = ""
                recived_message = ""
                return render_template("mailbox.html", messages=recived_message, sendMessages=sent_message, draftMessages=draft_message)
        except Exception as e:
            print(e)
    else:
        return redirect('/login')


@users.route('/users/', methods=['POST', 'GET'])
def user():
    '''
        Show a list of the online and offline users registered to MessageInABottle.
        Also provide the functionality for block and report a user.
    '''
    if current_user is not None and hasattr(current_user, 'id'):  # check if the user is logged
        print("sei loggato, operazione 'users' accettata")
        owner_blocklist = current_user.id
        user_in_blacklist = request.args.get("block_user_id")  # is the id of the user that he wants to block (it could be put in the URL)

        # chek if in the URL there is the id of the user to block
        if user_in_blacklist is not None:
            # put user in the blacklist
            if request.args.get("block") == "1":  # is a parameter that could be in the URL to identify the blacklist action
                add_to_blacklist(owner_blocklist, user_in_blacklist)

            # remove user from the blacklist
            elif request.args.get("block") == "0":
                remove_to_blacklist(owner_blocklist, user_in_blacklist)
            else:
                owner_reportlist = current_user.id
                user_in_reportlist = request.args.get("block_user_id")
                add_to_reportlist(owner_reportlist, user_in_reportlist)

        # user_in_blacklist is none:
        result = retrive_users(current_user.id)

        # Read the response and put it in the _users variable
        if result == "error":
            flash("error, retry later")
            redirect('/mailbox')
        else:
            return render_template("users.html", users=result)
    else:
       print("user not logged")
       return redirect('/login')
