from flask import Flask, render_template, url_for
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class ProductModel(db.Model):
    # __tablename__ = 'products'
    app = None
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
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
        print("enter to save to db")
        db.session.add(new_product)
        print("added not commited")
        db.session.commit()
        print(" commited")


    def delete_from_db(request_id):
        db.session.delete(request_id)
        db.session.commit()

    @classmethod        
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod        
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()


def init_db(app):
    ProductModel.init_db(app)