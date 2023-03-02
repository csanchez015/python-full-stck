from flask_app import app

import flask_app.controllers.user_controller
import flask_app.controllers.posts_controller

if __name__=="__main__":
    app.run(debug=True)
