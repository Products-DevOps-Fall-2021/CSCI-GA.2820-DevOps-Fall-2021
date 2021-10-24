import os
from flask import Flask, render_template, url_for
from werkzeug.utils import redirect
from flask.globals import request
from service.products import ProductService
from service import app

#root Home page
@app.route("/",  methods=['GET'])
def index():
    products = ProductService.index_page()
    return render_template('index.html', products = products)

# @app.route("/products", methods=["GET"])
# def list_all_products(): 
#     app.logger.info("Request to list all products") 
#     products = ProductService.get_all_products()
#     return products

# @app.route("/products/<int:id>", methods=["GET"])
# def list_product(id):
#     app.logger.info("Request to list a product with a given id") 
#     product= ProductService.find_product_by_id(id)
#     return product


@app.route("/products", methods=["POST"])
def create():
    app.logger.info("Request to Create product...")
    product_name = request.form['name']
    product_price = request.form['price']
    description = request.form['description']
    output = ProductService.create_product(product_name, product_price, description)
    if output == True:
        return  redirect('/')

    return "Issue adding product"


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    app.logger.info("Request to delete product...")
    output = ProductService.delete_product(id)
    if output == True:
        return  redirect('/')
    return 'There was a problem deleting the product'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    if request.method=='POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        output = ProductService.update_product(id,name, price, description)
        if output == False:
            return 'Issue in updating product' 
        else :
            return redirect('/')
    else:
        product = ProductService.find_product_by_id(id)
        return render_template('update.html', product=product)