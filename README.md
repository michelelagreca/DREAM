# Zoccheddu-LaGreca-Careddu
SW2 project

Google Docs document link:
https://docs.google.com/document/d/1M-lFGYc8HXF9tZ1pWb0d9tbTAmUPu-RdDyBFiRMbaas/edit

Comment:
The first RASD 1.0 has been delivered into a folder called Delivery not DeliveryFolder, after it has been changed but the old is left to prove the met RASD deadline.

INSTALLATION PROCEDURE
# Project initialization
Following instructions are useful to initialize the DREAM project on a local machine.
● Git is required for cloning the project from GitHub. The git installation procedure
is available in the following link:
https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

● To clone the project from GitHub: git clone
https://github.com/gccianmario/Zoccheddu-LaGreca-Careddu

# Django installation
Following instructions are useful to correctly install the Django backend.

● Python is required. Information about the installation are provided in the following
link: https://www.python.org/downloads/

● Firstly, it is necessary to go in the directory using the CMD terminal in Windows:
../Zoccheddu-LaGreca-Careddu\IT\dream-backend

● To install Django:
pip install django

● To install Django rest framework:
pip install djangorestframework

● To install cors headers:
pip install django-cors-headers

● To install coverage:
pip install coverage

● To run the server:
python manage.py runserver
Note: some packages may be already installed.
Copyright © 2022, Careddu G., La Greca M., Zoccheddu S. – All rights reserved 28
DREAM Careddu Gianmario, La Greca Michele Carlo, Zoccheddu Sara

# Django testing
Following instructions are useful to execute the testing of the backend.
● Firstly, it is necessary to go in the backend directory:
../Zoccheddu-LaGreca-Careddu\IT\dream-backend

● To install coverage: pip install coverage

● To run tests: coverage run manage.py test

● To view a detailed report in the console, with informations about the testing
percentage of the code: coverage report -m

● To view a html report, it is possible to run the following command, and it will be
available in the folder /htmlcov (to visualize it, it is necessary to open the file
index.html in a web browser): coverage html

# React installation
● Download and install NodeJs from the following link: https://nodejs.org/en/,
choose the option to automatic add to the PATH variable npm otherwise a further
step of configuration will be needed for the next part

● Go to ../Zoccheddu-LaGreca-Careddu\IT\dream-frontend with
CMD terminal in Windows and run the following commands:
npm install ( to install all the dependencies)
npm start (to run the web application on localhost:3000 by default)

# Deployment
For the correct operation of the system in local environment the django backend has to
run on http://127.0.0.1:8000/
Instead the React application has to run on http://localhost:3000/

# Django admin and extra informations

The console admin can be used for data insertion and modification at the following link:
http://127.0.0.1:8000/admin/
Maximum care has to be taken since the action performed in the console admin can
lead to inconsistent state of the database especially for the creation of new users and
their authentication.
It is possible to access to the server using the admin through the previous url, inserting
the following credentials:

● Email address: admin@gmail.com

● Password: admin

(all the registered user has admin as password to simplify testing)

