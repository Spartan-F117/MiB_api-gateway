from flask import Blueprint, render_template, flash, redirect, request
import requests
from flask_login import LoginManager, current_user
from mib import app
from mib.forms import UserForm

users = Blueprint('users', __name__)

LOTTERY_ENDPOINT = app.config['LOTTERY_MS_URL']
REQUESTS_TIMEOUT_SECONDS = 60
USERS_ENDPOINT = app.config['USERS_MS_URL']
MESSAGE_ENDPOINT = ""


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
        #return render_template("login.html")    #-> form is undefined

#This route is to delete an account 
@users.route('/deleteAccount', methods=['POST','GET'])
def delete_account():
    """
        This funcionality allows user to delete his/her account from MyMessageInTheBottle.
        The function will delete the account only for the logged user, and will redirect in the start page
    """
    if request.method == 'GET': #show the form
        if current_user is not None and hasattr(current_user, 'id'):
            return render_template("delete.html")
        else:
            return redirect('/login')
    else:
        if request.form['confirm_button'] == 'Delete my account': #if confirm_button is pressed the account is deleted (the elimination is done putting True in the is_deleted flag)
            payload = dict(id=current_user)
            try:
                response = requests.post(USERS_ENDPOINT + "/delete_user",
                                        json=payload,
                                        timeout=REQUESTS_TIMEOUT_SECONDS
                                        )
                if response.status_code == 201:
                    print("Account deleted")
                    return render_template('delete.html', is_deleted=True)
                elif response.status_code == 400:
                    print("user not logged")
                    return redirect("/login")
            except Exception as e:
                print(e)
        else:
            return redirect('/')
