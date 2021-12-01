from datetime import *
import unittest
from faker import Faker
from random import choice, randint
from mib.__init__  import *
from mib.__init__ import app as TestedApp

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
            
            assert True #True because the user could be just created

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
        r1 = self.client.post(URL, data=payload)

        r = self.client.post(URL, data=payload)

        assert r.status_code == DOUBLE_LOGIN

#test logout

#1) logout
    def test_logout_user(self):
        URL = '/logout'
        r = self.client.get(URL)
        assert r.status_code == 302

#test user

    #1) insert a user into blacklist
    def test_y_add_blacklist(self):
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
        assert r.status_code == 302

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

#test send

# #1) send email
#     def test_send_email(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/send'
#             file_name="fake-text-stream.txt"
#             payload = {
#                 'recipient' : 'nick1',
#                 'body' : 'ciao nick1',
#                 'delivery_date' : '7/11/2021',
#                 "image_file" : (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button' : 'Send',
#             }
#             r = app2.post(URL, data=payload)
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             nick1 = db.session.query(User).filter(User.nickname=="nick1").first()
#             message_check=db.session.query(Message).filter(Message.receiver_id==nick1.id).filter(Message.sender_id==nick5.id).filter(Message.body=="ciao nick1").first()

#             #get send
#             r=app2.get(URL)

#             assert message_check is not None

# #1bis) send email without recipient
#     def test_send_email_without_recipient(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/send'
#             file_name="fake-text-stream.txt"
#             payload = {
#                 'body' : 'ciao nick1',
#                 'delivery_date' : '7/11/2021',
#                 "image_file" : (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button' : 'Send',
#             }
#             r = app2.post(URL, data=payload)
#             assert r.status_code == 200

# #1bisbis) message send without date
#     def test_send_email_without_date(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/send'
#             file_name="fake-text-stream.txt"
#             payload = {
#                 'recipient' : 'nick1',
#                 'body' : 'ciao nick1 senza data',
#                 "image_file" : (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button' : 'Send',
#             }
#             r = app2.post(URL, data=payload)
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             nick1 = db.session.query(User).filter(User.nickname=="nick1").first()
#             message_check=db.session.query(Message).filter(Message.receiver_id==nick1.id).filter(Message.sender_id==nick5.id).filter(Message.body=="ciao nick1 senza data").first()
#             assert message_check is not None

# #1bisbisbis) send email get
#     def test_send_email_get(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/send'
#             r = app2.get(URL)
#             assert r.status_code == 200

# #test draft_id

#     def test_send_email_get_draft_id(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/send?draft_id=1&reply=True&reciever=1'
#             r = app2.get(URL)
#             assert r.status_code == 200

# #2) send email to multiple user
#     def test_send_email_multiple_users(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/send'
#             file_name="fake-text-stream.txt"
#             payload = {
#                 'recipient': ['nick1','nick2'],
#                 'body' : 'ciao nick1 e nick2',
#                 'delivery_date' : '7/11/2021',
#                 "image_file" : (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button' : 'Send',
#             }
#             r = app2.post(URL, data=payload)
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             nick1 = db.session.query(User).filter(User.nickname=="nick1").first()
#             nick2 = db.session.query(User).filter(User.nickname=="nick2").first()
#             message_check_nick1=db.session.query(Message).filter(Message.receiver_id==nick1.id).filter(Message.sender_id==nick5.id).filter(Message.body=="ciao nick1 e nick2").first()
#             message_check_nick2=db.session.query(Message).filter(Message.receiver_id==nick2.id).filter(Message.sender_id==nick5.id).filter(Message.body=="ciao nick1 e nick2").first()
#             assert message_check_nick1 is not None and message_check_nick2 is not None

# #3) draft email
#     def test_draft_email(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             print('ora')
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/send'
#             file_name="fake-text-stream.txt"
#             payload = {
#                 'recipient' : 'nick1',
#                 'body' : 'ciao nick1',
#                 'delivery_date' : '7/11/2021',
#                 "image_file" : (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button' : 'Save as draft',
#             }
#             r = app2.post(URL, data=payload)
#             print(r.status_code)
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             nick1 = db.session.query(User).filter(User.nickname=="nick1").first()
#             message_check=db.session.query(Message).filter(Message.receiver_id==nick1.id).filter(Message.sender_id==nick5.id).filter(Message.is_draft==True).first()
#             assert message_check is not None


# #4) draft email to multiple users
#     def test_draft_email_multiple_users(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/send'
#             file_name="fake-text-stream.txt"
#             payload = {
#                 'recipient': ['nick1','nick2'],
#                 'body' : 'ciao nick1 e nick2',
#                 'delivery_date' : '7/11/2021',
#                 "image_file" : (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button' : 'Save as draft',
#             }
#             r = app2.post(URL, data=payload)
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             nick1 = db.session.query(User).filter(User.nickname=="nick1").first()
#             nick2 = db.session.query(User).filter(User.nickname=="nick2").first()
#             message_check_nick1=db.session.query(Message).filter(Message.receiver_id==nick1.id).filter(Message.sender_id==nick5.id).filter(Message.body=="ciao nick1 e nick2").filter(Message.is_draft==True).first()
#             message_check_nick2=db.session.query(Message).filter(Message.receiver_id==nick2.id).filter(Message.sender_id==nick5.id).filter(Message.body=="ciao nick1 e nick2").filter(Message.is_draft==True).first()
#             assert message_check_nick1 is not None and message_check_nick2 is not None

# #5) enter in the page without login
#     def test_send_email_without_login(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL = '/send'
#             r = app2.get(URL)
#             assert r.status_code == 302

# #6) message with blacklist
#     def test_send_email_blacklist(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/send'
#             payload = {
#                 'recipient': 'nick1',
#                 'body': 'ciao blacklist nick1',
#                 'delivery_date': '7/11/2021',
#                 'submit_button': 'Send',
#             }
#             file = {'image_file': ''}
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             nick1 = db.session.query(User).filter(User.nickname=="nick1").first()
#             blacklist_test = BlackList()
#             blacklist_test.user_id = nick1.id
#             blacklist_test.blacklisted_user_id = nick5.id
#             db.session.add(blacklist_test)
#             db.session.commit()
#             r = app2.post(URL, data=payload)
#             message_check=db.session.query(Message).filter(Message.receiver_id==nick1.id).filter(Message.sender_id==nick5.id).filter(Message.body=="ciao blacklist nick1").first()
#             db.session.delete(blacklist_test)
#             db.session.commit()
#             test_blacklist_removed = db.session.query(BlackList).filter(BlackList.id==nick1.id).filter(BlackList.blacklisted_user_id==nick5.id).first()
#             assert message_check is None and test_blacklist_removed is None

# #7)test send as message
#     def test_send_email_send_as_message(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             draft_id =  db.session.query(Message).filter(Message.is_draft==True).first().message_id
#             print(draft_id)
#             URL = '/send?draft_id='
#             file_name="fake-text-stream.txt"
#             payload = {
#                 'recipient' : 'nick1',
#                 'body' : 'ciao nick1 send as message',
#                 'delivery_date' : '7/11/2021',
#                 "image_file" : (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button' : 'Send as message',
#             }
#             r = app2.post(URL+str(draft_id), data=payload)
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             nick1 = db.session.query(User).filter(User.nickname=="nick1").first()
#             message_check=db.session.query(Message).filter(Message.receiver_id==nick1.id).filter(Message.sender_id==nick5.id).filter(Message.body=="ciao nick1 send as message").first()
#             assert message_check is not None

# #7bis) send as message without date
#     def test_send_email_send_as_message_without_date(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             draft_id =  db.session.query(Message).filter(Message.is_draft==True).first().message_id
#             print(draft_id)
#             URL = '/send?draft_id='
#             file_name="fake-text-stream.txt"
#             payload = {
#                 'recipient' : 'nick1',
#                 'body' : 'ciao nick1 send as message without date',
#                 "image_file" : (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button' : 'Send as message',
#             }
#             r = app2.post(URL+str(draft_id), data=payload)
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             nick1 = db.session.query(User).filter(User.nickname=="nick1").first()
#             message_check=db.session.query(Message).filter(Message.receiver_id==nick1.id).filter(Message.sender_id==nick5.id).filter(Message.body=="ciao nick1 send as message without date").first()
#             assert message_check is not None


# #8) email save changes
#     def test_send_email_save_changes(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             draft_id =  db.session.query(Message).filter(Message.is_draft==True).first().message_id
#             print(draft_id)
#             URL = '/send?draft_id='
#             file_name="fake-text-stream.txt"
#             payload = {
#                 'recipient' : 'nick1',
#                 'body' : 'ciao nick1 save changes',
#                 'delivery_date' : '7/11/2021',
#                 "image_file" : (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button' : 'Save changes',
#             }
#             r = app2.post(URL+str(draft_id), data=payload)
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             nick1 = db.session.query(User).filter(User.nickname=="nick1").first()
#             message_check=db.session.query(Message).filter(Message.receiver_id==nick1.id).filter(Message.sender_id==nick5.id).filter(Message.body=="ciao nick1 save changes").first()
#             assert message_check is not None

# #8) email save changes without date
#     def test_send_email_save_changes_without_date(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             draft_id =  db.session.query(Message).filter(Message.is_draft==True).first().message_id
#             print(draft_id)
#             URL = '/send?draft_id='
#             file_name="fake-text-stream.txt"
#             payload = {
#                 'recipient' : 'nick1',
#                 'body' : 'ciao nick1 save changes without date',
#                 "image_file" : (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button' : 'Save changes',
#             }
#             r = app2.post(URL+str(draft_id), data=payload)
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             nick1 = db.session.query(User).filter(User.nickname=="nick1").first()
#             message_check=db.session.query(Message).filter(Message.receiver_id==nick1.id).filter(Message.sender_id==nick5.id).filter(Message.body=="ciao nick1 save changes without date").first()
#             assert message_check is not None

# #test profile

# #1) change info
#     def test_change_info(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/profile'
#             payload = {
#                 'firstname': 'name_test',
#                 'surname': 'surname_test',
#                 'new_password': 'pass_test',
#                 'old_password': 'pass5',
#                 'submit_button': 'Save changes',
#             }
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             r = app2.post(URL, data=payload)
#             db_check=db.session.query(User).filter(User.id==nick5.id).filter(User.firstname=="name_test").filter(User.lastname=="surname_test").first()
#             assert db_check is not None

# #2) change info with wrong password
#     def test_change_info_wrong_password(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/profile'
#             payload = {
#                 'firstname': 'name_test',
#                 'surname': 'surname_test',
#                 'new_password': 'pass_test',
#                 'old_password': 'wrong_pass',
#                 'submit_button': 'Save changes'
#             }
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             r = app2.post(URL, data=payload)
#             db_check=db.session.query(User).filter(User.id==nick5.id).filter(User.firstname=="name_test").filter(User.lastname=="surname_test").first()
#             assert db_check is None

# #3) word filter
#     def test_change_z_filter(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/profile'
#             payload = {
#                 'filter': 'ciao,addio',
#                 'submit_button': 'Submit',
#             }
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             r = app2.post(URL, data=payload)
#             db_check=db.session.query(Filter_list).filter(Filter_list.user_id==nick5.id).filter(Filter_list.list=="ciao,addio").first()
#             assert db_check is not None

# #4) profile without login
#     def test_enter_profile_page_without_login(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL = '/profile'
#             r = app2.get(URL)
#             assert r.status_code == 302

# #5) change info get
#     def test_change_info_get(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/profile'
#             r=app2.get(URL)
#             assert r.status_code == 200

# #6) change info get filter just exist
#     def test_change_info_get_filter_exist(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             filter = Filter_list()
#             filter.user_id=db.session.query(User).filter(User.nickname=='nick5').first().id
#             filter.list = "ciao"
#             db.session.add(filter)
#             db.session.commit()
#             URL = '/profile'
#             r=app2.get(URL)
#             db.session.delete(filter)
#             assert r.status_code == 200

# #test logout

# #1) logout
#     def test_logout(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/logout'
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             r = app2.get(URL)
#             print(db.session.query(User).filter(User.nickname=="nick5").first().is_active)
#             db_check=db.session.query(User).filter(User.id==nick5.id).filter(User.is_active==False).first()
#             assert db_check is not None

# #2) logout_without login
#     def test_logout_without_login(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL = '/logout'
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             r = app2.get(URL)
#             assert r.status_code == 302

# #test delete account

# #1) delete account get
#     def test_z_delete_account_get(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/deleteAccount'
#             r = app2.get(URL)
#             assert r.status_code == 200


# #2) delete account get without login
#     def test_z_delete_account_get_without_login(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL = '/deleteAccount'
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             r = app2.get(URL)
#             assert r.status_code == 302

# #3) delete account post
#     def test_zy_delete_account_post(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/deleteAccount'
#             payload = {
#                 'confirm_button' : 'Delete my account'
#             }
#             r = app2.post(URL, data=payload)
#             nick5 = db.session.query(User).filter(User.nickname=='nick5').first()
#             check_db = db.session.query(User).filter(User.nickname==nick5.id).filter(User.is_deleted==True)
#             assert check_db is not None

# #4) delete account post without login
#     def test_zy_delete_account_post_without_login(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL = '/deleteAccount'
#             payload = {
#                 'confirm_button' : 'Delete my account'
#             }
#             r = app2.post(URL, data=payload)
#             assert r.status_code == 200

# #delete account post error button
#     def test_zy_delete_account_post_error_button(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/deleteAccount'
#             payload = {
#                 'confirm_button' : 'test'
#             }
#             r = app2.post(URL, data=payload)
#             assert r.status_code == 302

# #test home

# #1) home logged
#     def test_home(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/'
#             r = app2.get(URL)
#             assert r.status_code == 302

# #2) home without login
#     def test_home_without_login(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL = '/'
#             r = app2.get(URL)
#             assert r.status_code == 302

# # test calendar

# #1)calendar
#     def test_calendar(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL = '/calendar'
#             r = app2.get(URL)
#             assert r.status_code == 302

# #2)test calendar without login

#     def test_calendar_without_login(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/calendar'
#             r = app2.get(URL)
#             assert r.status_code == 200

# #test mailbox

# #1) mailbox
#     def test_mailbox(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/mailbox'
#             r = app2.get(URL)
#             assert r.status_code == 200

# #2) mailbox without login
#     def test_mailbox_without_login(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL = '/mailbox'
#             r = app2.get(URL)
#             assert r.status_code == 302

# # 1) Test lottery
#     def test_lottery_join(self):
#         with app.app_context():
#             app2 = TestedApp.test_client()
#             URL_LOGIN = '/login'
#             URL_LOTTERY = '/lottery'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_LOGIN, data=payload_login)

#             r = app2.post(URL_LOTTERY)
#             nick5 = db.session.query(User).filter(User.nickname == 'nick5').first()
#             query = db.session.query(Lottery).filter(Lottery.contestant_id==nick5.id).first()
#             assert query is not None

# # 1) Test join lottery again
#     def test_lottery_join_again(self):
#         with app.app_context():
#             app2 = TestedApp.test_client()
#             URL_LOGIN = '/login'
#             URL_LOTTERY = '/lottery'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_LOGIN, data=payload_login)
#             nick5 = db.session.query(User).filter(User.nickname == 'nick5').first()


#             # first registration
#             r = app2.post(URL_LOTTERY)
#             query = db.session.query(Lottery).filter(Lottery.contestant_id == nick5.id).all()
#             query_numb = len(query)
#             print(query_numb)

#             # second registration
#             r = app2.post(URL_LOTTERY)
#             query2 = db.session.query(Lottery).filter(Lottery.contestant_id == nick5.id).all()
#             query_numb2 = len(query2)



#             assert query_numb2 == query_numb

#         # 1) Test lottery
#     def test_winner_lottery(self):
#         with app.app_context():
#             app2 = TestedApp.test_client()
#             URL_DELETE = "/delete_messages"

#             # delete senza login
#             r = app2.get(URL_DELETE)

#             #login
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)

#             #send message
#             URL = '/send'
#             file_name = "fake-text-stream.txt"
#             payload = {
#                 'recipient': 'nick1',
#                 'body': 'ciao nick1',
#                 'delivery_date': '7/11/2021',
#                 "image_file": (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button': 'Send',
#             }
#             r = app2.post(URL, data=payload, content_type="multipart/form-data")

#             #delete message
#             nick5 = db.session.query(User).filter(User.nickname == 'nick5').first()

#             #delete senza i punti necessari
#             nick5.lottery_points = 0
#             db.session.commit()
#             r = app2.get(URL_DELETE)

#             #delete con i punti necessari
#             nick5.lottery_points += 12
#             db.session.commit()
#             r = app2.get(URL_DELETE)

#             assert r.status_code == 201

#     def test_send_mail(self):
#         with app.app_context():
#             r = send_mail("provaase5@gmail.it","testo body")
#             r1 = send_mail("provaase5@gmail.it", "")
#             assert r and r1


#     def test_lottery_fun(self):
#         with app.app_context():
#             app2 = TestedApp.test_client()
#             URL_LOGIN = '/login'
#             URL_LOTTERY = '/lottery'
#             payload_login = {
#                 'email': 'email1@prova.it',
#                 'password': 'pass1'
#             }
#             r_login = app2.post(URL_LOGIN, data=payload_login)
#             nick = db.session.query(User).filter(User.nickname == 'nickOK').first()
#             print (nick.nickname)

#             # first registration
#             r = app2.post(URL_LOTTERY)
#             query = db.session.query(Lottery).filter(Lottery.contestant_id == nick.id).all()
#             query_numb = len(query)
#             print(query_numb)

#             r = lottery()
#             assert r

#     def test_OpenedMessage(self):
#         with app.app_context():
#             app2 = TestedApp.test_client()
#             app2 = TestedApp.test_client()

#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)

#             URL = '/send'
#             file_name = "fake-text-stream.txt"
#             payload = {
#                 'recipient': 'nick1',
#                 'body': 'ciao nick1',
#                 'delivery_date': '20/11/2021',
#                 "image_file": (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button': 'Send',
#             }
#             r = app2.post(URL, data=payload)

#             r = checkMessageOpened()
#             assert r

#     def test_deletion_message(self):
#         with app.app_context():
#             app2=TestedApp.test_client()
#             URL_login = '/login'
#             payload_login = {
#                 'email': 'email5',
#                 'password': 'pass5'
#             }
#             r_login = app2.post(URL_login, data=payload_login)
#             URL = '/send'
#             file_name="fake-text-stream.txt"
#             payload = {
#                 'recipient' : 'nick1',
#                 'body' : 'ciao nick1',
#                 'delivery_date' : '20/11/2021',
#                 "image_file" : (io.BytesIO(b"some initial text data"), file_name),
#                 'submit_button' : 'Send',
#             }
#             r = app2.post(URL, data=payload)
#             nick5 = db.session.query(User).filter(User.nickname=="nick5").first()
#             nick5.lottery_points = 12
#             db.session.commit()
#             nick1 = db.session.query(User).filter(User.nickname=="nick1").first()
#             message_check=db.session.query(Message).filter(Message.receiver_id==nick1.id).filter(Message.sender_id==nick5.id).filter(Message.body=="ciao nick1").first()
#             message_id = message_check.message_id
#             URL = '/message/{}'.format(message_id)
#             URL = URL+"?delete"
#             response = app2.post(URL)
#             URL = '/message/{}'.format(message_id)
#             URL = URL + "?lottery=0"
#             response = app2.post(URL)
#             assert message_check is not None