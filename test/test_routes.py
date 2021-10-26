import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import logging
import unittest
from datetime import date, datetime

from urllib.parse import quote_plus
from service import status  # HTTP Status Codes
from service.models import db, ProductModel
from service.routes import app
from product_cart import ProductFactory


logging.disable(logging.CRITICAL)
BASE_URL = "/products"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestProductServer(unittest.TestCase):
    """Product Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.logger.setLevel(logging.CRITICAL)
        ProductModel.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.app = app.test_client()
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        """Test the Home Page"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def _create_products(self, count):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            resp = self.app.post(
                BASE_URL, 
                json=test_product.serialize(), 
                content_type=CONTENT_TYPE_JSON,
                
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test product"
            )
            new_product = resp.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products


    def test_get_product_list(self):
        """Get a list of Products"""
        self._create_products(5)
        resp = self.app.get( BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)
        resp = self.app.get("/products/yash", content_type=BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product(self):
        """Get a single Product"""
        # get the id of a product
        test_product = self._create_products(1)[0]
        resp = self.app.get(
            "/products/{}".format(test_product.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_get_product_not_found(self):
        """Get a Product thats not found"""
        resp = self.app.get("/products/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        """Create a new Product"""
        test_product = ProductFactory()
        logging.debug(test_product)
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,       
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_product = resp.get_json()
        

        self.assertEqual(new_product["name"], test_product.name, "Names do not match")
        self.assertEqual(
            new_product["description"], test_product.description, "Descripton does not match"
        )
       
        self.assertEqual(
            new_product["price"], test_product.price, "Price does not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        print('*->'*100, resp.status_code, location)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_product = resp.get_json()
        print('N->'*100,new_product )
        self.assertEqual(new_product[0]["name"], test_product.name, "Names do not match")
        self.assertEqual(
            new_product[0]["description"], test_product.description, "Descripton does not match"
        )
        self.assertEqual(
            new_product[0]["price"], test_product.price, "Price does not match"
        )

        test_product.name= ""
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        test_product.name = 'Demo'
        test_product.price= -100
        resp = self.app.post(
            BASE_URL, 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON,
            
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


if __name__ =='__main__':
    unittest.main()