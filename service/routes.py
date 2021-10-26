import os
from flask import Flask, render_template, url_for, make_response
from werkzeug.exceptions import BadRequest
from werkzeug.utils import redirect
from flask.globals import request
from service.error_handler import  request_validation_error
from service.products import ProductService
from service import app
from service import status
from flask import Flask, jsonify, request, url_for, make_response, abort, request
import json

#root Home page
@app.route("/",  methods=['GET'])
def index():
    return make_response(jsonify(name='Products REST API Service', version='1.0', 
                            url = url_for('list_all_products', _external=True)), status.HTTP_200_OK)


@app.route("/products", methods=["POST"])
def create():
    app.logger.info("Request to Create product...")
    check_content_type("application/json")
    record = json.loads(request.data)
    product_name = record['name']
    product_price = record['price']
    description = record['description']
    if product_name =="":
        return request_validation_error("Product name is required.")
    if product_price =="" or float(product_price)<0:
        return request_validation_error("Product price is required and cannot be less than zero.")
    output = ProductService.create_product(product_name, product_price, description)

    location_url = url_for("list_all_products", id=output['id'], _external=True)
    return make_response(
        jsonify(output), status.HTTP_201_CREATED, {'Location': location_url}
    )

@app.route("/products", methods=["GET"])
def list_all_products(): 
    app.logger.info("Request to list all products") 
    products = ProductService.get_all_products()
    return make_response(
        jsonify(products), status.HTTP_200_OK
    )

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )