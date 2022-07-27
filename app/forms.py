from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Email, Optional
from flask_wtf.file import FileRequired, FileField
from .helpers import CountrySelectField




class UserSignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()


class UserSignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    artist = SelectField('Are you a Tattoo Artist?', choices=['Yes', "No"])
    submit_button = SubmitField()


class ArtistRegistryForm(FlaskForm):
    image = FileField('Image File', validators=[FileRequired()])
    # once this form is instatiated, instance.image will hold file value
    description = TextAreaField('Choose one art piece to be displayed on the website')
    nickname = StringField('Nickname', validators=[DataRequired()])
    social = StringField('Instagram', validators=[DataRequired()])
    email = StringField('Business Email', validators=[DataRequired(), Email()])
    country = CountrySelectField()
    category = SelectField('Which art style is your specialty?', choices=['Traditional', 'Japanese', 'Realism', 'Surrealism', 'Abstract', 'Minimalism', 'Blackwork', 'Geometric'])
    submit_button = SubmitField()


class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField(validators=[DataRequired()])
    send_message = SubmitField()

# Create a Favorites Form which holds a button that instantiates a favorite

class FavoriteButton(FlaskForm):
    add_artist = RadioField(coerce=bool, choices=[(True, 'yes'), (False,'no')])
    submit_button = SubmitField(label="")

class AcceptPending(FlaskForm):
    image = StringField('Image', validators=[Optional()])
    nickname = StringField('Nickname', validators=[Optional()])
    social = StringField('Social', validators=[Optional()])
    email = StringField('Email', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])
    category = StringField('Category', validators=[Optional()])
    user_id = StringField('User ID', validators=[Optional()])
    submit = SubmitField()

class DeletePending(FlaskForm):
    pending_id = StringField('Pending User ID', validators=[Optional()])
    submit = SubmitField()


    