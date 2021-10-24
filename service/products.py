from flask import Flask, render_template
from service.models import ProductModel
from service.error_handler import not_found, request_validation_error
from . import app
class ProductService():

    def index_page():
        products = ProductModel.query.order_by(ProductModel.creation_date).all()
        return products

    def get_all_products():
        products = ProductModel.get_products()
        results = [ProductModel.serialize(product) for product in products]
        return str(results)
    
    def create_product(product_name, product_price, pdescription):
        new_product = ProductModel(name = product_name, price = product_price, description = pdescription)
        try:
            new_product = ProductModel(name = product_name, price = product_price)
            ProductModel.save_to_db(new_product)
            return True   
        except Exception:
            return False

    def delete_product( id):
        product_to_delete = ProductModel.find_by_id(id)
        try:
            product_to_delete = ProductModel.find_by_id(id)
            ProductModel.delete_from_db(product_to_delete)
            return True
        except Exception:
            return False

    def update_product(id, name , price, description):
        product_to_update = ProductModel.find_by_id(id)
        try:
            if name != "":
                product_to_update.name = name
            if price !="" and float(price)>=0:
                product_to_update.price = price
            if description!="":
                product_to_update.description = description
            
            ProductModel.save_to_db(product_to_update)
            return product_to_update
        except Exception:
            return False
    
    def find_product_by_id(id):
        product = ProductModel.find_by_id(id)
        if product is None:
            return False
        return ProductModel.serialize(product)
