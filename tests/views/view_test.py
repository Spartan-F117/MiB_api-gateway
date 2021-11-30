import unittest
from faker import Faker
from random import choice, randint


LOGIN_OK = 200
LOGIN_FAIL = 201
DOUBLE_LOGIN = 202


class ViewTest(unittest.TestCase):
    faker = Faker()

    BASE_URL = "http://localhost"

    @classmethod
    def setUpClass(cls):
        from mib import create_app
        cls.app = create_app()
        cls.client = cls.app.test_client()
        from mib.rao.user_manager import UserManager
        cls.user_manager = UserManager
    
#test login

#1) login
    def login_test_user(self):
        """
        Simulate the customer login for testing the views with @login_required
        :return: customer
        """
        URL = '/login'
        payload = {
                'email': 'email1@example.com',
                'password': 'pass1'
            }

        r = self.requests.post(
            self.BASE_URL+URL,
            json=payload
        )
        assert r.status_code == LOGIN_OK
    
# #2) wrong login
#     def test_wrong_login_user(self):
#         URL = '/login'
#         payload = {
#             'email': 'email1@example.com',
#             'password': 'pass1000'
#         }
#         r = self.requests.post(
#             self.BASE_URL+URL,
#             json=payload
#         )
#         assert r.status_code == LOGIN_FAIL

# #3) login when just login
#     def test_login_user_when_just_login(self):
#         URL = '/login'
#         payload = {
#             'email': 'email1@example.com',
#             'password': 'pass5'
#         }
#         r1 = self.requests.post(
#             self.BASE_URL+URL,
#             json=payload
#         )
#         r = self.client.post(
#             self.BASE_URL+URL,
#             json=payload
#         )
#         assert r.status_code == DOUBLE_LOGIN
    
    def generate_user(self):
        """Generates a random user, depending on the type
        Returns:
            (dict): a dictionary with the user's data
        """

        data = {
            'id': randint(0,999),
            'email': self.faker.email(),
            'password': self.faker.password(),
            'is_active' : choice([True,False]),
            'authenticated': False,
            'is_anonymous': False,
            'firstname': self.faker.first_name(),
            'lastname': self.faker.last_name(),
            'date_of_birth': self.faker.date()
        }
        return data
