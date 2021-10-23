from flask import Flask, render_template
from service.models import ProductModel
from . import app

class ProductService():

    def index_page():
        products = ProductModel.query.order_by(ProductModel.creation_date).all()
        print("sumit")
        return products

    
    def create_product(product_name, product_price):
        new_product = ProductModel(name = product_name, price = product_price)
        print("after new_product")
        try:
            ProductModel.save_to_db(new_product)
            return True   
        except Exception :
            return False

    def delete_product( id):
        product_to_delete = ProductModel.find_by_id(id)
        print("find deleted_product")
        try:
            ProductModel.delete_from_db(product_to_delete)
            print(" deleted")
            return True
        except Exception:
            return False

    def update_product(id, name , price):
        product_to_update = ProductModel.find_by_id(id)
        try:
            product_to_update.name = name
            product_to_update.price = price
            ProductModel.save_to_db(product_to_update)
            return True
        except Exception:
            return False
    
    def find_product_by_id(id):
        return ProductModel.find_by_id(id);
