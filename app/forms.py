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

    patient_picked = SelectField(label='Patients',choices=[])
    submit = SubmitField('Submit')
    def __init__(self, patient_list: list = None, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.patient_list=patient_list
        self.patient_picked.choices = self._mongo_mock()
    def _mongo_mock(self) -> list:
        return [self.patient_list[i] for i in range(len(self.patient_list))]