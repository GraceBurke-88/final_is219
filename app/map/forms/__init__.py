from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class location_edit_form(FlaskForm):
#add back validator
    population = TextAreaField('Population',
    description = "Please add info about location population")
    #is_admin = BooleanField('Admin', render kw={'value':'1'})
    submit = SubmitField()

class csv_upload(FlaskForm):
    file = FileField()
    submit = SubmitField()

class create_location_form(FlaskForm):
    title = TextAreaField('Location Name', [
        validators.DataRequired(),
    ], description="Add a location")
    longitude = TextAreaField('Longitude', [
        validators.DataRequired(),
    ], description="Add a longitude")
    latitude = TextAreaField('Latitude', [
         validators.DataRequired(),
    ], description="Add a latitude")
    population = TextAreaField('Population', [
             validators.DataRequired(),
        ], description="Add a population")

    #is_admin = BooleanField('Admin', render_kw={'value':'1'})
    submit = SubmitField()