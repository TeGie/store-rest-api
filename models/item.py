from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')  
      
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name_and_store_id(cls, name, store_id):
        return cls.query.filter_by(name=name).filter_by(store_id=store_id).first()

    def json(self):
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}
