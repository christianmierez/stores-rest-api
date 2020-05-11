from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel

class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float,
        required=True,
        help="This field cannot be blank!"
    )
    parser.add_argument('store_id', 
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    '''
    GET request method definition 
    '''
    @jwt_required() 
    def get(self, name):
        try: 
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error ocurred searching for the item.'}, 500
        
        if item:
                return item.json()
        return {'message': 'Item not found'}, 404
    

    '''
    POST request method definition 
    '''
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 
        
        data = Item.parser.parse_args()            
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message':'An error ocurred inserting the item'}, 500

        return item.json(), 201 # http status code = CREATED
    
    '''
    DELETE request method definition 
    '''
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message': 'Item deleted'}
    
    '''
    PUT request method definition 
    '''
    def put(self, name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
            

        item.save_to_db()

        return item.json() 

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.find_all()]}
