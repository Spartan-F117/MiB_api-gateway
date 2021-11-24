from flask import Blueprint, render_template, flash, redirect
import requests
from flask_login import LoginManager, current_user
from mib import app

users = Blueprint('users', __name__)

LOTTERY_ENDPOINT = app.config['LOTTERY_MS_URL']
REQUESTS_TIMEOUT_SECONDS = 60
USERS_ENDPOINT = app.config['USERS_MS_URL']
MESSAGE_ENDPOINT = ""

# #This route is to see the mailbox
@users.route('/mailbox/', methods=['GET'])
def inbox():
    '''
     Shows the mailbox of the user divded into three parts
     1) The Inbox part shows the received messages
     2) The Sent part shows the messages that user sent
     3) The Draft part shows the messages in the draft

     It also provides the functionality for the user to delete future
     messages if the user is lottery winner
    '''
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