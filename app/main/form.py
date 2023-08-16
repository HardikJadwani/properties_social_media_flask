from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Length

from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(('Username'), validators=[DataRequired()])
    about_me = TextAreaField(('About me'),
                             validators=[Length(min=0, max=140)])
    contact  = StringField('Contact Details', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
            
class EditPropertyForm(FlaskForm):
    details = TextAreaField(('Add property details'), validators=[DataRequired()])
    location= TextAreaField(('Add location details'), validators=[DataRequired()])
    square_feet=IntegerField(('Add area in square feets'),validators=[DataRequired()])
    basement = BooleanField('Basement')
    terrace = BooleanField('Terrace')
    garden = BooleanField('Garden')
    balcony = BooleanField('Balcony')
    submit = SubmitField('Submit')



class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PropertyForm(FlaskForm):
    details = TextAreaField(('Add property details'), validators=[DataRequired()])
    location= TextAreaField(('Add location details'), validators=[DataRequired()])
    square_feet=IntegerField(('Add area in square feets'),validators=[DataRequired()])
    basement = BooleanField('Basement')
    terrace = BooleanField('Terrace')
    garden = BooleanField('Garden')
    balcony = BooleanField('Balcony')
    submit = SubmitField('Submit')