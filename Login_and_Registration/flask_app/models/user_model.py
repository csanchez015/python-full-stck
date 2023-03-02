from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL('login_and_registration').query_db(query, data)
        return results
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('login_and_registration').query_db(query, data)
        if not results :
            return False
        else:
            return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('login_and_registration').query_db(query, data)
        if not results:
            return False
        else:
            return cls(results[0])
    
    @staticmethod
    def validate_user(data):
        is_Valid = True
        if len(data['first_name']) < 3:
            is_Valid = False
            flash("First name must be at least 3 characters.")
        if len(data['last_name']) < 3:
            is_Valid = False
            flash("Last name must be at least 3 characters.")
        if User.get_by_email(data):
            is_Valid = False
            flash("Email already taken.")
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.")
            is_Valid = False
        if len(data['password']) < 8:
            is_Valid = False
            flash("Password must be at least 8 characters.")
        if data['confirm_password'] != data['password']:
            is_Valid = False
            flash("Passwords don't match.")
        return is_Valid
    
    @staticmethod
    def validate_login(data):
        is_Valid = True
        found_user = User.get_by_email(data)
        if found_user:
            if not bcrypt.check_password_hash(found_user.password, data['password']):
                is_Valid = False
        else:
            is_Valid = False
        if not is_Valid:
            flash("Invalid login.")
        return is_Valid
