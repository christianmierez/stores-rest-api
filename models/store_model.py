from db_sql import db_sql

class StoreModel(db_sql.Model):
    __tablename__ = 'stores'

    id = db_sql.Column(db_sql.Integer, primary_key=True)
    name = db_sql.Column(db_sql.String(80))
    
    items = db_sql.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name, 
            'items': [item.json() for item in self.items.all()]}


    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
            return cls.query.all()

    def save_to_db(self):
        db_sql.session.add(self)
        db_sql.session.commit()
    
    def delete_from_db(self):
        db_sql.session.delete(self)
        db_sql.session.commit()