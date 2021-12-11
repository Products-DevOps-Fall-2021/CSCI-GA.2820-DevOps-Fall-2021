import os
from flask import Flask, render_template, url_for, make_response
from werkzeug.exceptions import BadRequest
from werkzeug.utils import redirect
from flask.globals import request
from service.error_handler import  bad_request, request_validation_error, not_found
from service.products import ProductService
from service.models import DataValidationError, ProductModel
from service import app
from service import status
from flask import Flask, jsonify, request, url_for, make_response, abort, request
import json
import logging
from flask import send_from_directory
from flask_restx import Api, Resource, fields, reqparse, inputs, apidoc
import service.models as models
import sys


######################################################################
# Configure the Root route before OpenAPI
######################################################################
@app.route("/")
def index():
    # return make_response(jsonify(name='Products REST API Service', version='1.0', url = url_for('list_all_products', _external=True)), status.HTTP_200_OK)
    root_dir = os.path.dirname(os.getcwd())
    print("*"*100, os.path.join(root_dir, 'service', 'static'))
    return render_template("index.html")


######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Product Demo REST API Service',
          description='This is a sample server Product store server.',
          default='products',
          doc='/apidocs', # default also could use doc='/apidocs/'
          prefix='/api'
         )


# Define the model so that the docs reflect what can be sent
# create model
create_model = api.model('CreateProduct', {
    'name': fields.String(required=True,
                        description='The name of the Product'),
    'price': fields.Float(required=True,
                        description='Price of the Product'),
    'description': fields.String(required=True,
                              description='The description of the Product'),
    
})

# product model
product_model = api.inherit(
    'ProductModel', 
    create_model,
    {
        'id': fields.Integer(readOnly=True,
                            description='The unique id assigned internally by service'),
        'like': fields.Integer(readOnly=False, 
                            description='Number of likes of a product'),
        'is_active': fields.Boolean(readOnly=True,
                            description='The product is active or not')
        
    }
) 

# query string arguments
product_args = reqparse.RequestParser()
product_args.add_argument('name', type=str, required=False, help='List Products by name')
product_args.add_argument('id', type=int, required=False, help='List Products by id')
product_args.add_argument('minimum', type=int, required=False, help='Minimum Price of the product')
product_args.add_argument('maximum', type=int, required=False, help='Maximum Price of the product')



######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST


######################################################################
#  PATH: /products
######################################################################
@api.route('/products', strict_slashes=False)
class ProductCollection(Resource):
    """ Handles all interactions with collections of Products """
    #------------------------------------------------------------------
    # LIST ALL PRODUCTS
    #------------------------------------------------------------------
    @api.doc('list_products')
    @api.expect(product_args, validate=True)
    @api.marshal_list_with(product_model)
    def get(self):
        """ Returns all of the Products """
        app.logger.info('Request to list Products...')
        args = product_args.parse_args()
        product_name = request.args.get("name")
        product_id = request.args.get("id")
        minimum_price = request.args.get("minimum")
        maximum_price = request.args.get("maximum")
        app.logger.info(type(product_id))
        products = []     
        if product_id:
            app.logger.info('Filtering by id: %s', product_id)
            product = ProductService.find_product_by_id(product_id)
            if not product:
                abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(product_id))
            return product, status.HTTP_200_OK
        elif product_name:
            app.logger.info('Filtering by name: %s', product_name)
            products = ProductService.find_product_by_name(product_name)
        elif minimum_price or maximum_price:
            app.logger.info("Request to list all products in the given range") 
            products = ProductService.query_by_price(minimum_price, maximum_price)
        else:
            app.logger.info('Returning unfiltered list.')
            products = ProductService.get_all_products()
        app.logger.info('[%s] Products returned', len(products))
        results = [product for product in products]
        return results, status.HTTP_200_OK

    #------------------------------------------------------------------
    # ADD A NEW PRODUCT  
    #------------------------------------------------------------------
    @api.doc('create_products')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(product_model, code=201)
    def post(self):
        """
        Creates a Product
        This endpoint will create a Product based the data in the body that is posted
        """
        app.logger.info('Request to Create a Product')
        record = json.loads(request.data)
        app.logger.info(record)
        if 'name' in record and 'price' in record and 'description' in record:
            product_name = record['name']
            product_price = record['price']
            description = record['description']
            output = ProductService.create_product(product_name, product_price, description)      
            app.logger.info(output)
            location_url = api.url_for(ProductResource, id=output['id'], _external=True)
            return output, status.HTTP_201_CREATED, {'Location': location_url}
        else:
            abort(status.HTTP_400_BAD_REQUEST, 
            "Provide name, price and description to add a new product.")
        


######################################################################
#  PATH: /products/{id}
######################################################################
@api.route('/products/<id>')
@api.param('id', 'The Product identifier')
class ProductResource(Resource):
    """
    ProductResource class
    Allows the manipulation of a single Product
    GET /Product{id} - Returns a Product with the id
    PUT /Product{id} - Update a Product with the id
    DELETE /Product{id} -  Deletes a Product with the id
    """

    #------------------------------------------------------------------
    # RETRIEVE A PRODUCT
    #------------------------------------------------------------------
    @api.doc('get_products')
    @api.response(404, 'Product not found')
    @api.marshal_with(product_model)
    def get(self, id):
        """
        Retrieve a single Product
        This endpoint will return a Product based on it's id
        """
        app.logger.info(type(id))
        app.logger.info("Request to Retrieve a product with id [%s]", id)
        product = ProductService.find_product_by_id(id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(id))
        return product, status.HTTP_200_OK


    #------------------------------------------------------------------
    # UPDATE AN EXISTING PRODUCT
    #------------------------------------------------------------------
    @api.doc('update_products')
    @api.response(404, 'Product not found')
    @api.response(400, 'The posted Product data was not valid')
    @api.expect(product_model)
    @api.marshal_with(product_model)
    def put(self, id):
        """
        Update a Product
        This endpoint will update a Product based the body that is posted
        """
        app.logger.info("Request to Update product...")
        product = ProductModel.find_by_id(id)
        if product:
            data = request.get_json()
            if 'name' in data:      
                product.name = data['name']
            if 'price' in data:
                product.price = data['price']
            if 'description' in data:
                product.description = data['description']
            ProductModel.save_to_db(product)
            return product, status.HTTP_200_OK
        else:
            abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(id))

        
    #------------------------------------------------------------------
    # DELETE A PRODUCT
    #------------------------------------------------------------------
    @api.doc('delete_products')
    @api.response(204, 'Product deleted')
    def delete(self, id):
        """
        Delete a Product
        This endpoint will delete a Product based the product_id specified in the path
        """
        app.logger.info("Request to delete product...")
        output = ProductService.delete_product(id)
        response_code = status.HTTP_204_NO_CONTENT
        app.logger.info('Product with id [%s] was deleted', id)
        return '', response_code


######################################################################
#  PATH: /products/{id}/like
######################################################################
@api.route('/products/<id>/like')
@api.param('id', 'The Product identifier')
class ProductLike(Resource):
    @api.doc('like_products')
    @api.response(404, 'Product not found')
    @api.marshal_with(product_model)
    def put(self, id):
        """
        Like the Product
        This endpoint increments the likes
        """
        app.logger.info("Request to increase product likes...")
        product = ProductModel.find_by_id(id)
        if product:
            product.like=product.like+1
            ProductModel.save_to_db(product)    
            response_code = status.HTTP_200_OK
            return product, response_code
        else:
            abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(id))


######################################################################
#  PATH: /products/{id}/dislike
######################################################################
@api.route('/products/<id>/dislike')
@api.param('id', 'The Product identifier')
class ProductDisLike(Resource):
    @api.doc('dislike_products')
    @api.response(404, 'Product not found')
    @api.marshal_with(product_model)
    def put(self, id):
        """
        Dislike the Product
        This endpoint decreases the likes
        """
        app.logger.info("Request to decrease product likes...")
        product = ProductModel.find_by_id(id)
        if product:
            product.like=product.like-1
            ProductModel.save_to_db(product)    
            response_code = status.HTTP_200_OK
            return product, response_code   
        else:
            abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(id))


######################################################################
#  PATH: /products/{id}/disable
######################################################################
@api.route('/products/<id>/disable')
@api.param('id', 'The Product identifier')
class ProductDisable(Resource):
    @api.doc('disable_products')
    @api.response(404, 'Product not found')
    @api.marshal_with(product_model)
    def put(self, id):
        """
        Disable the Product
        This endpoint disables the product
        """
        app.logger.info("Request to disable the product...")
        product = ProductModel.find_by_id(id)
        if product:
            output = ProductService.disable_product(id)
            response_code = status.HTTP_200_OK
            return output, response_code  
        else:
            abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(id))


######################################################################
#  PATH: /products/{id}/enable
######################################################################
@api.route('/products/<id>/enable')
@api.param('id', 'The Product identifier')
class ProductEnable(Resource):
    @api.doc('enable_products')
    @api.response(404, 'Product not found')
    @api.marshal_with(product_model)
    def put(self, id):
        """
        Enable the Product
        This endpoint enables the product
        """
        app.logger.info("Request to enable the product...")
        product = ProductService.find_product_by_id(id)
        if product:
            output = ProductService.enable_product(id)
            response_code = status.HTTP_200_OK
            return output, response_code
        else:
            abort(status.HTTP_404_NOT_FOUND, "Product with id '{}' was not found.".format(id))



######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

@app.before_first_request
def init_db(dbname="test"):
    """ Initlaize the model """
    try:
        models.init_db(app)
    except Exception  as error:
        app.logger.critical("%s: Cannot continue", error)
        # gunicorn requires exit code 4 to stop spawning workers when they die
        sys.exit(4)

def check_content_type(content_type):
    """ Checks whether the request content type is correct """  
    if request.headers['Content-Type'] != content_type:
        app.logger.error(
            'Invalid Content-Type: %s',
            request.headers['Content-Type'])
        abort(415, 'Content-Type must be {}'.format(content_type))


#pending 
# error handling - this file and test file
# execute nosetests
# UI not working  
# messages, 404 and other text updates
# check dislike, enable and disable
