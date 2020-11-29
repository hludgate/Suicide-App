from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from app.fhirHelper import fhirHelper 
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    user_type = RadioField('Type of User',choices=[('Patient','Patient'),('Doctor','Doctor')])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
feels = ['Very Good','Good','Neutral','Bad','Very Bad']
oftens = ['Very Often','Often','Neutral','Not Often','Never']
class EditProfileForm(FlaskForm):
    groups = SelectField(label='Group',choices=[(feel, feel) for feel in feels])
    thoughts = SelectField(label='thoughts',choices=[(often, often) for often in oftens])
    submit = SubmitField('Submit')

class GetPatientForm(FlaskForm):
    patients = User.query.filter_by(user_type='Patient').all()
    patient_list = []
    for patient in patients:
        if patient.first_name is not None and patient.last_name is not None:
            patient_list.append((patient.username,patient.first_name + ' ' + patient.last_name))
    patient_picked = SelectField(label='Patients',choices=patient_list)
    submit = SubmitField('Submit')
