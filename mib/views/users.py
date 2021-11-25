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


@users.route('/profile', methods=['GET','POST'])
def profile():
    """
        This functionality allows to users to view the user's profile.
        Retrive the information about the user in the db, and pass as argument
        the values in the 'profile_info.html' template.
        If the user who try to access this service is not logged, will be render in the
        'home' page
    """
    if current_user is not None and hasattr(current_user, 'id'): #check if the user is logged
        if not request.form.is_submitted(): #filter is asked
            
            payload = dict(user_id=current_user.id)
            print('trying seeing user filter....')
            response = requests.get(USERS_ENDPOINT + '/profile_filter',
                                        json=payload,
                                        timeout=REQUESTS_TIMEOUT_SECONDS
                                        )
            print('received response for user filter....')
            json_response = response.json()

            user_filter_list = json_response.get['filter']

            return render_template("profile_info.html", current_user=current_user,user_filter_list=user_filter_list)
        else: #apply the modification in the form
            firstname = request.form.data['firstname']
            lastname = request.form.data['lastname']
            new_password = request.form.data['new_password']
            old_password = request.form.data['old_password']
            birthday = str(request.form.data['birthday'])
            location = request.form.data['location']
            filter = request.form.data['filter']
            if 'filter' in request.form: #if the user presses the filter button i change the word filter
                print("change filter branch")
    
                payload = dict(filter=filter, user_id=current_user.id)
                print('trying updating user filter....')
                response = requests.post(USERS_ENDPOINT + '/change_filter',
                                            json=payload,
                                            timeout=REQUESTS_TIMEOUT_SECONDS
                                            )
                print('received response for update filter....')
                json_response = response.json()
                user_filter_list = json_response.get['filter']

                return render_template("profile_info.html", current_user=current_user,user_filter_list=user_filter_list)
            else: #if the user presses the other button he changes is information with the info in the form
                print("change info branch")
                #TODO richiesta modifica info
                payload = dict(new_password=new_password, firstname=firstname,
                           lastname=lastname, birthday=birthday,
                           old_password=old_password, location=location, user_id=current_user.id)
                
                print('trying updating user info....')
                response = requests.post(USERS_ENDPOINT + '/change_info',
                                            json=payload,
                                            timeout=REQUESTS_TIMEOUT_SECONDS
                                            )
                print('received response for update info....')
                json_response = response.json()
                user_filter_list = json_response.get['filter']

                status = response.status_code

                if status == 201:
                    print("info updated")
                else:
                    print("wrong password")
                return render_template("profile_info.html", current_user=current_user,user_filter_list=user_filter_list)
    else:
        return redirect('/login')