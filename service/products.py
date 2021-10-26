from flask import Flask
from service.models import ProductModel
from . import app
class ProductService():

    def index_page():
        products = ProductModel.query.order_by(ProductModel.creation_date).all()
        return products

    def create_product(product_name, product_price, product_description):
        new_product = ProductModel(name = product_name, price = product_price, description = product_description)
        ProductModel.save_to_db(new_product)
        return ProductModel.serialize(new_product)   
    
    def get_all_products():
        products = ProductModel.get_products()
        results = [ProductModel.serialize(product) for product in products]
        return results
    
    def find_product_by_id(id):
        product = ProductModel.find_by_id(id)
        if product is None:
            return None
        return ProductModel.serialize(product)

    