from db_sql import db_sql

class ItemModel(db_sql.Model):
    __tablename__ = 'items'

    id = db_sql.Column(db_sql.Integer, primary_key=True)
    name = db_sql.Column(db_sql.String(80))
    price = db_sql.Column(db_sql.Float(precision=2))

    store_id = db_sql.Column(db_sql.Integer, db_sql.ForeignKey('stores.id'))
    store = db_sql.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self):
        return {'name': self.name, 'price': self.price}


    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db_sql.session.add(self)
        db_sql.session.commit()
    
    def delete_from_db(self):
        db_sql.session.delete(self)
        db_sql.session.commit()