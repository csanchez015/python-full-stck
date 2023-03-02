from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.user_model import User
from flask_app.models.posts_model import Post

@app.route('/new_post')
def new_post():
    users = User.get_all_users()
    return render_template('new_post.html')


@app.route('/posts')
def posts():
    
    post = Post.get_all()

    return render_template('all_posts.html')