from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class login_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),
    ])

    password = PasswordField('Password', [

        validators.DataRequired(),
        #checks min 6 characters, at least one uppercase letter, one lowercase letter and one number:
        validators.length(min=6, max=35)
    ])
    submit = SubmitField()


class register_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),
    ], description="You need to signup with an email")

    password = PasswordField('Create Password', [
        validators.DataRequired(),
        validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$", flags=0, message=None),
        validators.EqualTo('confirm', message='Passwords must match'),

    ], description="Create a password ")
    confirm = PasswordField('Repeat Password', description="Please retype your password to confirm it is correct")
    submit = SubmitField()

class create_user_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),

    ], description="You need to signup with an email")

    password = PasswordField('Create Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),

    ], description="Create a password ")
    confirm = PasswordField('Repeat Password', description="Please retype your password to confirm it is correct")
    is_admin = BooleanField('Admin', render_kw={'value':'1'})
    submit = SubmitField()


class profile_form(FlaskForm):
    about = TextAreaField('About', [validators.length(min=6, max=300)],
                          description="Please add information about yourself")

    submit = SubmitField()

class user_edit_form(FlaskForm):
    about = TextAreaField('About', [validators.length(min=6, max=300)],
description="Please add information about yourself")
    is_admin = BooleanField('Admin', render_kw={'value':'1'})
    submit = SubmitField()


class security_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),

    ], description="You can change your email address")

    password = PasswordField('Create Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),

    ], description="Create a password ")
    confirm = PasswordField('Repeat Password', description="Please retype your password to confirm it is correct")

    submit = SubmitField()

class csv_upload(FlaskForm):
    file = FileField()
    submit = SubmitField()