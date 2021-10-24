from re import template
import unittest
from flask import Flask
from service.models import ProductModel, init_db
from service.products import ProductService
import service.models as models
import os 


class TestProductOperation(unittest.TestCase):
    def setUpClass():
        # establish db connection
        app = Flask(__name__)
        test_app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        models.init_db(app)
        
    def setUp(self):
        None
    def tearDown(self):
        None

    def test_get_api_success(self):
        None

if __name__ == '__main__':
    unittest.main()