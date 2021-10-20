
from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

redis_cache = FlaskRedis()
db = SQLAlchemy()
ma = Marshmallow()

class ProductModel(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    price = db.Column(db.Float, nullable = False)

    def __init__(self, name, description, creation_date, price):
        self.name = name
        self.description = description
        self.creation_date = creation_date
        self.price = price

class ProductSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    description = fields.String()
    creation_date = fields.DateTime()
    price = fields.Float()