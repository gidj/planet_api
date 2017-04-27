# planet_api

Small API for serving assets

Instructions:
-------------

Use Vagrant (preferred):
* Make sure you have vagrant intalled.
* Clone the repo, and 'cd' into the base directory.
* As long as you want to use the provided defaults, just issue the following command:
** vagrant up
* Wait for the box to download and Vagrant to provision the VM
* After provisioning, the base API endpoint is at http://192.168.33.10/api/v1/

Manully (not really recommended):
* Make sure you have PostgreSQL installed on the machine you will use, and that it is running
* Create the 'planet' user:
** createuser planet
* Create the 'planet' database:
** createdb planet
* Clone the planet_api repository, and cd into it:
** git clone https://github.com/gidj/planet_api.git && cd planet_api
* Create a virtualenv and source it:
** virtualenv venv && source venv/bin/activate
* Intall the requirements:
** pip install -r requirements.pip
* Set up the database:
** python manage.py db upgrade
* Start the app:
** python manage.py runserver
* Now you should be able to access the API at localhost:5000/api/v1/



