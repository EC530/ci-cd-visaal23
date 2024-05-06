from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from authentication import auth_blueprint
# from userManagement import user_mgmt_blueprint

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb+srv://admin:admin@ec530.qevqtrc.mongodb.net/healthmonitoring?retryWrites=true&w=majority"
mongo = PyMongo(app)

# Register Blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')
# app.register_blueprint(user_mgmt_blueprint, url_prefix='/user_mgmt')

if __name__ == '__main__':
    app.run(debug=True)
