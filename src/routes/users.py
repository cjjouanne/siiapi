from src import app, bcrypt, db, login_manager
from flask_login import login_user, current_user, logout_user
from flask import render_template, flash, redirect, url_for, request
from ..models.user import User
from ..forms.forms import RegistrationForm, LoginForm
from datetime import datetime

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('companies'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        now = datetime.now()
        apiKey = bcrypt.generate_password_hash(hashed_password+str(now)).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, apiKey=apiKey.replace('.','a').replace('/','z'), sessionType='user')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('users/register.html', title='Registro', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('companies'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('companies'))
        else:
            flash('Error al ingresar. Por favor revisa tu email y contrasena', 'danger')
    return render_template('users/login.html', title='Inicia Sesion', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))