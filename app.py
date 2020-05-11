import os 

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db_sql import db_sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'Pulg@13!_'
api = Api(app)

@app.before_first_request
def create_tables():
    db_sql.create_all()

jwt = JWTManager(app) # creates /auth endpoint

@jwt.user_claims_loader
def add_claims_to_jwt(identity): 
        if identity == 1:   # instead of hard-coding, we should read from a config file or database to get a list of admins instead
            return {'is_admin': True}
        return {'is_admin': False}

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

db_sql.init_app(app)

# prevents to run the app when app.py is imported from another file 
if __name__ == '__main__':
    app.run(port=5000, debug=True)
