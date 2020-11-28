from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, GetPatientForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app.fhirHelper import fhirHelper 

@app.route('/')
@app.route('/index')
@login_required
def index():
    #fhObj = fhirHelper()
    #name = fhObj.getPatient()
    #posts = [
    #        {
    #            'author': {'username': name},
    #            'body': 'Beautiful day in Portland!'
    #        }
    #    ]
    #
    #return render_template("index.html", title='Home Page', posts=posts)
    next_page = url_for('user', username=current_user.username)
    return redirect(next_page)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = url_for('user', username=current_user.username)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, user_type = form.user_type.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>',methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.user_type == 'Patient':
        posts = [
            {'author': user, 'body': user.user_type},
            {'author': user, 'body': 'Test post #4'}
        ]
        return render_template('patient_portal.html', user=user, posts=posts)
    else:
        form = GetPatientForm()
        if form.validate_on_submit():

            return redirect(url_for('patient_info', patient=form.patient_picked.data))
        return render_template('doctor_portal.html', user=user, form=form)       

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.groups = form.groups.data
        current_user.thoughts = form.thoughts.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.thoughts.data = current_user.thoughts
        form.groups.data = current_user.groups
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/patient_info/<patient>',methods=['GET', 'POST'])
@login_required
def patient_info(patient):
    user = User.query.filter_by(username=patient).first_or_404()
    fhir_id = '09075876-bd10-46cf-9455-d55dc7df9f59'
    fhObj = fhirHelper(fhir_id)
    sad_sum = fhObj.getPatientGender()
    age = fhObj.getPatientAge()
    if age < 19 or age > 45:
        sad_sum += 1
    status = fhObj.getPatientMaritalStatus()
    if (status == 'L' or status == 'A' or status == 'D' or status == 'W'):
        sad_sum += 1
    if user.thoughts == 'Bad' or user.thoughts == 'Very Bad':
        sad_sum += 1
    if user.groups == 'Bad' or user.groups == 'Very Bad':
        sad_sum += 1    
    conditions = fhObj.getPatientConditions()
    con_list = ['depression','addict','alcohol','overdose','chronic']
    for con in conditions:
        for l in con_list:
            if con.find(l) >= 0:
                sad_sum += 1 
    if sad_sum < 5:
        risk = 'Low'
    elif sad_sum < 7:
        risk = 'Medium'
    else:
        risk = 'High'

    return render_template('patient_info.html',patient=patient, risk=sad_sum)