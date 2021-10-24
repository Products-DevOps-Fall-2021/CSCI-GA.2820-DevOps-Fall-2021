from flask import Flask, render_template, url_for
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import InvalidRequestError

db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class ProductModel(db.Model):
    app = None
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)#, nullable=False)
    price = db.Column(db.Float, nullable = False)

    def __repr__(self):
        return '<Task %r>' %self.id

    @staticmethod
    def init_db(app):
        ProductModel.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  

    def save_to_db(new_product):
        try:
            db.session.add(new_product)
            db.session.commit()
        except InvalidRequestError:
            db.session.rollback()


    def delete_from_db(request_id):
        db.session.delete(request_id)
        try:
            db.session.commit()
        except InvalidRequestError:
            db.session.rollback()

    def get_products():
        return ProductModel.query.order_by(ProductModel.creation_date).all()

    @classmethod        
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod        
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    def serialize(self):
        """ Serializes a Product into a dictionary """
        return {
            "id": self.id, 
            "name": self.name,
            "description": self.description,
            "creation_date": self.creation_date,
            "price": self.price
        }

    def deserialize(self, data):
        """
        Deserialize a Product from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        self.name = data["name"]
        self.description = data["description"]
        self.price = data["price"]
        self.id = data["id"]
        self.creation_date = data["creation_date"]

        return self

def init_db(app):
    ProductModel.init_db(app)