from flask import Flask
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, validators, ValidationError,validators, StringField,PasswordField,SubmitField,BooleanField,DateField,TextField,IntegerField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo

#from app.models import User

class RegisterForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField("Email", validators=[DataRequired(),Email()])
    pswd = PasswordField("Password", validators=[DataRequired()])
    cpswd = PasswordField("Confirm Password", validators=[DataRequired(),EqualTo('pswd')])
    submit = SubmitField("Sign Up")
    '''def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("username has been already taken!")'''


class ContactForm(FlaskForm):
  name = TextField("Name", [validators.Required("Please Enter Your Name")])
  email = TextField("Email",[validators.Required("Please enter your email address"), validators.email("Please enter your email address")])
  subject = TextField("Subject", [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message", [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")

class Login(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()])
    pswd = PasswordField("Password", validators=[DataRequired()])
    remember= BooleanField("Remember me")
    submit=SubmitField("Login")

class Showrem(FlaskForm):
    sdate = DateField('Select from Date : ',format="%m/%d/%Y")
    ldate = DateField('Select To Date : ',format="%m/%d/%Y")
    subject = SelectField('Subject :', choices = [('Office Work', 'office'),('House Hold works', 'Household'),('Bank Loan', 'Loan'),('Others', 'Not Listed')])
    submit=SubmitField("Filter")

class Modifyremd(FlaskForm):
    date = DateField('Date : ',format="%m/%d/%Y")
    submit=SubmitField("Filter")

class Modifyrems(FlaskForm):
     subject = SelectField('Subject :', choices = [('Office Work', 'office'),('House Hold works', 'Household'),('Bank Loan', 'Loan'),('Others', 'Not Listed')])
     submit=SubmitField("Filter")
class Modifyremn(FlaskForm):
    selectedname = TextField("Reminder Name",[validators.Required("Please enter subject.")])
    submit=SubmitField("Filter")

class IDform(FlaskForm):
    id = IntegerField("ID",validators=[DataRequired()])
    submit=SubmitField("Filter")


class Reminder(FlaskForm):
     date = DateField('Date',format="%m/%d/%Y",validators=[DataRequired()])
     name = TextField("Reminder Name",[validators.Required("Please enter subject.")])
     subject = SelectField('Subject :', choices = [('Office Work', 'office'),('House Hold works', 'Household'),('Bank Loan', 'Loan'),('Others', 'Not Listed')])
     discript= TextField('Discription',[validators.Required("Please enter subject.")])
     email =   StringField("Email", validators=[DataRequired(),Email()])
     contact=  IntegerField("Contact",validators=[DataRequired()])
     sms=     IntegerField("SMS",validators=[DataRequired()])
     id =  IntegerField("ID",validators=[DataRequired()])
     recur = SelectField('Recur', choices = [('1', '1'),
      ('2', '2'),('3', '3'),('4', '4')])
     submit = SubmitField("Create Reminder")
