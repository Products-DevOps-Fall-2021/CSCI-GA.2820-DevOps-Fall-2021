from flask import Flask, render_template, url_for
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from service.start import db

class ProductModel(db.Model):
    __tablename__ = 'products'
    app = None
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)#, nullable=False)
    price = db.Column(db.Float, nullable = False)

    def __init__(self, pid, pname, pdescription, pprice):
        self.id = pid
        self.name = pname
        self.description = pdescription
        self.price = pprice
        self.creation_date = str(datetime.now())

    def __repr__(self):
        return '<Task %r>' %self.id

    @staticmethod
    def init_db(app):
        ProductModel.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod        
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod        
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()