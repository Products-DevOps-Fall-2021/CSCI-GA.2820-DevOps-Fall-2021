# products

### Setting up the development environment
Install [Git](http://git-scm.com/downloads) for using bash commands.
To setup the development environment, we use [Vagrant](https://www.vagrantup.com/downloads) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads). The recommended code editor is [Visual Studio Code](https://code.visualstudio.com/).

The Vagrantfile installs all of the needed software to run the service. You can clone this github repository and follow the given commands to start running the service:
 
```bash
git clone https://github.com/products-devops-fall-21/products.git  

cd products     

#bring up the vm
vagrant up 

#open a shell inside the vm
vagrant ssh 

cd /vagrant

python run.py

[---------------------------------------------------------
    To display the logs use the following command instead:
    honcho start
---------------------------------------------------------]
#At this point the website will be live

#exit out of the vm shell back to your host computer
exit 

#shutdown the vm to return later with vagrant up
vagrant halt 
```



search [127.0.0.1:5000](http://127.0.0.1:5000/) on browser to access the website and find the URL for accessing '/products' page.

### The Database for products has following columns:
| Column | Type | Description
| :--- | :--- | :--- |
| id | Integer | ID (automatically given by database) 
| name | String | Name of the product
| description | String | Description of product
| creation date | DateTime | Creation date and time of product
| price | Float | Price of product

### API Documentation

 |                 URL                 | HTTP Method |                         Description                          | HTTP Return Code |
| :---------------------------------: | :---------: | :----------------------------------------------------------: | :---------------:|
|              /           |   **GET**   |              The Name of Rest API service, the version and URL to list all products             |  HTTP_200_OK |
|              /products              |   **GET**   |              Returns a list all of the products              | HTTP_200_OK |
|           /products/{id}            |   **GET**   |             Returns the product with a given id in JSON format             | HTTP_200_OK |
|              /products              |  **POST**   | creates a new product with ID and creation date auto assigned by the Database and adds it to the products list | HTTP_201_CREATED |
|           /products/{id}            |   **PUT**   | updates the product with given id with the credentials specified in the request |  HTTP_200_OK |
|           /products/{id}            | **DELETE**  |           deletes a product record from the database           | HTTP_204_NO_CONTENT |

### Testing
Use the following commands to run the test cases:

Mac: 
```
nosetests
```
Windows: 
```
nosetests --exe
```

As of now we are able to receive 95% test coverage.