import os
from service.start import app
from service.products import init_db

DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

if __name__ == "__main__":
    print("**********************************************")
    print(" P R O D U C T   S E R V I C E   R U N N I N G")
    print("**********************************************")
    init_db()
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)