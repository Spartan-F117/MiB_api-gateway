from flask import Blueprint, render_template, flash, redirect, request
import requests
from flask_login import login_required, current_user, logout_user
from mib import app
from mib.forms import UserForm, SendForm
from mib.auth.user import User
import base64
from datetime import date, datetime
from mib.rao.user_manager import UserManager

users = Blueprint('users', __name__)

LOTTERY_ENDPOINT = app.config['LOTTERY_MS_URL']
USERS_ENDPOINT = app.config['USERS_MS_URL']
REQUESTS_TIMEOUT_SECONDS = 60
MESSAGE_ENDPOINT = app.config['MESSAGE_MS_URL']


def add_to_blacklist(owner_blocklist, user_in_blacklist):
    payload = dict(id_owner=owner_blocklist, id_to_insert=user_in_blacklist)
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
        response = requests.post(USERS_ENDPOINT + "/delete_blacklist", json=payload, timeout=REQUESTS_TIMEOUT_SECONDS)
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
            print("user already reported")
            flash("user already reported")
    except Exception as e:
        print(e)

def send_message(sender_id, sender_nickname, receiver_id, receiver_nickname, body, delivery_date, image):
    
    print('trying sending message....')

    payload = dict(sender_id=sender_id, sender_nickname=sender_nickname,receiver_id=receiver_id,receiver_nickname=receiver_nickname, body=body, delivery_date=delivery_date, image=image)
    try:
        response = requests.post(MESSAGE_ENDPOINT + "/send_message", json=payload, timeout=REQUESTS_TIMEOUT_SECONDS)
        if response.status_code == 202:
            print("message sent")
        else:
            print("message not sent")
    except Exception as e:
        print(e)
    
    print('received response for sending message....')

    return 200

def retrive_users(id_):

    payload = dict(id=str(id_))

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

def get_user_by_nickname(nickname):

    print('trying receiving user id from nickname....')
             
    try:
        response = requests.get("%s/user_nickname/%s" % (USERS_ENDPOINT, nickname),
                                timeout=REQUESTS_TIMEOUT_SECONDS)
        json_payload = response.json()
        user = None

        if response.status_code == 200:
            user = User.build_from_json(json_payload)

    except Exception as e:
        print(e)

    print('received response for user id from nickname....')

    return user

def delete_draft_message(draft_id):

    print('trying deliting draft message....')

    try:
        response = requests.get("%s/delete_draft_message/%s" % (MESSAGE_ENDPOINT, draft_id),
                                timeout=REQUESTS_TIMEOUT_SECONDS)

    except Exception as e:
        print(e)

    print('received response for delete draft message....')

def draft_message_info(draft_id):
    print('trying receiving draft message info....')

    try:
        response = requests.get("%s/draft_message_info/%s" % (MESSAGE_ENDPOINT, draft_id),
                                timeout=REQUESTS_TIMEOUT_SECONDS)
        json_payload = response.json()

    except Exception as e:
        print(e)

    print('received response for draft message info....')

    return json_payload

def blacklist_request(sender_id, receiver_id):
    print('trying receiving blacklist info....')

    try:
        response = requests.get("%s/blacklist_info?sender_id=%s&receiver_id=%s" % (USERS_ENDPOINT, sender_id, receiver_id),
                                timeout=REQUESTS_TIMEOUT_SECONDS)
        json_payload = response.json()

    except Exception as e:
        print(e)

    print('received response for blacklist info....')

    if response.status_code == 200: #blacklist found
        return False
    else:
        return True

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


@users.route('/users/', methods=['POST', 'GET'])
@login_required
def user():
    '''
        Show a list of the online and offline users registered to MessageInABottle.
        Also provide the functionality for block and report a user.
    '''
    #if current_user is not None and hasattr(current_user, 'id'):  # check if the user is logged
    owner_blocklist = current_user.id
    user_in_blacklist = request.args.get("block_user_id")  # is the id of the user that he wants to block (it could be put in the URL)

    # chek if in the URL there is the id of the user to block
    if user_in_blacklist is not None:
        # put user in the blacklist
        if request.args.get("block") == "1":  # is a parameter that could be in the URL to identify the blacklist action
            add_to_blacklist(str(owner_blocklist), str(user_in_blacklist))
            print("user added to blacklist")
        # remove user from the blacklist
        elif request.args.get("block") == "0":
            remove_to_blacklist(str(owner_blocklist), str(user_in_blacklist))
        else:
            owner_reportlist = current_user.id
            user_in_reportlist = request.args.get("block_user_id")
            add_to_reportlist(str(owner_reportlist), str(user_in_reportlist))

    # user_in_blacklist is none:
    result = retrive_users(current_user.id)

    list_user = []
    for item in result:
        user = User.build_from_json(item)

        list_user.append(user)

    # Read the response and put it in the _users variable
    if result == "error":
        flash("error, retry later")
        redirect('/mailbox')
    else:
        return render_template("users.html", users=list_user)
    #else:
    #   print("user not logged")
    #   return redirect('/login')


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
        if request.method == 'GET': #filter is asked
            
            #payload = dict(user_id=current_user.id)
            print('trying seeing user filter....')
            response = requests.get(USERS_ENDPOINT + '/profile_filter/'+str(current_user.id),
                                        timeout=REQUESTS_TIMEOUT_SECONDS
                                        )
            print('received response for user filter....')
            json_response = response.json()
            print(json_response)
            print("filtri: "+json_response['filter'])
            user_filter_list = json_response['filter']

            return render_template("profile_info.html", current_user=current_user,user_filter_list=user_filter_list)
        else: #apply the modification in the form
            firstname = request.form.get('firstname')
            lastname = request.form.get('surname')
            new_password = request.form.get('new_password')
            old_password = request.form.get('old_password')
            birthday = str(request.form.get('birthday'))
            location = request.form.get('location')
            filter = request.form.get('filter')
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
                user_filter_list = json_response['filter']

                return render_template("profile_info.html", current_user=current_user,user_filter_list=user_filter_list)
            else: #if the user presses the other button he changes is information with the info in the form
                print("change info branch")
                #TODO richiesta modifica info
                payload = dict(new_password=new_password, firstname=firstname,
                           surname=lastname, birthday=birthday,
                           old_password=old_password, location=location, user_id=current_user.id)
                
                print('trying updating user info....')
                response = requests.post(USERS_ENDPOINT + '/change_info',
                                            json=payload,
                                            timeout=REQUESTS_TIMEOUT_SECONDS
                                            )
                print('received response for update info....')
                json_response = response.json()
                user_filter_list = json_response['filter']

                status = response.status_code

                if status == 201:
                    print("info updated")
                    return redirect('/profile')
                else:
                    print("wrong password")
                return render_template("profile_info.html", current_user=current_user, user_filter_list=user_filter_list)
    else:
        return redirect('/login')


# This route is to delete an account
@users.route('/deleteAccount/', methods=['POST', 'GET'])
@login_required
def delete_account():
    """
        This funcionality allows user to delete his/her account from MyMessageInTheBottle.
        The function will delete the account only for the logged user, and will redirect in the start page

        if confirm_button is pressed the account is deleted (the elimination is done putting True in the is_deleted flag)
    """
    print("siamo nella delete")

    if request.method == "GET":
        print("siamo nella GET DELETE")
        return render_template("delete.html")
    else:
        payload = dict(user_id=str(current_user.id))
        try:
            response = requests.post(USERS_ENDPOINT + "/delete_user",
                                     json=payload,
                                     timeout=REQUESTS_TIMEOUT_SECONDS
                                     )
            if response.status_code == 201:
                print("Account deleted")
                logout_user()
                return render_template('delete.html', is_deleted=True)
            elif response.status_code == 301:
                print("Generic error")
                return redirect("/mailbox")
        except Exception as e:
            print(e)

    return render_template("delete.html")

# #This route is to see the mailbox
@users.route('/mailbox/', methods=['GET'])
@login_required
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
    

    # look for filter
    #payload_filter = dict(id=current_user)
    try:
        response = requests.get(USERS_ENDPOINT + "/profile_filter/"+str(current_user.id),
                                    timeout=REQUESTS_TIMEOUT_SECONDS
                                    )
        if response.status_code == 201:
            #filter recived
            filter = response.json()['filter']
        elif response.status_code == 202:
            #no filter setting
            filter = ""
        elif response.status_code == 303:
            #generic error
            filter = ""
    except Exception as e:
        print(e)

    payload = dict(id=str(current_user.id), filter=str(filter))
    print("filter")
    print(filter)
    try:
        print("message_endpoint")
        print(MESSAGE_ENDPOINT)
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
        if response.status_code == 201:
            flash("you can't see this information")
            return render_template("login.html")
        elif response.status_code == 202:
            print("infromation recived")
            json_response = response.json()
            sent_message = json_response['sent_message']
            draft_message = json_response['draft_message']
            recived_message = json_response['received_message']
            print("rec_m")
            print(recived_message)
            print("sent_m")
            print(sent_message)
            print("draft_m")
            print(draft_message)
            return render_template("mailbox.html", messages=recived_message, sendMessages=sent_message, draftMessages=draft_message)
    except Exception as e:
        print(e)
   


@users.route('/send/', methods=['GET','POST'])
@login_required  
def send():
    isDraft =False                                                  # The message by default is set as "NOT A DRAFT"
    draftReciever = request.args.get("reciever")                    # take argument "reciever"
    draftBody = request.args.get("body")                            # take argument "body"
    isReply = request.args.get("reply")                             # take arument reply
    draft_id = request.args.get('draft_id')                         # # take argument "draft_id"
    form = SendForm()
    if request.method == 'POST':
        if form.data is not None and form.data['recipient'] is not None: #check if the receiver is None
            # check for images
            if request.files['image_file'] is not None:
                image_binary=base64.b64encode(request.files['image_file'].read())
            else:
                image_binary = ""
            #check if the send or draft buttom is pressed
            if request.form['submit_button'] == "Send" or request.form['submit_button'] == 'Save as draft':
                if draft_id is not None:
                    delete_draft_message(draft_id)
                if form.data['delivery_date'] is None: #if no date is specified, the current date is put
                    delivery_date=date.today()
                else:
                    delivery_date=form.data['delivery_date']
                body=form.data['body']
                for nick in form.data['recipient']: #for each receiver that specified in the form create a message
                    result=get_user_by_nickname(nick)
                    receiver_id = result.id
                    blacklist_response = blacklist_request(current_user.id, receiver_id)
                    print("prima if")
                    if blacklist_response == True:
                        print("dentro if")
                        if request.form['submit_button'] != 'Save as draft': #check whitch button is pressed and set the corresponding flag
                            print("dentro send")
                            send_message(str(current_user.id),current_user.nickname, str(receiver_id), nick, body, str(delivery_date),str(image_binary))
                            print("message sent")
                        else:
                            #TODO create drfat message request
                            pass
            elif request.form['submit_button'] == 'Send as message':
                if form.data['delivery_date'] is None:
                    delivery_date=date.today()
                else:
                    delivery_date=form.data['delivery_date']
                body=form.data['body']
                for nick in form.data['recipient']:
                    result=get_user_by_nickname(nick)
                    receiver_id = result.id
                    blacklist_response = blacklist_request(current_user.id, receiver_id)
                    if blacklist_response == False:
                        image= image_binary.decode('utf-8')
                        #TODO send draft message request
            elif request.form['submit_button'] == "Save changes":
                body=form.data['body']
                if form.data['delivery_date'] is None:
                    delivery_date=date.today()
                else:
                    delivery_date=form.data['delivery_date']
                image= image_binary.decode('utf-8')
                for nick in form.data['recipient']:
                    result=get_user_by_nickname(nick)
                    receiver_id = result.id
                    #TODO update draft message request
                    pass
            result = retrive_users(current_user.id)
            new_user_list = []
            for item in result:
                user = User.build_from_json(item)
                new_user_list.append(user.nickname)
            dictUS = {}
            for el in new_user_list:
                dictUS[el] = 0
            if draftReciever is not None:
                dictUS[draftReciever] = 1
            return render_template("send.html",  current_user=current_user, current_user_firstname=current_user.firstname, form=form, user_list=dictUS, is_submitted=True)
        
    else:
        #show the form and fill it if it's to modify a draft message
        
        form.body.data=draftBody
        result = retrive_users(current_user.id)
        new_user_list = []
        for item in result:
            user = User.build_from_json(item)
            new_user_list.append(user.nickname)
        dictUS = {}
        for el in new_user_list:
            dictUS[el] = 0

        if (isReply is not None and isReply) and (draftReciever is not None):
            if draftReciever is not None:
                form.body.data=str(draftReciever)+' wrote:\n'+str(draftBody)+'\n-----------------\n'

        if draft_id is not None:
            result = draft_message_info(draft_id)
            dictUS[result.receiver_nickname] = 1

        return render_template("send.html", current_user=current_user, current_user_firstname=current_user.firstname, form=form, user_list=dictUS, draft_id=draft_id), 200
        