from flask_app import app
from flask import render_template, request, redirect
from flask_app.models.user_model import User


@app.route('/new_user', methods=['POST'])
def new_user():
    User.create_user(request.form)
    return redirect('/')


@app.route('/create_user')
def create_user():
    return render_template('create_user.html')


@app.route('/show_user/<int:user_id>')
def show_user(user_id):
    data = {
        "id" : user_id,
    }
    
    user=User.show_user(data)
    return render_template("show_user.html", user = user)


@app.route('/save_user/<int:user_id>', methods=['POST'])
def save_user(user_id):
    data = {
        "id" : user_id,
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
    }
    User.edit_user(data)
    return redirect('/')


@app.route('/edit_user/<int:user_id>')
def edit_user(user_id):
    data = {
        "id" : user_id,
    }
    user = User.show_user(data)
    return render_template("edit_user.html", user = user)


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):

    data = {
        "id" : user_id
    }
    User.delete_user(data)
    return redirect('/')


@app.route('/')
def index():
    users = User.get_all_users()
    return render_template('read_all.html', users = users)