from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask import render_template, redirect, request, session, flash


@app.route('/dashboard')
def dashboard():
    if 'uid' not in session:
        flash("Must be logged in")
        return redirect('/')

    data = {
        'id' : session['uid']
    }
    logged_in_user = User.get_by_id(data)
    
    recipes = Recipe.get_all_recipes()
    return render_template('dashboard.html', recipes = recipes, user = logged_in_user)


@app.route('/new_recipe')
def create_recipe():
    if not 'uid' in session:
        return redirect('/')
    return render_template('create_recipe.html')


@app.route('/save_recipe', methods = ['POST'])
def save_recipe():
    print(request.form)
    data = {
        **request.form,
        'users_id' : session['uid']
    }
    if not Recipe.validate_recipe(request.form):
        return redirect('/new_recipe')
    Recipe.create_recipe(data)
    return redirect('/dashboard')


@app.route('/view_recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    if not 'uid' in session:
        return redirect('/')
    
    data = {
        'id' : recipe_id
    }
    recipes = Recipe.view_recipe(data)
    
    user_data = {
        'id' : session['uid']
    }
    logged_in_user = User.get_by_id(user_data)
    return render_template('view_recipe.html', recipes = recipes, user = logged_in_user)


@app.route('/edit_recipe/<int:recipe_id>')
def edit_recipe(recipe_id):
    if not 'uid' in session:
        flash("You must be logged in.")
        return redirect('/')
    data = {
        'id' : recipe_id,
    }
    recipe = Recipe.get_one_recipe(data)
    return render_template('edit_recipe.html', recipe = recipe)


@app.route('/save_update/<int:recipe_id>', methods = ['POST'])
def save_update(recipe_id):
    
    user_data = {
        'id' : recipe_id,
    }
    recipe = Recipe.get_one_recipe(user_data)
    if session['uid'] != recipe.users_id:
        return redirect('/dashboard')

    data = {
        **request.form,
        'id' : recipe_id
    }
    
    if not Recipe.validate_recipe(request.form):
        return redirect ('/dashboard')
    Recipe.update_recipe(data)
    return redirect('/dashboard')


@app.route('/delete_recipe/<int:recipe_id>')
def delete_recipe(recipe_id):
    data = {
        'id' : recipe_id
    }
    recipe = Recipe.get_one_recipe(data)
    if session['uid'] != recipe.users_id:
        return redirect('/dashboard')

    Recipe.delete_recipe(data)
    return redirect('/dashboard')