from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://db:5432/pm?user=postgres"
app.config['SECRET_KEY'] = '87ddc7dc2ca2f007ee13dca6'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
