from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import HTTPException
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://db:5432/pm?user=postgres"
app.config['SECRET_KEY'] = '87ddc7dc2ca2f007ee13dca6'


@app.errorhandler(HTTPException)
def handle_exception(error):
    response = jsonify(error=str(error))
    response.status_code = error.code
    return response


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
