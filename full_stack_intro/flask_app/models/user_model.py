from flask_app.config.mysqlconnection import connectToMySQL
class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.age = data["age"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users ORDER BY age DESC;"
        results = connectToMySQL('my_first_full_stack_ex').query_db(query)

        users = []
        for dict in results:
            user = cls(dict)
            users.append(user)

        return users

    
    @classmethod 
    def create(cls, data):

        query = "INSERT INTO users (first_name, last_name, age) VALUES(%(first_name)s, %(last_name)s, %(age)s)"
        results = connectToMySQL('my_first_full_stack_ex').query_db(query, data)
        
        return results