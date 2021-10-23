import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #test.db = our database
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

if __name__=="__main__":
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    # print("sumit")
    app.run(host=host, port=port, debug=True)