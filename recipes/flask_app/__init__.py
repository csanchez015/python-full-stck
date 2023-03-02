from flask import Flask
app = Flask(__name__)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

app.secret_key = "Shhhhh this is the secret key shh!"