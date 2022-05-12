"""This test the homepage"""
import pytest
from app.db import db
from app.db.models import User

#password that is invalid for login
def test_invalid_password_login(client, application):
   response = client.get("/login")
   response = client.post("/login",data={'email': '123@gmail.com', 'password': '123456rer2r2r'})
   data = {'username': '123456@qq.com', 'password': '12345678'}
   #print get_id(client)
   #user = client.query.get(user_id)
   #current_user = client.get_user()


#Bad username/email  (login)
def test_invalid_username_login(client, application):
   response = client.get("/login")
   data = {'email': '1234@gmail.com', 'password': '123456'}
   response = application.test_client().post('/login', data=data)
   #look for message Invalid username or password

#Already Registered (Registration)
def test_already_registered(client, application):
    #insert data
   data = {'email': '123@gmail.com', 'password': '123456', 'confirm': '123456'}
   application.test_client().post('/register', data=data)
   #check for 'already registered' message
   data = {'email': '123@gmail.com', 'password': '123456', 'confirm': '123456'}
   response = application.test_client().post('/register', data=data)


#Sucessful Login
def test_login(client, application):
    response = client.get("/login")
    data = {'email': '123@gmail.com', 'password': '123456'}
    response = application.test_client().post('/login', data=data)
     #look for message 'Welcome success'
    if b'a href="/dashboard">/dashboard</a>' in response.data:
        response = client.get("/dashboard")
        print('successful login')
    else:
        print('unsuccessful login')

def test_successful_registration(client, application):
    response = client.get("/register")
    data = {'email': '87889@gmail.com', 'password': '123456', 'confirm': '123456'}
    response = application.test_client().post('/register', data=data)
    print(response.data)
    #client.post('/users/<int:user_id>/delete')

#Password Confirmation (registration)
def test_pass_confirmation_registration(client, application):
    response = client.get("/register")
    data = {'email': 'new@gmail.com', 'password': '123456', 'confirm': '1236'}
    response = application.test_client().post('/register', data=data)
    if b'Passwords must match' in response.data:
        print("Passwords must match")

# Code for regular expression from https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
import re
#Bad username / email (Registration)
def test_bad_username_register(client, application):
   response = client.get("/register")
   data = {'email': '3@com', 'password': '123456', 'confirm': '123456'}
   regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
   email = data['email']
   if(re.fullmatch(regex, email)):
       print("Valid Email")
       response = application.test_client().post('/register', data=data)
   else:
       print("Invalid Email")

#Invalid password criteria
def test_invalid_password_register(client, application):
   response = client.get("/register")
   data = {'email': '4@gmail.com', 'password': '123', 'confirm': '123'}
   password = data['password']
   if(len(password) >= 6 and len(password) < 35):
       print("Valid Password")
       response = application.test_client().post('/register', data=data)
   else:
       print("Invalid Password")


def test_deny_dash(client, application):
#denying access to the dashboard for not logged in users
   response = client.get("/login")
   response = application.test_client().post('/login', data={'email': 'm', 'password': '123', 'confirm': '123'})
   if b'a href="/dashboard">/dashboard</a>' in response.data:
       response = client.get("/dashboard")
       print('allowing access to the dashboard for logged in users')
   else:
        print('denying access to the dashboard for logged in users')

#allowing access to the dashboard for logged in users
def test_allow_dash(client, application):
   response = client.get("/login")
   response = application.test_client().post('/login', data={'email': '123@gmail.com', 'password': '123456', 'confirm': '123456'})
   if b'a href="/dashboard">/dashboard</a>' in response.data:
       response = client.get("/dashboard")
       print('allowing access to the dashboard for logged in users')
   else:
       print('denying access to the dashboard for logged in users')