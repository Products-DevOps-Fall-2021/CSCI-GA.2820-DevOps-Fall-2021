import os
from flask import Flask, render_template, url_for
from werkzeug.utils import redirect
from flask.globals import request
from service.products import ProductService
from service import app
from service import status
from flask_restx import Api

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Api-Key'
    }
}


api = Api(app,
          version='1.0.0',
          title='Product Demo REST API Service',
          description='This is a sample server Product store server.',
          default='products',
          default_label='Product shop operations',
          authorizations=authorizations,
         )

def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)

#root Home page
@app.route("/",  methods=['GET'])
def index():
    products = ProductService.index_page()
    return render_template('index.html', products = products)

@app.route("/products", methods=["GET"])
def list_all_products(): 
    app.logger.info("Request to list all products") 
    products = ProductService.get_all_products()
    return products , status.HTTP_200_OK

@app.route("/products/<int:id>", methods=["GET"])
def list_product(id):
    try:
        id = int(id)
    except ValueError:
        app.logger.info("Invalid Product ID.")
        abort(status.HTTP_400_BAD_REQUEST, "Invalid Product ID.")
    app.logger.info("Request to list a product with a given id") 
    product= ProductService.find_product_by_id(id)
    return product, status.HTTP_200_OK


@app.route("/products", methods=["POST"])
def create():
    app.logger.info("Request to Create product...")
    product_name = request.form['name']
    product_price = request.form['price']
    description = request.form['description']
    if product_name is None:
        abort(status.HTTP_417_EXPECTATION_FAILED, "Product name is required.")
    if product_price is None or product_price<=0:
        abort(status.HTTP_417_EXPECTATION_FAILED, "Product price is required.")
    output = ProductService.create_product(product_name, product_price, description)
    if output == True:
        return  redirect('/')

    return abort(status.HTTP_503_SERVICE_UNAVAILABLE, "Product could not be added in db")


@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    try:
        id = int(id)
    except ValueError:
        app.logger.info("Invalid Product ID.")
        api.abort(status.HTTP_400_BAD_REQUEST, "Invalid Product ID.")
    app.logger.info("Request to delete product...")
    output = ProductService.delete_product(id)
    if output == True:
        return  redirect('/')
    abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(id))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method=='POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        output = ProductService.update_product(id,name, price, description)
        if output == False:
            abort(status.HTTP_503_SERVICE_UNAVAILABLE, "Product could not be updated with id '{}' was not found.".format(id))
        else :
            return redirect('/')
    else:
        product = ProductService.find_product_by_id(id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(id))
        return render_template('update.html', product=product)