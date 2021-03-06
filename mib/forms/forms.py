import wtforms as f
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from datetime import date


# Contains fields for the login form
class LoginForm(FlaskForm):
    email = f.StringField('email', validators=[DataRequired()], render_kw={"placeholder": "email"})
    password = f.PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    display = ['email', 'password']

# Contains fields for the registration (create user) form
class UserForm(FlaskForm):
    email = f.StringField('e-mail', validators=[DataRequired()], render_kw={"placeholder": "email"})
    firstname = f.StringField('Firstname', validators=[DataRequired()], render_kw={"placeholder": "Firstname"})
    lastname = f.StringField('Lastname', validators=[DataRequired()], render_kw={"placeholder": "Lastname"})
    password = f.PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    date_of_birth = f.DateField('Date of birth', format='%d/%m/%Y', render_kw={"placeholder": "DD/MM/YYYY"})
    nickname = f.StringField('Nickname', validators=[DataRequired()], render_kw={"placeholder": "Nickname"})
    location = f.StringField('Location', validators=[DataRequired()], render_kw={"placeholder": "Location"})
    display = ['email', 'firstname', 'lastname', 'password', 'date_of_birth','nickname','location']

    # Checks if data_of_birth is left blank or is invalide date return false, else result
    # def validate_on_submit(self):
    #     result = super(UserForm, self).validate()
    #     print(str(self.date_of_birth.data)+"data")
    #     if (self.date_of_birth.data is not None and self.date_of_birth.data>date.today()):
    #         return False
    #     else:
    #         return result

# Contains fields for the "send message" service
class SendForm(FlaskForm):
    recipient = f.SelectMultipleField('Recipient', validators=[DataRequired()])
    body = f.TextAreaField('Message', render_kw={"placeholder": "Message goes here", 'class': 'form-control', 'rows': 5}, validators=[DataRequired()])
    delivery_date = f.DateField('Delivery date', format='%d/%m/%Y', render_kw={"placeholder": "DD/MM/YYYY"})
    send_button = f.SubmitField('send')
    draft_button = f.SubmitField('save as draft')
    display = ['body', 'delivery_date']