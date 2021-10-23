import os
from flask import Flask, render_template, url_for
from werkzeug.utils import redirect
from flask.globals import request
from service.products import ProductService
from service import app

@app.route("/",  methods=['GET'])
def index():
    products = ProductService.index_page()
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


@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    app.logger.info("Request to delete product...")
    output = ProductService.delete_product(id)
    if output == True:
        return  redirect('/')
    return 'There was a problem deleting the product'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    product = ProductService.find_product_by_id(id)
    if request.method=='POST':
        name = request.form['name']
        price = request.form['price']
        output = ProductService.update_product(id,name, price)
        if output == True:
            return redirect('/')
        else :
            return 'Issue updating product'   
    else:
        return render_template('update.html', product=product)

    # print( id)
    # app.logger.info("Request to update product...")
    # print("Request to update product...")
    # name = request.form['name']
    # price = request.form['price']
    # print(name)
    # output = ProductService.update_product(id,name, price)
    # if output == True:
    #     return redirect('/')
    # else:
    #     return 'Issue updating product' 
