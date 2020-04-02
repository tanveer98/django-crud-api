



### deployment procedure (to AWS EC2)

##  deployment to aws EC2
### Installing dependencies
1. apt-get install python3-pip python3 sqlite3 python3-venv to installing the necesasry packages
2. pip install -r requirements.txt or pip3 install django djangorestframework for dependencies

### Creating a virtual enviornment
3. python3 -m venv NAME_OF_VENV to create a virtual enviornment for the deployment (to keep dependencies isolated)

### Deploying the project
4. git clone (inside the venv)
5. go to crudAPI/settings.py, changed allowed hosts from [*] to ['127.0.0.1', 'localhost', '{EC2_INSTNC_DNS}', (optional), {'EC2_INSTANCE_IP}'] (so that you can acess the endpoint via postman or browser)
6. go to root project directory (where manage.py is) and run the following command python3 manage.py migrate (to create the sqlite db)
7. to server run the command python3 manage.py runserver 0:8000, the default server will run on port 8000

you can use postman or browser to send requests at {EC2_DNS_NAME}:8000

