from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash

from flask_app.models.user_model import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods = ['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    
    found_user = User.get_by_email(request.form)
    session['uid'] = found_user.id
    return redirect('/dashboard')


@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password' : hash
    }
    session['uid'] = User.register_user(data)
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/dashboard')
def dashboard():
    if not 'uid' in session:
        flash("You must be logged in.")
        return redirect('/')
    
    return render_template('registration.html')