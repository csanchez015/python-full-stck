from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.user_model import User

@app.route('/')
def index():
    users = User.get_all_users()

    return render_template("index.html", users = users)
    

@app.route('/new_user')
def new_user():
    
    return render_template("new_user.html")


@app.route('/create_user', methods = ['POST'])
def create_user():
    
    User.create(request.form)
    return redirect('/')