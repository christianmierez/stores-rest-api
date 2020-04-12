from flask_restful import Resource, reqparse
from models.store_model import StoreModel

class Store(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('name', 
        type=str,
        required=True,
        help="Every store needs a name.")
    
    def get(self, name):
        try:
            store = StoreModel.find_by_name(name)
        except:
            return {'message': 'An error ocurred searching for the store.'}, 500
        
        if store:
            return store.json()
        return {'message': 'Store not found.'}
    
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name: '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()    
        except:
            {'message': 'An error ocurred searching for the store.'}, 500

        return store.json(), 201
    
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store: 
            store.delete_from_db()
        
        return {'message': 'Store deleted successfully'}
    
class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}