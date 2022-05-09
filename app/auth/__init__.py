import logging

from flask import Blueprint, render_template, redirect, url_for, flash, current_app, abort
from flask_login import login_user, login_required, logout_user, current_user
from jinja2 import TemplateNotFound
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from app.auth.decorators import admin_required
from app.auth.forms import login_form, register_form, profile_form, security_form, user_edit_form, create_user_form
from app.db import db
#from app.db.models import User, Location, location_user
from flask_mail import Message

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    form = register_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(email=form.email.data, password=generate_password_hash(form.password.data), is_admin=1)
            db.session.add(user)
            db.session.commit()
            if user.id == 1:
                user.is_admin = 1
                db.session.add(user)
                db.session.commit()

            msg = Message("Welcome to the site",
                          sender="from@example.com",
                          recipients=[user.email])
            msg.body = "Welcome to the site"

            #current_app.mail.send(msg)
            flash('Congratulations, you are now a registered user!', "success")

            return redirect(url_for('auth.login'), 302)

        else:
            flash('Already Registered')
            return redirect(url_for('auth.login'), 302)
    return render_template('register.html', form=form)
