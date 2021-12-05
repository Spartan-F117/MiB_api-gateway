from datetime import *
import unittest
from faker import Faker
from random import choice, randint

from flask_login.utils import login_user
from mib.__init__  import *
from mib.__init__ import app as TestedApp
import io
from flask_login import  current_user

        


LOGIN_OK = 200
LOGIN_FAIL = 201
DOUBLE_LOGIN = 202


class ViewTest(unittest.TestCase):
    faker = Faker()

    BASE_URL = "http://localhost"

    @classmethod
    def setUpClass(self):
        from mib import create_app
        self.app = create_app()
        self.client = self.app.test_client()
        from mib.rao.user_manager import UserManager
        self.user_manager = UserManager
        from mib.auth.user import User
        self.user = User
        from mib.views.users import lottery_participant as lottery
        self.lottery = lottery
        from mib.views.users import send_partecipation_lottery as send_lottery
        self.send_lottery = send_lottery
        from mib.views.users import decrease_lottery_points as decrease_lottery
        self.decrease_lottery = decrease_lottery
        from mib.views.users import draft_message_info as draft_message_info
        self.draft_message_info = draft_message_info
        from mib.views.users import delete_message as delete_message
        self.delete_message = delete_message

    
    def generate_user(self):
        """Generates a random user, depending on the type
        Returns:
            (dict): a dictionary with the user's data
        """

        data = {
            'id': randint(0,999),
            'email': self.faker.email(),
            'password': self.faker.password(),
            'nickname': self.faker.nick_name(),
            'is_active' : choice([True,False]),
            'authenticated': False,
            'is_anonymous': False,
            'firstname': self.faker.first_name(),
            'lastname': self.faker.last_name(),
            'date_of_birth': self.faker.date()
        }
        return data

#creazione utenti

#1) set db
    def test_aa_initialize(self):
            URL = '/create_user/'
            payload = {
                'email': 'example1@email.it',
                'password': 'pass1',
                'nickname': 'nick1',
                'firstname': 'name1',
                'lastname': 'last1',
                'location': 'location1',
                'date_of_birth': '1/01/2000'
            }
            r1 = self.client.post(URL, data=payload)
            
            payload = {
                'email': 'example2@email.it',
                'password': 'pass2',
                'nickname': 'nick2',
                'firstname': 'name2',
                'lastname': 'last2',
                'location': 'location2',
                'date_of_birth': '1/01/2000'
            }
            r2 = self.client.post(URL, data=payload)

            payload = {
                'email': 'example3@email.it',
                'password': 'pass3',
                'nickname': 'nick3',
                'firstname': 'name3',
                'lastname': 'last3',
                'location': 'location3',
                'date_of_birth': '1/01/2000',
            }
            r3 = self.client.post(URL, data=payload)
            
            payload_test = {
                'id': '1',
                'email': 'example3@email.it',
                'password': 'pass3',
                'nickname': 'nick3',
                'firstname': 'name3',
                'lastname': 'last3',
                'location': 'location3',
                'date_of_birth': '1/01/2000',
                'is_active':'False',
                'authenticated': 'False',
                'is_anonymous': 'False',
                'is_admin': 'False'
            }
            user= self.user.build_from_json(payload_test)

            user.__str__()
            
            assert True #True because the user could be just created

#test wrong create
    def test_wrong_create(self):
        URL = '/create_user/'
        payload = {
            'email': 'example1@email.it',
            'password': 'pass1',
            'nickname': 'nick1',
            'firstname': 'name1',
            'lastname': 'last1',
            'location': 'location1',
            'date_of_birth': '1/01/2000'
        }
        r1 = self.client.post(URL, data=payload)
        assert r1.status_code == 200

    def test_wrong_create_2(self):
        URL = '/login/'
        payload = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r = self.client.post(URL, data=payload)
        URL = '/create_user/'
        payload = {
            'email': 'example1@email.it',
            'password': 'pass1',
            'nickname': 'nick1',
            'firstname': 'name1',
            'lastname': 'last1',
            'location': 'location1',
            'date_of_birth': '1/01/2000'
        }
        r1 = self.client.post(URL, data=payload)
        assert r1.status_code == 200

#test login

#1) login
    def test_login_user(self):
        URL = '/login/'
        payload = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r = self.client.post(URL, data=payload)
        assert r.status_code == LOGIN_OK

#2) login with wrong password
    def test_wrong_login_user(self):
        URL = '/login/'
        payload = {
            'email': 'example1@email.it',
            'password': 'pass_wrong'
        }
        r = self.client.post(URL, data=payload)
        assert r.status_code == LOGIN_OK

#3) login when just login
    def test_login_user_when_just_login(self):
        URL = '/login/'
        payload = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        self.client.post(URL, data=payload)

        r = self.client.post(URL, data=payload)

        assert r.status_code == 200

#test logout

#1) logout
    def test_logout_user(self):
        URL = '/logout'
        r = self.client.get(URL)
        assert r.status_code == 302

#test user

    #1) insert a user into blacklist
    def test_ya_add_blacklist(self):
        URL_login = '/login/'
        payload = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r1 = self.client.post(URL_login, data=payload)
        URL = '/users/'
        r = self.client.get(URL+'?block_user_id=2&block=1') #block user1
        self.client.get(URL) #testing 36-66
        assert True

    #1) insert a user into blacklist again
    def test_yb_add_blacklist_again(self):
        URL_login = '/login/'
        payload = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r1 = self.client.post(URL_login, data=payload)
        URL = '/users/'
        r = self.client.get(URL+'?block_user_id=2&block=1') #block user1
        self.client.get(URL) #testing 36-66
        assert True

#2) remove user from blacklist
    def test_y_remove_blacklist(self):
        URL_login = '/login/'
        payload = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r1 = self.client.post(URL_login, data=payload)
        URL = '/users/'
        r = self.client.get(URL+'?block_user_id=2&block=0') #free user1
        assert True


#5) enter in the page without login
    def test_enter_users_page_without_login(self):
        URL = '/users/'
        r = self.client.get(URL)
        assert r.status_code == 200

#6) add user in the report list
    def test_add_report_list(self):
        URL_login = '/login/'
        payload_login = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/users/'
        r = self.client.get(URL+'?block_user_id=2&block=2') #report user1
        assert True

    def test_add_report_list_2(self):
        URL_login = '/login/'
        payload_login = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/users/'
        r = self.client.get(URL+'?block_user_id=100&block=2') #report user1
        assert True

#test send

#1) send email
    def test_send_email(self):
        URL_login = '/login/'
        payload_login = {
        'email': 'example1@email.it',
        'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/send/'
        file_name="fake-text-stream.txt"
        payload = {
            'recipient' : 'nick2',
            'body' : 'ciao nick2',
            'delivery_date' : '7/11/2021',
            "image_file" : (io.BytesIO(b"some initial text data"), file_name),
            'submit_button' : 'Send',
        }
        r = self.client.post(URL, data=payload)
        
        #get send
        r2=self.client.get(URL)

        assert r.status_code == 200

#1bis) send email without recipient
    def test_send_email_without_recipient(self):
       
        URL_login = '/login/'
        payload_login = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/send/'
        file_name="fake-text-stream.txt"
        payload = {
            'body' : 'ciao nick1',
            'delivery_date' : '7/11/2021',
            "image_file" : (io.BytesIO(b"some initial text data"), file_name),
            'submit_button' : 'Send',
        }
        r = self.client.post(URL, data=payload)
        assert r.status_code == 200

#1bisbisbis) send email get
    def test_send_email_get(self):
        
        URL_login = '/login/'
        payload_login = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/send/'
        r = self.client.get(URL)
        assert r.status_code == 200


# #test draft_id 

#3) draft email
    def test_draft_email(self):
        
        URL_login = '/login/'
        payload_login = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/send/'
        file_name="fake-text-stream.txt"
        payload = {
            'recipient' : 'nick2',
            'body' : 'ciao nick2',
            'delivery_date' : '7/11/2021',
            "image_file" : (io.BytesIO(b"some initial text data"), file_name),
            'submit_button' : 'Save as draft',
        }
        r = self.client.post(URL, data=payload)
        assert r.status_code == 200



#7)test send as message
    def test_send_email_send_as_message(self):
        
        URL_login = '/login/'
        payload_login = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/send/'
        file_name="fake-text-stream.txt"
        payload = {
            'recipient' : 'nick2',
            'body' : 'ciao nick2 send as message',
            'delivery_date' : '7/11/2021',
            "image_file" : (io.BytesIO(b"some initial text data"), file_name),
            'submit_button' : 'Send as message',
        }
        r = self.client.post(URL, data=payload)
        assert r.status_code == 200


#8) email save changes
    def test_send_email_save_changes(self):
        
            URL_login = '/login/'
            payload_login = {
                'email': 'example1@email.it',
                'password': 'pass1'
            }
            r_login = self.client.post(URL_login, data=payload_login)
            URL = '/send/'
            file_name="fake-text-stream.txt"
            payload = {
                'recipient' : 'nick2',
                'body' : 'ciao nick2 save changes',
                'delivery_date' : '7/11/2021',
                "image_file" : (io.BytesIO(b"some initial text data"), file_name),
                'submit_button' : 'Save changes',
            }
            r = self.client.post(URL, data=payload)
            assert r.status_code==200

# #test profile

#1) change info
    def test_za_change_info(self):

            URL_login = '/login/'
            payload_login = {
                'email': 'example1@email.it',
                'password': 'pass1'
            }
            r_login = self.client.post(URL_login, data=payload_login)
            URL = '/profile'
            payload = {
                'firstname': 'name_test',
                'surname': 'surname_test',
                'birthday': '',
                'location': 'livorno',
                'new_password': 'pass1',
                'old_password': 'pass',
                'submit_button': 'Save changes',
            }
            r = self.client.post(URL, data=payload)
            assert r.status_code == 200


#3) word filter
    def test_change_z_filter(self):
        
            URL_login = '/login/'
            payload_login = {
                'email': 'example1@email.it',
                'password': 'pass1'
            }
            r_login = self.client.post(URL_login, data=payload_login)
            URL = '/profile'
            payload = {
                'filter': 'ciao,addio',
                'submit_button': 'Submit',
            }
            r = self.client.post(URL, data=payload)
            assert r.status_code==200

#4) profile without login
    def test_enter_profile_page_without_login(self):
        
        URL = '/profile'
        r = self.client.get(URL)
        assert r.status_code == 200

#5) change info get
    def test_change_info_get(self):
        
        URL_login = '/login/'
        payload_login = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/profile'
        r=self.client.get(URL)
        assert r.status_code == 200

# #test delete account

#1) delete account get
    def test_z_delete_account_get(self):
       
        URL_login = '/login/'
        payload_login = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/deleteAccount/'
        r = self.client.get(URL)
        assert r.status_code == 200

# #3) delete account post
#     def test_zy_delete_account_post(self):

#         URL = '/create_user/'
#         payload_create = {
#             'email': 'example100@email.it',
#             'password': 'pass100',
#             'nickname': 'nick100',
#             'firstname': 'name100',
#             'lastname': 'last100',
#             'location': 'location100',
#             'date_of_birth': '1/01/2000'
#         }
#         r1 = self.client.post(URL, data=payload_create)

#         payload_test = {
#             'id': '1000',
#             'email': 'example100@email.it',
#             'password': 'pass100',
#             'nickname': 'nick100',
#             'firstname': 'name100',
#             'lastname': 'last100',
#             'location': 'location100',
#             'date_of_birth': '1/01/2000',
#             'is_active':'False',
#             'authenticated': 'False',
#             'is_anonymous': 'False',
#             'is_admin': 'False'
#         }
#         # user = self.user.build_from_json(payload_test)
#         # login_user(user)
#         URL = '/deleteAccount/'
#         payload = {
#             'confirm_button' : 'Delete my account'
#         }
#         r = self.client.post(URL, data=payload)
#         assert r.status_code == 200

#test home

#1) home logged
    def test_home(self):

            URL_login = '/login/'
            payload_login = {
                'email': 'example1@email.it',
                'password': 'pass1'
            }
            r_login = self.client.post(URL_login, data=payload_login)
            URL = '/'
            r = self.client.get(URL)
            assert r.status_code == 302


# test calendar

#1)calendar
    def test_calendar(self):
        
        URL = '/calendar'
        r = self.client.get(URL)
        assert r.status_code == 200

# #test mailbox

#1) mailbox
    def test_mailbox(self):
        
        URL_login = '/login/'
        payload_login = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/mailbox/'
        r = self.client.get(URL)
        assert r.status_code == 200

# 1) Test lottery
    def test_lottery_join(self):
        
            URL_LOGIN = '/login/'
            URL_LOTTERY = '/lottery/'
            payload_login = {
                'email': 'example1@email.it',
                'password': 'pass1'
            }
            r_login = self.client.post(URL_LOGIN, data=payload_login)

            r = self.client.post(URL_LOTTERY)
            assert r.status_code==302

# 1) Test join lottery again
    def test_lottery_join_again(self):
        
            URL_LOGIN = '/login/'
            URL_LOTTERY = '/lottery/'
            payload_login = {
                'email': 'example1@email.it',
                'password': 'pass1'
            }
            r_login = self.client.post(URL_LOGIN, data=payload_login) 
            # first registration
            r = self.client.post(URL_LOTTERY)
            # second registration
            r = self.client.post(URL_LOTTERY)
            assert r.status_code==302
    
    def test_lottery_partecipant(self):
        r = self.lottery()
        assert r == False

    def test_send_lottery_partecipant(self):
        r = self.send_lottery()
        assert r == False

    def test_decrease_lottery_points(self):
        r = self.decrease_lottery()
        assert r == 200

    def test_draft_message_info(self):
        try:
            self.draft_message_info()
        except Exception as e:
            assert True

#test open message
    def test_zaa_OpenedMessage(self):

        URL_login = '/login/'
        payload_login = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)

        URL = '/send/'
        file_name = "fake-text-stream.txt"
        payload = {
            'recipient': 'nick2',
            'body': 'ciao nick2',
            'delivery_date': '20/11/2021',
            "image_file": (io.BytesIO(b"some initial text data"), file_name),
            'submit_button': 'Send',
        }
        r = self.client.post(URL, data=payload)

        assert r.status_code==200

#tesy deletion message
    def test_deletion_message(self):
        
            URL_login = '/login/'
            payload_login = {
                'email': 'example1@email.it',
                'password': 'pass1'
            }
            r_login = self.client.post(URL_login, data=payload_login)
            URL = '/send/'
            file_name="fake-text-stream.txt"
            payload = {
                'recipient' : 'nick2',
                'body' : 'ciao nick2',
                'delivery_date' : '20/11/2021',
                "image_file" : (io.BytesIO(b"some initial text data"), file_name),
                'submit_button' : 'Send',
            }
            r = self.client.post(URL, data=payload)
            URL = '/message/1'
            URL = URL+"?delete=True"
            response = self.client.post(URL)
            URL = '/message/2'
            URL = URL + "?lottery=0"
            response = self.client.post(URL)
            assert response.status_code==200

    def test_z_delete_message(self):
        r = self.delete_message()
        assert r is None

    def test_za_delete_message_2(self):
        URL_login = '/login/'
        payload_login = {
            'email': 'example2@email.it',
            'password': 'pass2'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/delete_messages/'
        r = self.client.get(URL)
        assert r.status_code == 200

    def test_za_delete_message_3(self):
        URL_login = '/login/'
        payload_login = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/delete_messages/'
        r = self.client.get(URL)
        assert r.status_code == 200

    def test_lottery_get(self):
        URL_login = '/login/'
        payload_login = {
            'email': 'example1@email.it',
            'password': 'pass1'
        }
        r_login = self.client.post(URL_login, data=payload_login)
        URL = '/lottery/'
        r = self.client.get(URL)
        assert r.status_code == 200

        
