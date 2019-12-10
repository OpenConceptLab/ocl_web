# ocl_web

Web client interface for Open Concept Lab terminology services API.

## Docker setup

### Prerequisites

Docker

### Development

Before starting the web project, you need to start the API as described in
https://github.com/OpenConceptLab/oclapi

To run the server in a development mode use:
docker-compose up

To take down the server use:
docker-compose down

To take down the server and drop all data:
docker-compose down -v

### Debugging

Using PyCharm 2017.2

1. Start the server in development mode.
2. Import the project into PyCharm by pointing to ocl_web as root directory
3. Go to Settings -> Project: ocl_web -> Project Interpreter
4. Click the cog icon and Add Remote
5. Choose SSH Credentials and fill in the form as follows:
``` 
Host: localhost
Port: 2001
User name: root
Password: Root123
Python interpreter path: /usr/local/bin/python
``` 
6. Accept all warnings regarding certificates.
7. Close settings with OK
8. Go to Run -> Edit Configurations...
9. Click the plus icon and choose Django server
10. Fill in the form as follows (adjust working directory and path mappings accordingly):
``` 
Name: oclweb
Host: 0.0.0.0
Port: 7001
Working directory: C:\Users\Rafal\Workspace\ocl_web\
Path mappings: C:/Users/Rafal/Workspace/ocl_web/=/code
```
11. Confirm with OK and debug with the newly created configuration.
12. Go to http://localhost:7001 to verify it works.

By default the OCL WEB server runs against OCL API at 8000. If you want to run it against an OCL API debug server, open the debug configuration
and add the following environment variable: 
``` 
OCL_API_HOST=http://172.17.0.1:8001'
``` 

### Running Tests

#### Unit Tests

`docker-compose run web bash run_unit_tests.sh`

#### UI Tests

```
docker build -t openconceptlab/oclweb:dev .
docker run --rm openconceptlab/oclweb:dev bash run_ui_tests.sh
```

## Continous Integration

Please see https://github.com/OpenConceptLab/oclapi/blob/jetstream/README.md#continuous-integration

## Manual Developer Setup

### Prerequisites

1. ocl_web  
   * Fork the repo on Github
   * Clone your fork locally
   ```
   git clone https://github.com/{youruser}/ocl_web.git
   ```   
   * Add a remote repo to upstream in order to be able to fetch updates:
   ```
   cd ocl_web
   git remote add upstream https://github.com/OpenConceptLab/ocl_web
   ```
   
2. python
3. npm
4. pip
5. python virtualenv
  * ``` pip install virtualenv ```
6. OCL API must be setup, up and running.

### OCL Web Setup

1. Change working directory to repository root
   ```sh
   cd ocl_web 
   ```
2. Create a virtualenv for the project (NOTE: "env" is the name of virtualenv by convention, but you can give it any name, just be sure to add it to the ignores list in git)
   ```sh 
   virtualenv env #Creates a virtual environment
   ```
3. Create the file that will be used as the DB for ocl_web
   ```sh
   touch ocl.db 
   ```
4. Activate the virtual environment created in step __2__ . For deactivation of virtual env just write 'deactivate'. (NOTE: Replace "env" with the directory name you used to create your virtual environment)
   ```sh
   source ./env/bin/activate
   ```
5. Set the environment variables below to let OCL Web connect to API and set the DB location. Note that OclAPI must be already setup for this, you can see the token at http://0.0.0.0:8000/admin/authtoken/token/ (8000 is the port where oclapi server is running). Note that for a local development environment, OCL_API_HOST will typically be set to `http://localhost:8000`.
   
   ```sh
   export OCL_API_HOST='<your_api_server_ip>'
   export OCL_API_TOKEN='<root_token_from_api>'
   export OCL_ANON_API_TOKEN='<root_token_from_api>'
   export DATABASE_URL=sqlite:////<OCL_WEB_ROOT>/ocl.db
   
   ```
   
6. Install python and node.js dependencies -- NOTE: Make sure your version of pip in your virtualenv is up-to-date (e.g. pip install --upgrade pip)
   ```sh 
   pip install -r requirements/local.txt
   npm install
   ```
7. Install grunt cli 
   ```sh
   npm install -g grunt-cli
   ```
8. Prepare database (create tables for models and apply migrations)
   ```sh
   python ocl_web/manage.py syncdb #You will be prompted to create an ocl_web superuser
   python ocl_web/manage.py migrate 
   ```
9. Create a user. Make sure to get status=201 on the output. Otherwise the user is not created.
   ```sh
   python ocl_web/manage.py create_test_user --username <username> --password <password>
   ```
10. Serve the application 
   ```sh 
   grunt serve 
   ```
11. Application should be up at http://localhost:7000 and you should be able to login with the user created in step __9__


### Running Tests

OCL_WEB has a suite of unit tests written in python (django test) and end-to-end tests written in [protractor](https://github.com/angular/protractor) running either headless (PhantomJS) or Chrome.

1. Unit Tets
  ```sh
  python ocl_web/manage.py test 
  ``` 
2. Running E2E tests
  * Headless on showcase server: 
  ```sh
  ./run_ui_tests.sh 
  ```
  * Locally on Chrome: 
  ```sh 
  OCL_WEB=. browser=phantomjs env=local username=<username> password=<pwd> ./run_ui_tests.sh
  ```


## Settings

__cookiecutter-django__ relies extensively on environment settings which **will not work with Apache/mod_wsgi setups**. It has been deployed successfully with both Gunicorn/Nginx and even uWSGI/Nginx.

For configuration purposes, the following table maps the cookiecutter-django environment variables to their Django setting:

|          Environment Variable         | Django Setting                 | Development Default                            | Production Default                          |
|:-------------------------------------:|--------------------------------|------------------------------------------------|---------------------------------------------|
| DJANGO_AWS_ACCESS_KEY_ID              | AWS_ACCESS_KEY_ID              | n/a                                            | raises error                                |
| DJANGO_AWS_SECRET_ACCESS_KEY          | AWS_SECRET_ACCESS_KEY          | n/a                                            | raises error                                |
| DJANGO_AWS_STORAGE_BUCKET_NAME        | AWS_STORAGE_BUCKET_NAME        | n/a                                            | raises error                                |
| DJANGO_CACHES                         | CACHES                         | locmem                                         | memcached                                   |
| DJANGO_DEBUG                          | DEBUG                          | True                                           | False                                       |
| DJANGO_EMAIL_BACKEND                  | EMAIL_BACKEND                  | django.core.mail.backends.console.EmailBackend | django.core.mail.backends.smtp.EmailBackend |
| DJANGO_SECRET_KEY                     | SECRET_KEY                     | CHANGEME!!!                                    | raises error                                |
| DJANGO_SECURE_BROWSER_XSS_FILTER      | SECURE_BROWSER_XSS_FILTER      | n/a                                            | True                                        |
| DJANGO_SECURE_SSL_REDIRECT            | SECURE_SSL_REDIRECT            | n/a                                            | True                                        |
| DJANGO_SECURE_CONTENT_TYPE_NOSNIFF    | SECURE_CONTENT_TYPE_NOSNIFF    | n/a                                            | True                                        |
| DJANGO_SECURE_FRAME_DENY              | SECURE_FRAME_DENY              | n/a                                            | True                                        |
| DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS | SECURE_HSTS_INCLUDE_SUBDOMAINS | n/a                                            | True                                        |
| DJANGO_SESSION_COOKIE_HTTPONLY        | SESSION_COOKIE_HTTPONLY        | n/a                                            | True                                        |
| DJANGO_SESSION_COOKIE_SECURE          | SESSION_COOKIE_SECURE          | n/a                                            | False                                       |
* TODO: Add vendor-added settings in another table


> Copyright (C) 2016 Open Concept Lab. Use of this software is subject
> to the terms of the Mozille Public License v2.0. Open Concept Lab is
> also distributed under the terms the Healthcare Disclaimer
> described at http://www.openconceptlab.org/license/.
