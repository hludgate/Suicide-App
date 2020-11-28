from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    user_type = RadioField('Type of User',choices=[('Patient','Patient'),('Doctor','Doctor')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        #user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        #user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
feels = ['Very Good','Good','Neutral','Bad','Very Bad']

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    groups = SelectField(label='Group',choices=[(feel, feel) for feel in feels])
    thoughts = SelectField(label='thoughts',choices=[(feel, feel) for feel in feels])

class GetPatientForm(FlaskForm):
    #patients = User.query.filter_by(user_type='Patient').all()
    #patient_list = []
    #for patient in patients:
    #    patient_list.append((patient.username,patient.username))
    #patient_picked = SelectField(label='Patients',choices=patient_list)
    submit = SubmitField('Submit')
