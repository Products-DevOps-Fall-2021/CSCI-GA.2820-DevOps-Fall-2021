
from flask import Flask, render_template
from models import ProductModel



class ProductService():

    def index_page(self):
        products = ProductModel.query.order_by(ProductModel.creation_date).all()
        return products

    def create_product(self, product_name, product_price):
        new_product = ProductModel(content = product_name, price = product_price)
        try:
            ProductModel.save_to_db(new_product)
            return True   
        except Exception :
            return False

    def delete_product(self , id):
        product_to_delete = ProductModel.find_by_id(id)
        try:
            ProductModel.delete_from_db(product_to_delete)
            return True
        except Exception:
            return False

    def update_product(self, id, name , price):
        product_to_update = ProductModel.find_by_id(id)
        try:
            product_to_update.name = name
            product_to_update.price = price
            ProductModel.save_to_db(product_to_update)
            return True
        except Exception:
            return False
