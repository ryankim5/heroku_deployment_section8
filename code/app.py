from flask import Flask, request, jsonify
from flask_restful import Api, reqparse
from flask_jwt_extended import JWTManager, create_access_token

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from FlaskSQLAlchemy_SETUP import db # SQLAlchemy Import; Does NOT Cause Circular Import

app = Flask(__name__)

# APP SECRET KEY Settings (Configerations)
app.secret_key = "R2ya3adfasdfhcayud5rybwq23eir2692647uqwyecruiyq2345ewiou78cbyqou23elhdidEx2i7cute6VisualS2tud8io2CojXde3id2quncq9r838f8ec7q"
app.config["JWT_SECRET_KEY"] = app.secret_key

# SQLAlchemy Settings (Configerations)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# Create Flask-RESTful App API with Flask APP
api = Api(app)

jwt = JWTManager(app)  # /auth, POST

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/auth", methods=["POST"])
def auth():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not authenticate(username, password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")

api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
