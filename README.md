
# Deployment procedure (to AWS EC2)

0. Be sure to open port 8000 from AWS console for the installation environment!

### Installing dependencies

1. `apt-get install python3-pip python3 sqlite3 python3-venv` (to installing the necessary packages) (this assumes that its running on debian/ubuntu where venv is NOT bundled with python3 by default)
2. `pip install -r requirements.txt`
   or
   `pip3 install django djangorestframework` (if requirements doesn't work) (do this after cloning the repository)

### Creating a virtual enviornment

3. `python3 -m venv NAME_OF_VENV` (to create a virtual enviornment for the deployment to keep dependencies isolated)

### Deploying the project

4. `cd NAME_OF_VENV` &&
   `git clone ...` (to get the necessary project files)
   `source bin/activate` to activate the virtul environment
    install dependency using the method from step 2   
    
5. go to crudAPI/settings.py, change allowed hosts from
   `[*]`
   to
   `['127.0.0.1', 'localhost', '{EC2_DNS_NAME}']`
   (so that you can access the endpoint via postman or browser, optionally you can add instance IP address if you want)
6. go to root project directory (where manage.py is) and run the following command
   `python3 manage.py migrate` (to create and initalize db)
7. `python3 manage.py test` (to run the tests)
8. to server run the command
   `python3 manage.py runserver 0:8000`, the default server will run on port 8000

you can use postman or browser to send requests at _{EC2_DNS_NAME}:8000_



# Exposed endpoints

There are 3 endpoints available, namely
* /category = end point to create and retrieve categories
* /category/pk = endpoint to update and delete category with the id = pk

* /products = end point to create and retrieve products
* /products/pk = endpoint to update and delete product with the id = pk

* /category-details = get list of categories, each containing a list of products it hsa relationship with (namely, all the products inside the list have that particular category as foreign key)
* /category-details/pk = get category and products where category id = pk;
