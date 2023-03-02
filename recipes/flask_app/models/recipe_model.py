from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user_model import User

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30_min = data['under_30_min']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
    
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30_min, created_at, updated_at, users_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30_min)s, NOW(), NOW(), %(users_id)s);"
        results = connectToMySQL('recipes_db').query_db(query, data)
        return results

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s , date_made = %(date_made)s, under_30_min = %(under_30_min)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('recipes_db').query_db(query, data)
        
    
    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes_db').query_db(query, data)
        if not results:
            return False
        else:
            return cls(results[0])
    
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.users_id;"
        results = connectToMySQL('recipes_db').query_db(query)
        recipes = []
        for result in results:
            recipe = cls(result)
            user_data = {
                **result,
                'id' : result['users.id'],
                'created_at' : result['users.created_at'],
                'updated_at' : result['users.updated_at']
            }
            creator = User(user_data)
            recipe.creator = creator
            recipes.append(recipe)
        return recipes

    @classmethod
    def view_recipe(cls, data):
        query = "SELECT * FROM recipes JOIN users ON users.id = users_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipes_db').query_db(query, data)
        return cls(results[0])
        # recipes = []
        # for result in results:
        #     recipe = cls(result)
        #     user_data = {
        #         **result,
        #         'id' : result['users.id'],
        #         'created_at' : result['users.created_at'],
        #         'updated_at' : result['users.updated_at']
        #     }
        #     creator = User(user_data)
        #     recipe.creator = creator
        #     recipes.append(recipe)
        # return recipes
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes_db').query_db(query, data)
        return results

    @staticmethod
    def validate_recipe(data):
        is_Valid = True
        if len(data['name']) < 2:
            is_Valid = False
            flash ("Name field must be at least 2 characters")
        if len(data['description']) < 2:
            is_Valid = False
            flash ("Description field must be at least 2 characters")
        if len(data['instructions']) < 2:
            is_Valid = False
            flash ("Instructions field must be at least 2 characters")
        if len(data['date_made']) < 2:
            is_Valid = False
            flash ("Date made field must be at least 2 characters")
        return is_Valid

    
