import unittest
from flask import Flask
from service.models import ProductModel
from service.products import ProductService
import service.models as models


class TestProductOperation(unittest.TestCase):
    def setUpClass():
        # establish db connection
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        models.init_db(app)
    
    def setUp(self):
        None
    def tearDown(self):
        None

    def test_create_product_success(self):
        test_product = ProductModel(name = "Demo", price = 35, description = "Description")
        self.assertNotEqual(test_product, None)
        self.assertEqual(test_product.name, "Demo")
        self.assertEqual(test_product.price, 35)
        self.assertEqual(test_product.description, "Description")
    
    
    def test_create_product_failure(self):
        self.assertRaises(TypeError, ProductModel(price = 35), True)
        self.assertRaises(TypeError, ProductModel(name = "Demo"), True)
        self.assertRaises(TypeError, ProductModel(), True)
        self.assertRaises(TypeError, ProductModel(price = "Demo"), True)
        self.assertRaises(TypeError, ProductModel(name = 35), True)

    #def test_delete_product_success(self):
    #    test_product = ProductModel(name = "Demo", price = 35)
    #    self.assertNotEqual(test_product, None)
    #    self.assertEqual(ProductModel.save_to_db(test_product), None)
    #    test_deleted = ProductModel.find_by_id(test_product.id)
    #    self.assertEqual(ProductModel.delete_from_db(test_deleted), None)

    def test_delete_product_failure(self):
        self.assertRaises(TypeError, ProductService.delete_product("Demo"), True)
        self.assertRaises(TypeError, ProductService.delete_product(35), True)

    #def test_update_product_success(self):
    #    self.assertEqual(ProductService.create_product("Demo", 35, "Description"), True)       
    #    new_demo_product = ProductModel.find_by_name("Demo")  
    #    self.assertNotEqual(new_demo_product, None)
    #    self.assertEqual(ProductService.update_product(id = new_demo_product.id , name = "Updated Demo" , price = 40, description = "Updated Description"), True)
    #    demo_deleted = ProductModel.find_by_name("Updated Demo")
    #    self.assertEqual(ProductModel.delete_from_db(demo_deleted), None)

    def test_update_product_failure(self):
        self.assertRaises(TypeError, ProductService.update_product("Demo", "Demo", "Demo","Demo"), True)
        self.assertRaises(TypeError, ProductService.update_product(35, 35, 35, 35), True)

if __name__ == '__main__':
    unittest.main()


        
        