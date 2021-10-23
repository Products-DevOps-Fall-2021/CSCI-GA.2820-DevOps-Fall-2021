import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import service.models as models


print("START APP")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #test.db = our database
try:
    models.init_db(app)
except Exception  :
    print('DB ERROR')

DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

print("start file run successfully......")

print('Setting up logging for {}...'.format(__name__))
# if __name__ != '__main__':
#     print("yash THESIA")
#     gunicorn_logger = logging.getLogger('gunicorn.error')
#     if gunicorn_logger:
#         app.logger.handlers = gunicorn_logger.handlers
#         app.logger.setLevel(gunicorn_logger.level)

app.logger.info('Logging established')
app.logger.info("**********************************************")
app.logger.info(" P R O D U C T   S E R V I C E   R U N N I N G")
app.logger.info("**********************************************")








import os
from flask import Flask, render_template, url_for
from werkzeug.utils import redirect
from flask.globals import request
from service.products import ProductService
# from . import app

@app.route("/",  methods=['GET'])
def index():
    print("starting index page")
    products = ProductService.index_page()
    print("completed index page")
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
def delete(id=1):
    app.logger.info("Request to delete product...")
    output = ProductService.delete_product(id)
    if output == True:
        return  redirect('/')
    return 'There was a problem deleting the product'


@app.route('/update/<int:id>', methods=["POST"])
def update(id):
    app.logger.info("Request to update product...")
    print("Request to update product...")
    name = request.form['name']
    price = request.form['price']
    output = ProductService.update_product(id,name, price)
    if output == True:
        return redirect('/')
    return 'There was a problem deleting the product'
