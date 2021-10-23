from flask import Flask, render_template, url_for
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from . import db
# from werkzeug.utils import redirect
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #test.db = our database
# db = SQLAlchemy(app)


class ProductModel(db.Model):
    __tablename__ = 'products'
    app = None
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)#, nullable=False)
    price = db.Column(db.Float, nullable = False)

    def __init__(self, pid, pname, pdescription, pprice):
        self.id = pid
        self.name = pname
        self.description = pdescription
        self.price = pprice
        self.creation_date = str(datetime.now())

    def __repr__(self):
        return '<Task %r>' %self.id

# with app.app_context():
#     db.create_all()

# @app.route('/', methods=['POST', 'GET'])

    @staticmethod
    def init_db(app):
        ProductModel.logger.info('Initializing database')
        ProductModel.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod        
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod        
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    # @staticmethod
    # def all():
    #     ProductModel.logger.info('Processing all Products')
    #     return ProductModel.query.all()




# def index():
#     if request.method=="POST":
        
#         product_name = request.form['content']
#         product_price = request.form['price']
#         new_product = Specification(content = product_name, price = product_price)

#         try:
#             db.session.add(new_product)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'Issue adding product'
    
#     else:
#         products = Specification.query.order_by(Specification.creation_date).all()
#         return render_template('index.html', products = products)

# @app.route('/delete/<int:id>')

# def delete(id):
#     product_to_delete = Specification.query.get_or_404(id)

#     try:
#         db.session.delete(product_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There wwas a problem deleting the product'

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     product = Specification.query.get_or_404(id)
#     if request.method=='POST':
#         product.content = request.form['content']
#         product.price = request.form['price']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'Issue updating product'
#     else:
#         return render_template('update.html', product=product)

# if __name__=="__main__":
#     app.run(host='0.0.0.0', debug=True)