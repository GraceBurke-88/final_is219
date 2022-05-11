from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class song_edit_form(FlaskForm):
#add back validator
    title = TextAreaField('Title',
    description = "Please add info about song title")
    #is_admin = BooleanField('Admin', render kw={'value':'1'})
    submit = SubmitField()

class csv_upload(FlaskForm):
    file = FileField()
    submit = SubmitField()
