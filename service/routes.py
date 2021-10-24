import os
from flask import Flask, render_template, url_for
from werkzeug.utils import redirect
from flask.globals import request
from service.error_handler import internal_server_error, not_found, request_validation_error
from service.products import ProductService
from service import app
from service import status

#root Home page
@app.route("/",  methods=['GET'])
def index():
    products = ProductService.index_page()
    return render_template('index.html', products = products)

@app.route("/products", methods=["GET"])
def list_all_products(): 
    app.logger.info("Request to list all products") 
    products = ProductService.get_all_products()
    print(products)
    return products

@app.route("/products/<int:id>", methods=["GET"])
def list_product(id):
    try:
        id = int(id)
    except ValueError:
        app.logger.info("Invalid Product ID.")
        return request_validation_error("Invalid Product ID.")
    app.logger.info("Request to list a product with a given id") 
    product= ProductService.find_product_by_id(id)
    if product==False:
        return not_found("Product Id not found from database")
    return product, status.HTTP_200_OK


@app.route("/products", methods=["POST"])
def create():
    app.logger.info("Request to Create product...")
    product_name = request.form['name']
    product_price = request.form['price']
    description = request.form['description']
    if product_name =="":
        return request_validation_error("Product name is required.")
    if product_price =="" or float(product_price)<0:
        return request_validation_error("Product price is required and cannot be less than zero.")
    output = ProductService.create_product(product_name, product_price, description)
    if output == True:
        return  redirect('/')

    return internal_server_error("Product Cannot be added in db due to internal server error")


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        id = int(id)
    except ValueError:
        app.logger.info("Invalid Product ID.")
        return request_validation_error("Invalid Product ID.")
    app.logger.info("Request to delete product...")
    output = ProductService.delete_product(id)
    if output == True:
        return  redirect('/')
    
    return internal_server_error("Product not found in DB")


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    if request.method=='POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        if price !="" and float(price)<0:
            return request_validation_error("Product price cannot be less than zero.")
        output = ProductService.update_product(id,name, price, description)
        if output == False:
            return not_found("Product Id not found from database which needs to update")
        else :
            return redirect('/')
    else:
        product = ProductService.find_product_by_id(id)
        if not product:
            return not_found("Product Id not found from database which needs to update")
        return render_template('update.html', product=product)