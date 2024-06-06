from app import app
from flask_jwt_extended import JWTManager

jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)
