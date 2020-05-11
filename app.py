import os 

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db_sql import db_sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# changes the url to the authentication endpoint from /auto to /login
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.secret_key = 'Pulg@13!_'
api = Api(app)

@app.before_first_request
def create_tables():
    db_sql.create_all()

jwt = JWT(app, authenticate, identity) # creates /auth endpoint

# customize JWT auth response, include user_id in response body
@jwt.jwt_error_handler
def customized_error(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code,
    }), error.status_code

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

db_sql.init_app(app)

# prevents to run the app when app.py is imported from another file 
if __name__ == '__main__':
    app.run(port=5000, debug=True)
