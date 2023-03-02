from flask_app.config.mysqlconnection import connectToMySQL
class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user.id']

    
    @classmethod
    def get_all(cls):
        query= "SELECT * FROM posts"
        results = connectToMySQL('my_first_full_stack_ex').query_db(query)

        posts = []
        for dict in results:
            posts = cls(dict)
            posts.append(posts)
        return posts