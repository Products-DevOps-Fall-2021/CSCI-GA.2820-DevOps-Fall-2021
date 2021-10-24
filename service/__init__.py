import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import service.models as models

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

from service import routes

