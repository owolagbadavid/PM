from app import app, db
from auth.auth_routes import auth_routes
from users.user_routes import user_routes
from db.models import *
from flask_migrate import Migrate

migrate = Migrate(app, db)

# Register the auth_routes Blueprint with the app
app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(user_routes, url_prefix='/api/users')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
