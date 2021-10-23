import os
from flask import Flask, render_template, url_for
from werkzeug.utils import redirect
from flask.globals import request
from service.products import ProductService
from service.start import app

@app.route("/",  methods=['GET'])
def index():
    products = ProductService.index_page()
    print("sumit")
    return render_template('index.html', products = products)

# @app.route("/products", methods=["GET"])
# def list_products():
#     app.logger.info("Request to list products...") 
#     return {}


@app.route("/products", methods=["POST"])
def create():
    app.logger.info("Request to Create product...")

    product_name = request.form['name']
    product_price = request.form['price']
    output = ProductService.create_product(product_name, product_price)
    if output == True:
        return  redirect('/')

    return "Issue adding product"


@app.route('/delete/<int:id>', methods=["DELETE"])
def delete(id):
    app.logger.info("Request to delete product...")
    output = ProductService.delete_product(id)
    if output == True:
        return  redirect('/')
    return 'There was a problem deleting the product'


@app.route('/update/<int:id>', methods=["PUT"])
def update(id):
    app.logger.info("Request to update product...")
    name = request.form['name']
    price = request.form['price']
    output = ProductService.update_product(id,name, price)
    if output == True:
        return redirect('/')
    return 'There was a problem deleting the product'
