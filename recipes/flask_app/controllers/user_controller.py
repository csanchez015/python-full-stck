from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash

from flask_app.models.user_model import User

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods =['POST'])
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


@app.route('/login', methods = ['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    
    user = User.get_by_email(request.form)
    session['uid'] = user.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



